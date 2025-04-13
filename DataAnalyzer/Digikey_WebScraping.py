import time
#import pyautogui
import ctypes
import pathlib

from selenium import webdriver
from selenium.webdriver.edge import service
# import webbrowser
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from textwriter import textwriter


class Digikey_WebScraping():
    def __init__(self, PartNumber = ""):
        self.initial()
        self.TargetPN = PartNumber
#       self.Scraping()
#       self.terminate()

    def terminate(self):
        self.chrome.close()
        self.chrome.quit()

    def initial(self):
#       self.chrome = webdriver.Chrome(ChromeDriverManager().install())
#         options = webdriver.ChromeOptions()
#         options.add_argument('--disable-blink-features=AutomationControlled')
#         options.add_argument("--disable-extensions")
#         options.add_experimental_option('useAutomationExtension', False)
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         options.add_experimental_option('excludeSwitches', ['enable-logging'])
#         options.add_experimental_option("detach",True)
#
#
#         self.chrome = webdriver.Chrome(ChromeDriverManager().install(), options=options)


        # Microsoft Edge Version
        edgeOption = webdriver.EdgeOptions()
        edgeOption.use_chromium = True
        edgeOption.add_argument("start-maximized")
        edgeOption.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

        path = str(pathlib.Path(__file__).parent.resolve())
        driveraddress = path + r'\assets\Edge\edgedriver_win64\msedgedriver.exe'
        s = service.Service(driveraddress)
        self.edge = webdriver.Edge(service=s, options=edgeOption)


    def BotDetectorHandler(self):
        Button_lotions = self.chrome.find_element_by_xpath("/html/body/div/div/div[2]").rect

        scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
        click_position = [int(Button_lotions['x'] + Button_lotions['width'] / 2) * scaleFactor,
                          int(Button_lotions['y'] + Button_lotions['height'] * 2) * scaleFactor]
        BotText = "Click Position Search..."
        print(BotText)
        textwriter(BotText)

        click_element = self.chrome.find_element_by_xpath('/html/body/div/div/div[2]')
        time.sleep(1)

        BotText = "Mouse Button Holding..."
        print(BotText)
        textwriter(BotText)

        ActionChains(self.chrome).click_and_hold(click_element).perform()
        time.sleep(5)

        pyautogui.moveTo(x=click_position[0], y=click_position[1], duration=0.1)
        pyautogui.mouseDown(x=click_position[0], y=click_position[1], duration=20)
        pyautogui.moveTo(x=click_position[0]+1, y=click_position[1], duration=0.1)
        pyautogui.moveTo(x=click_position[0] - 1, y=click_position[1], duration=0.1)
        pyautogui.mouseUp(x=click_position[0], y=click_position[1], duration=3)
        time.sleep(5)


        # pyautogui.mouseUp(button='left')
        # pyautogui.mouseDown(x=click_position[0], y=click_position[1],button='right')
        # time.sleep(15)
        # pyautogui.mouseUp(button='right')
        # time.sleep(10)

        # while(1):
        #     print(pyautogui.position())
        #     textwriter(pyautogui.position())



    def Scraping(self):
#       Mouser_URL = 'https://www.mouser.ca/Search/Refine?Keyword='
        Digikey_URL = "https://www.digikey.ca/en/products?KeyWords="
        Search_URL = Digikey_URL + self.TargetPN

        # self.chrome.get(Search_URL)
        self.edge.get(Search_URL)

        ### Ctrl + Shift + 'I' makes debug mode in Chrome

        try:
            if "At DigiKey," in  self.chrome.find_element_by_xpath('/html/body/div/div/div[1]').text:
                BotText = "\nBot Detection Program appeared..."
                print(BotText)
                textwriter(BotText)
                self.BotDetectorHandler()
        except:
            pass

        try:
            SearchCount = int(self.chrome.find_element_by_xpath('/html/body/div[2]/main/section/div[1]/section/div[1]/div[2]/span/span').text)
            if SearchCount > 1:
                ### Search it until single product
                #First_PartNumber = self.chrome.find_element_by_class_name("tr-mfgPartNumber")
                First_PartNumber = self.chrome.find_element_by_xpath('/html/body/div[2]/main/section/div[2]/div[2]/div/div[1]/table/tbody/tr[1]/td[2]/div/div[3]/a[1]')
                #aTag = First_PartNumber.find_element_by_tag_name("a")
                url = First_PartNumber.get_attribute("href")
                # self.chrome.get(url)
                self.edge.get(url)
        except:
            pass

        # ParameterRow = self.chrome.find_elements_by_tag_name("tr")
        ParameterRow = self.edge.find_elements_by_tag_name("tr")
        self.PartInfo = {}
        for param in ParameterRow:
#            idx_space = param.text.find(' ')
            idx_newline = param.text.find('\n')
#            idx = min([idx_space,idx_newline])
            idx = idx_newline
            Param_Later = param.text[idx + 1:]
            if len(Param_Later) > 0:
                if Param_Later[:2] == '/ ':
                    Param_Later = Param_Later[2:]
                if Param_Later[0] == ' ':
                    Param_Later = Param_Later[1:]
                if Param_Later[:2] == '- ':
                    Param_Later = Param_Later[2:]

            if Param_Later.find('\n') == -1:
                self.PartInfo[param.text[:idx]] = Param_Later[:]
            else:
                self.PartInfo[param.text[:idx]] = Param_Later[:Param_Later.find('\n')]

        #### Getting DigiKey Qty ###
        try:
            Qty_text = self.chrome.find_element_by_xpath('/html/body/div[2]/div/main/div/div[1]/div[2]/div/div/div/div[1]/div').text
            Qty_text = self.edge.find_element_by_xpath(
                '/html/body/div[2]/div/main/div/div[1]/div[2]/div/div/div/div[1]/div').text
            return Qty_text
        except:
            return ""



if __name__ == "__main__":
    starttime = time.time()
    PartNumber = "MAX13450EAUD+"
    DigikeyResult = Digikey_WebScraping(PartNumber=PartNumber)
    DigikeyResult.Scraping()

    for key, value in DigikeyResult.PartInfo.items():
        print("{} : {}".format(key, value))

    DigikeyResult.terminate()
    elapsedtime = time.time() - starttime

    print("Operation Completed in {:.3}s".format(elapsedtime))