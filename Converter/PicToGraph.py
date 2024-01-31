import time
import cv2
from PIL import Image
import numpy as np
import pandas as pd
import pathlib
import plotly.graph_objects as go
from TextWriter import TextWriter

### OCR Library ###
import pytesseract
from pytesseract import Output
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

OPENCV_HUE_RANGE_SCALE = 360/180
LEGEND_DETECTION_RANGE = 5

class PicToGraph:
    def __init__(self,PicturePath=""):
        self.PicturePath = PicturePath
        self.PictureLoader()

    def PictureLoader(self):
        im = Image.open(self.PicturePath)
        im.save(self.PicturePath[:-3] + "-600.png")
        self.PictureData_RGB = cv2.imread(self.PicturePath[:-3] + "-600.png")
        #self.PictureData_RGB = cv2.imread(self.PicturePath)
        self.PictureData_HSV = cv2.cvtColor(self.PictureData_RGB, cv2.COLOR_RGB2HSV)
        self.PictureData_H = (360 - 1 * (self.PictureData_HSV[:, :, 0] * OPENCV_HUE_RANGE_SCALE - 240)) % 360

        self.X_Axis_Length = self.PictureData_H.shape[1]
        self.Y_Axis_Length = self.PictureData_H.shape[0]

    def DeployImage(self,image=""):
        cv2.imshow("ImageView",image)
        cv2.waitKey(0)

    def ImageResize(self,image="",Scale=2):
        ### Resize
        Scale = Scale
        width = image.shape[1] * Scale
        height = image.shape[0] * Scale
        dim = (width, height)

        resized = cv2.resize(image,dim,interpolation=cv2.INTER_AREA)
        return resized

    def ImageCleanUp(self,image="",Scale=2, GrayProcess=True,BinaryThreshHold =127, Binarization=True,Erosion=True,Smooth=True):
        img = self.ImageResize(image,Scale)

        if GrayProcess:
            # Convert to gray
            img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            if Binarization:
                # Apply threshold to get image with only b&w (binarization)
                #img = cv2.threshold(img, BinaryThreshHold, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                img = cv2.threshold(img, BinaryThreshHold, 127, cv2.THRESH_BINARY)[1]

        if Erosion:
            # Apply dilation and erosion to remove some noise
            kernel = np.ones((1,1), np.uint8)
            img = cv2.dilate(img, kernel,iterations=1)
            img = cv2.erode(img, kernel, iterations=1)

        if Smooth:
            # Apply blur to smooth out the edges
            img = cv2.GaussianBlur(img, (5, 5), 0)

        return img

    def GrayImage(self,image=""):
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return grayImage

    def PicToString(self,image="",Scale=3):
        #resized = self.ImageResize(image,Scale=2)
        #ConvertedStr = pytesseract.pytesseract.image_to_string(resized)

        cleanedImage = self.ImageCleanUp(image=image,
                                       Scale=Scale,
                                       GrayProcess=False,
                                       Binarization=False,
                                       Erosion=True,
                                       Smooth=True,
                                       )
        ConvertedStr = pytesseract.pytesseract.image_to_string(cleanedImage)
        return ConvertedStr

    def PicToData(self, image="",ShowData=False,Scale=3,GrayProcess=True,Binarization=True,BinaryThreshHold=127,Erosion=True,Smooth=True):
        #resized = self.ImageResize(image,Scale=5)
        cleanedImage = self.ImageCleanUp(image=image,
                                       Scale=Scale,
                                       GrayProcess=GrayProcess,
                                       Binarization=Binarization,
                                       BinaryThreshHold = BinaryThreshHold,
                                       Erosion=Erosion,
                                       Smooth=Smooth,
                                       )
        Data = pytesseract.pytesseract.image_to_data(cleanedImage, output_type=Output.DICT)
        Data_DF = pd.DataFrame(Data)

        ReScalingItems = ['left','top','width','height']    ## Scaling back to original size
        for param in ReScalingItems:
            Data_DF[param] = list(map(lambda x: int(x / Scale), Data_DF[param]))

        Data_DF_Confident = Data_DF[Data_DF['conf'] != str(-1)]
        Data_DF_Confident = Data_DF_Confident[Data_DF_Confident['text'] != '']
        Data_DF_Confident = Data_DF_Confident[Data_DF_Confident['text'] != ' ']
        Data_DF_Confident = Data_DF_Confident[Data_DF_Confident['text'] != '  ']
        Data_DF_Confident = Data_DF_Confident[Data_DF_Confident['text'] != '   ']
        Data_DF_Confident = Data_DF_Confident[Data_DF_Confident['text'] != '|']

        Data_DF_Confident = Data_DF_Confident.reset_index()
        if ShowData:
            print("---- Image File Data ----")
            print('File Path: {}'.format(self.PicturePath))
            print('Size Horizontal: {}'.format(self.X_Axis_Length))
            print('Size Vertical: {}'.format(self.Y_Axis_Length))
            print("----Captured String Locations----")
            for n in range(len(Data_DF_Confident)):
                print("Text: {:4}\tX: {:4} \tY: {:4}".format(Data_DF_Confident['text'][n],Data_DF_Confident['left'][n],Data_DF_Confident['top'][n]))
            print("---------------------------------")

        return Data_DF_Confident

    def ImageDataMapper(self,image="",Data=""):
        n_boxes = len(Data['text'])
        img = image
        for i in range(n_boxes):
            try:
                if float(Data['conf'][i]) != -1:
                    (x, y, w, h) = (int(Data['left'][i]), int(Data['top'][i]), int(Data['width'][i]), int(Data['height'][i]))
                    img = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            except:
                print("")
        return img

    def ThreshHoldFinder(self,image=""):
        starttime = time.time()

        FoundData = {}
        Max_Text_Length = Max_Text_Count = Max_Thresh = 0
        for Thresh in range(0, 255, 25):
            DetectedData = self.PicToData(image=image, Scale=4, ShowData=False, BinaryThreshHold=Thresh, Smooth=False,
                                          Erosion=False)
            Text_Length = Text_Count = 0
            Text_Count = len(DetectedData['text'].values)
            for text in DetectedData['text'].values:
                Text_Length += len(text)

            ### Checking Text Group
            #CheckResult = {}
            # max_H = max_V = 0
            # for index in range(len(DetectedData)):
            #     count_H = count_V = max_thresh = 0
            #     for n in range(len(DetectedData)):
            #         if DetectedData['left'][index] <= DetectedData['left'][n] + LEGEND_DETECTION_RANGE and \
            #                 DetectedData['left'][index] >= DetectedData['left'][n] - LEGEND_DETECTION_RANGE:
            #             count_H += 1
            #
            #         if DetectedData['top'][index] <= DetectedData['top'][n] + LEGEND_DETECTION_RANGE and \
            #                 DetectedData['top'][index] >= DetectedData['top'][n] - LEGEND_DETECTION_RANGE:
            #             count_V += 1
            #
            #     if max_H <= count_H and max_V <= count_V:
            #         max_H = count_H
            #         max_V = count_V
            #
            #     CheckResult[index] = (count_H, count_V)
            # CheckResult_DF = pd.DataFrame(CheckResult)
            #
            # try:
            #     if max_H > max_V:
            #         self.LegendData_DF = DetectedData[CheckResult_DF.values[0] == max_H]
            #         max_thresh = Thresh
            #     else:
            #         self.LegendData_DF = DetectedData[CheckResult_DF.values[1] == max_V]
            #         max_thresh = Thresh

            if Max_Text_Count < Text_Count:
                Max_Text_Count = Text_Count

            if Max_Text_Length < Text_Length:
                Max_Text_Length = Text_Length

            if Max_Text_Length == Text_Length and Max_Text_Count == Text_Count:
                Max_Thresh = Thresh
                Max_FoundData = DetectedData
            # try:
            #     self.LegendData_DF
            # except:
            #     self.LegendData_DF = None

            #FoundData[Thresh] = FoundData


        elapstedtime = time.time() - starttime
        print("ThreshHoldFinder Completed in {:.3}s".format(elapstedtime))
        TextWriter("ThreshHoldFinder Completed in {:.3}s".format(elapstedtime))
        return [Max_Thresh, Max_FoundData]

    def LegendDetector(self,image=""):
        starttime = time.time()

        ThreshHold, TextData = self.ThreshHoldFinder(image=image)

        elapstedtime = time.time() - starttime
        print("LegendDetector Completed in {:.3}s".format(elapstedtime))
        TextWriter("LegendDetector Completed in {:.3}s".format(elapstedtime))

if __name__ == "__main__":
    path = r"C:\Users\pekep\Desktop\ggplot2-color-ggplot2-color-logo-1.png"
    Pic = PicToGraph(PicturePath=path)

    # Data = Pic.PicToData(image=Pic.PictureData_RGB,ShowData=True)
    # NewImage = Pic.ImageDataMapper(image=Pic.PictureData_RGB,Data=Data)
    # Pic.DeployImage(NewImage)

    Pic.LegendDetector(image=Pic.PictureData_RGB)

#    print(Pic.PicToString(image=Pic.PictureData_RGB,))
#    print(Pic.PicToData(image=Pic.PictureData_RGB))
#    Pic.DeployImage()
    #Pic.DeployImage()