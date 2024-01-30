import base64
from urllib.parse import quote as urlquote
# import dash_html_components as html
# import dash_core_components as dcc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pathlib
import os

#from dash_core_components import Interval
import sys
import codecs

from server import FILEPATH
from server import app
if __name__ != "__main__":

    from .SpectrumAnalyzer import *
    from .API_Mouser import *
    from .smith import *
    from .Promira_Serial_Control import *

else:
    #from server import FILEPATH
    from SpectrumAnalyzer import *
    from API_Mouser import *
    #from server import app
    from smith import *

Target_Path = '0'
Modification_Time = '0'
SPA = 0

def Running_Promira_File_Converter(FileFull_Path):
    print("---Promira Serial Control Batch Creation Mode ---")
    TextWriter("---Promira Serial Control Batch Creation Mode ---")
    global Target_Path
    global Modification_Time
    global SPA
    if Modification_Time != os.path.getmtime(FileFull_Path):
        Modification_Time = os.path.getmtime(FileFull_Path)
        SPA = Promira_Serial_Control(FilePath=FileFull_Path)

def Running_SpectrumAnalyzer(FileFull_Path):
    print("---Time Domain & Freq Domain Analysis Mode ---")
    TextWriter("---Time Domain & Freq Domain Analysis Mode ---")
    global Target_Path
    global SPA
    global Modification_Time
    if Modification_Time != os.path.getmtime(FileFull_Path):
        Modification_Time = os.path.getmtime(FileFull_Path)
        Target_Path = FileFull_Path
        SPA = SpectrumAnalyzer(Target_Path)

def Running_RFAnalyzer(FileFull_Path):
    print("---RF Parameter Analysis Mode ---")
    TextWriter("---RF Parameter Analysis Mode ---")
    global Target_Path
    global SPA
    global Modification_Time
    if Modification_Time != os.path.getmtime(FileFull_Path):
        Modification_Time = os.path.getmtime(FileFull_Path)
        Target_Path = FileFull_Path
        SPA = smith(Target_Path)

def Running_API_Mouser(FileFull_Path):
    print("---BOM Data Analysis Mode ---")
    TextWriter("---BOM Data Analysis Mode ---")
    apikey=os.environ['MOUSER_API']
    global Target_Path
    global SPA
    global Modification_Time
    if Modification_Time != os.path.getmtime(FileFull_Path):
        Modification_Time = os.path.getmtime(FileFull_Path)
        Target_Path = FileFull_Path
        SPA = API_Mouser(APIKEY=apikey,PATH=Target_Path)

def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(FILEPATH, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(FILEPATH):
        path = os.path.join(FILEPATH, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)

def show_callbacks(app):

    def format_regs(registrations, padding=10):
        # TODO: -- switch to single line printing if > 79 chars
        vals = sorted("{}.{}".format(i['id'], i['property'])
                      for i in registrations)
        return ", ".join(vals)

    output_list = []

    for callback_id, callback in app.callback_map.items():
        wrapped_func = callback['callback'].__wrapped__
        inputs = callback['inputs']
        states = callback['state']
        events = callback['events']

        str_values = {
            'callback': wrapped_func.__name__,
            'output': callback_id,
            'filename': os.path.split(wrapped_func.__code__.co_filename)[-1],
            'lineno': wrapped_func.__code__.co_firstlineno,
            'num_inputs': len(inputs),
            'num_states': len(states),
            'num_events': len(events),
            'inputs': format_regs(inputs),
            'states': format_regs(states),
            'events': format_regs(events)
        }

        output = """                                                                                                                                                                           
        callback      {callback} @ {filename}:{lineno}                                                                                                                                         
        Output        {output}                                                                                                                                                                 
        Inputs  {num_inputs:>4}  {inputs}                                                                                                                                                      
        States  {num_states:>4}  {states}                                                                                                                                                      
        Events  {num_events:>4}  {events}                                                                                                                                                      
        """.format(**str_values)

        output_list.append(output)
    return "\n".join(output_list)

@app.callback(
    Output(component_id="file-list",component_property=  "children"),
    [Input(component_id="upload-data",component_property=  "filename"),
     Input(component_id="upload-data",component_property=  "contents")])
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)
    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        filelist = [html.Li(file_download_link(filename)) for filename in files]
        return filelist[:6-1]


@app.callback(
    Output(component_id="showing-File",component_property=  "children"),
    [Input(component_id="upload-data",component_property=  "filename"),
     Input(component_id="upload-data",component_property=  "contents")])
def Processing_File(uploaded_filenames, uploaded_file_contents):
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        FileFullPath = FILEPATH + "\\" + uploaded_filenames[0]
        FileFullPath = r'{}'.format(FileFullPath)
        if ('BOM' in uploaded_filenames[0]):
            Running_API_Mouser(FileFullPath)
        elif ('promira' in uploaded_filenames[0].lower()):
            Running_Promira_File_Converter(FileFullPath)
            global SPA
        elif ('.csv' in uploaded_filenames[0] or '.xls' in uploaded_filenames[0]):
            Running_SpectrumAnalyzer(FileFullPath)
            global SPA
        elif('.s2p' in uploaded_filenames[0] or '.S2P' in uploaded_filenames[0]):
            Running_RFAnalyzer(FileFullPath)
            global SPA
        return [html.Li(uploaded_filenames)]

global history_file
@app.callback(
    Output('HistoryLog','srcDoc'),
    [Input(component_id="DataAnalyzer_tabs-selection", component_property="value")])
def update_historylog(Tabselection):
    data = ''
    if Tabselection == 'Revision History':
        Toppath = str(pathlib.Path(__file__).parent.parent.resolve())
        path = Toppath + str('\\DataAnalyzer\\assets\\')
        # try:
        #     path = os.environ['DataAnalyzerPath'] + str('\\DataAnalyzer\\assets\\')
        # except:
        #     path = os.getcwd() + str('\\DataAnalyzer\\assets\\')

        global history_file
        global file
        try:
            file = open(path + 'History_Log.txt', 'r')
        except:
            pass

        try:
            lines = file.readlines()
        except:
            fd = codecs.open(path + 'History_Log.txt', 'r', encoding='utf-8')
            lines = fd.read()

        for line in lines:
           data = data + line + '<BR>'

        file.close()
    return data


global file
@app.callback(
    Output('console-out','srcDoc'),
    [Input('interval1','n_intervals')])
def update_output(n):
    TextLine = 14

    Toppath = str(pathlib.Path(__file__).parent.parent.resolve())
    path = Toppath + str('\\Top_Assets\\')

    #path = os.getcwd() + str('\\Top_Assets\\')
    path = r'{}'.format(path)

    global file
    try:
        file = open(path + 'Log.txt', 'r')
    except:
        pass

    data = ''
    try:
        lines = file.readlines()
    except:
        fd = codecs.open(path + 'Log.txt', 'r', encoding='utf-8')
        lines = fd.read()

    if lines.__len__() <= TextLine:
        last_lines = lines
    else:
        last_lines = lines[-1*TextLine:]
    for line in last_lines:
        data = data + line + '<BR>'
    file.close()
    return data