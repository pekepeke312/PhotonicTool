# ===================================================================================
# Program Name: Data Analyzer
# Function: This program is an interface program with Plotly
#           This version can support with Drag and Drop belows
#           1. Oscilloscope Data Analysis
#           2. RF Parameters Check
#           3. BOM Status Check
# @author: Isao Yoneda
# ====================================================================================

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from app import *
import webbrowser
import pathlib
import os
from textwriter import textwriter
from kill_server import kill_server

path = str(pathlib.Path(__file__).parent.resolve()) + str('\\Top_Assets\\')
path = r'{}'.format(path)

try:
    os.remove(path + "Log.txt")
except (Exception,):
    print(f"removing " + path + "Log.txt has error")

textwriter("", end="")   # To create a blank textlog file
# To give a permission to administrator account about drag and drop
os.system('cmd /c "net user administrator /active:yes"')

host = "http://127.0.0.1"
port = "8888"
kill_server(host=host, port=port)
webbrowser.open(host + ':' + port)

app.run_server(port=8888, debug=False,)
