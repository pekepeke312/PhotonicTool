import base64
from pdf2image import convert_from_bytes
from TextWriter import TextWriter
import time
import os
import pathlib

#get relative data folder
PATH = pathlib.PurePath(__file__).parent
# DATA_PATH = PATH.joinpath("/assets").resolve()

Folder_Path = PATH.joinpath("assets")

def pdf2base64(file):
    starttime = time.time()
    base64file = []
    filename = file.split(".")[0]
    foldername = filename.split("/")[-1]
    pngfilelocation = Folder_Path.joinpath(foldername)

    try:
        os.mkdir(pngfilelocation)
    except:
        pass

    encoded_image = convert_from_bytes(open(file, "rb").read())
    for n in range(len(encoded_image)):
        pngfilename = filename +"/" + foldername +"_" + str(n) + ".png"
        encoded_image[n].save(pngfilename, "PNG")
        # print("png_" + str(n) + "saved")
        # TextWriter("png_" + str(n) + "saved")
        base64file.append(base64.b64encode(open(pngfilename, 'rb').read()).decode('ascii'))
        print("PDF Page No" + str(n+1) + " loaded")
        TextWriter("PDF Page No" + str(n+1) + " loaded")

    elapstedtime = time.time() - starttime
    print("PDF to base64 Conversion Completed in {:.3}s".format(elapstedtime))
    TextWriter("PDF to base64 Conversion Completed in {:.3}s".format(elapstedtime))

    return base64file

if __name__ == "__main__":
    file=r"assets/Altium.pdf"
    pdf2base64(file)