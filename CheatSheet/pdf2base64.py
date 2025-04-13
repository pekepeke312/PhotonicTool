import base64
from pdf2image import convert_from_bytes
from textwriter import textwriter
import time
import os
import pathlib

#get relative data folder
PATH = pathlib.PurePath(__file__).parent
# PNG_PATH = PATH.joinpath("/assets/pngfiles")

Folder_Path = PATH.joinpath("assets")
PNGFILE_Path = Folder_Path.joinpath("pngfiles")
try:
    os.mkdir(PNGFILE_Path)
except:
    pass

def pdf2base64(file):
    starttime = time.time()
    base64file = []
    filename = file.split(".")[0]
    foldername = filename.split("/")[-1]
    pngfilelocation = PNGFILE_Path.joinpath(foldername)

    try:
        os.mkdir(pngfilelocation)
    except:
        pass

    encoded_image = convert_from_bytes(open(file, "rb").read())
    print("Loading " + file)
    textwriter("Loading " + file)

    for n in range(len(encoded_image)):
        # pngfilename = filename +"/"  + foldername +"_" + str(n) + ".png"
        pngfilename = str(pngfilelocation) + "/" + foldername + "_" + str(n) + ".png"
        encoded_image[n].save(pngfilename, "PNG")
        # print("png_" + str(n) + "saved")
        # textwriter("png_" + str(n) + "saved")
        base64file.append(base64.b64encode(open(pngfilename, 'rb').read()).decode('ascii'))
        print("PDF Page No" + str(n+1) + " loaded")
        textwriter("PDF Page No" + str(n+1) + " loaded")

    elapstedtime = time.time() - starttime
    print("PDF to base64 Conversion Completed in {:.3}s".format(elapstedtime))
    textwriter("PDF to base64 Conversion Completed in {:.3}s".format(elapstedtime))

    return base64file

if __name__ == "__main__":
    file=r"assets/Altium.pdf"
    pdf2base64(file)