import base64
from urllib.parse import quote as urlquote

import dash
import pandas as pd
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import pathlib
import math
import time
import os

# from .PicToGraph import PicToGraph

import sys
import codecs
from server import FILEPATH
from server import app

TEXT_POSITION = 'center'
BOX_WIDTH = '100%'
ROUNDING_NUMBER = 4

from .assets import (
    Converter_Impedance,
    Converter_PicToGraph,
    Converter_HistoryLog,
    Converter_ResonantFrequency,
    Converter_UnitConversion,
    Converter_PCB_Pattern_Impedance,
)

from .smithchart import smithchart
from textwriter import textwriter
from .ResonantFrequency import ResonantFrequency
from .UnitConversion import UnitConversion
from .PCB_Pattern_Width_Calculator import PCB_Pattern_Width

VSWR = GAMMA = RL = ML_dB = ML_P = RSource = RLoad = ''
VSWR_ABS = GAMMA_ABS = ''

def RL_Update(GAMMA):
    global RL
    if (GAMMA == 0.0) or (GAMMA == 0):
        RL = '-Inf'
    else:
        try:
            if abs(GAMMA) < 0:
                RL = round(20 * math.log10(float(abs(GAMMA))), 3)
                RL = -1 * RL
            else:
                RL = round(20 * math.log10(float(abs(GAMMA))), 3)
        except:
            print(f"Return Loss Calculation Error with GAMMA = {GAMMA}")
            textwriter(f"Return Loss Calculation Error with GAMMA = {GAMMA}")
    return RL

def ML_dB_Update(GAMMA):
    global ML_dB
    if (GAMMA == 0.0) or (GAMMA == 0):
            ML_dB = 0
    else:
        if abs(GAMMA) < 0:
            ML_dB = round(-10*math.log10(1-pow(float(abs(GAMMA)),2)),4)
            ML_dB = ML_dB * -1
        else:
            ML_dB = round(-10 * math.log10(1 - pow(float(abs(GAMMA)), 2)), 4)
    return ML_dB

def ML_P_Update(ML_dB):
    global ML_P
    ML_P = round((100*(1-pow(10,-1*float(ML_dB)/10))),4)
    return ML_P

@app.callback(
    [Output(component_id='ID_IMP_VSWR_ABS_Wrapper', component_property='children'),
     Output(component_id='ID_IMP_VSWR_Wrapper',component_property='children'),
     Output(component_id='ID_IMP_GAMMA_ABS_Wrapper',component_property='children'),
     Output(component_id='ID_IMP_GAMMA_Wrapper',component_property='children'),
     Output(component_id='ID_IMP_RL_Wrapper', component_property='children'),
     Output(component_id='ID_IMP_ML_DB_Wrapper', component_property='children'),
     Output(component_id='ID_IMP_ML_PC_Wrapper', component_property='children'),
     Output(component_id="ID_IMP_SMITH_GRAPH",component_property="figure"),
     ],
    [Input(component_id='IMP_SOURCE_IMP_INPUT', component_property='value'),
     Input(component_id='IMP_LOAD_IMP_INPUT', component_property='value'),
     Input(component_id='ID_IMP_VSWR', component_property='value'),
     Input(component_id='ID_IMP_GAMMA', component_property='value'),
     Input(component_id='ID_IMP_RL', component_property='value'),
     Input(component_id='ID_IMP_ML_DB', component_property='value'),
     Input(component_id='ID_IMP_ML_PC', component_property='value'),
     State(component_id='IMP_CHARAC_IMP_INPUT', component_property='value'),
     ]
)
def IMP_update(rsource,rload,vswr,gamma,rl,ml_dB,ml_p,Zo):
    global RSource, RLoad, VSWR,VSWR_ABS, GAMMA, GAMMA_ABS, RL, ML_dB, ML_P, RunningSmithChart
    trigger_id = dash.callback_context.triggered[0]["prop_id"]
    if trigger_id == "IMP_SOURCE_IMP_INPUT.value":
        if rsource == None or rsource == "":
            raise PreventUpdate
        try:
            RSource = float(rsource)
        except:
            RSource = complex(rsource)
        RLoad = complex(rload)
        GAMMA = (RSource.conjugate() - RLoad) / (RSource.conjugate() + RLoad)
        GAMMA_ABS = abs(GAMMA)

        try:
            VSWR = (1 + GAMMA) / (1 - GAMMA)
            VSWR_ABS = abs(VSWR)
            RL = RL_Update(GAMMA)
            ML_dB = ML_dB_Update(GAMMA)
            ML_P = ML_P_Update(ML_dB)
        except:
            print("Rsource = {}: InputError".format(rsource))
            textwriter("Rsource = {}: InputError".format(rsource))

    elif trigger_id == "IMP_LOAD_IMP_INPUT.value":
        if rload == None or rload == "":
            raise PreventUpdate
        RSource = complex(rsource)
        RLoad = complex(rload)
        GAMMA = (RSource.conjugate() - RLoad) / (RSource.conjugate() + RLoad)
        GAMMA_ABS = abs(GAMMA)

        try:
            VSWR = (1 + GAMMA) / (1 - GAMMA)
            VSWR_ABS = abs(VSWR)
            RL = RL_Update(GAMMA)
            ML_dB = ML_dB_Update(GAMMA)
            ML_P = ML_P_Update(ML_dB)
        except:
            print("Rload = {}: InputError".format(rload))
            textwriter("Rload = {}: InputError".format(rload))

    elif trigger_id == "ID_IMP_VSWR.value":
        if vswr != "" and vswr != None:
            try:
                VSWR = float(vswr)
            except:
                VSWR = complex(vswr)
        else:
            raise PreventUpdate
        try:
    #        VSWR = abs(round((GAMMA + 1) / (GAMMA - 1), 4))
            VSWR_ABS = abs(VSWR)
            GAMMA = (VSWR - 1) / (VSWR + 1)
            GAMMA_ABS = abs(GAMMA)
            RL = RL_Update(GAMMA)
            ML_dB = ML_dB_Update(GAMMA)
            ML_P = ML_P_Update(ML_dB)
        except:
            print("VSWR = {}: InputError".format(vswr))
            textwriter("VSWR = {}: InputError".format(vswr))

    if trigger_id == "ID_IMP_GAMMA.value":
        if gamma != "" and gamma != None:
            try:
                GAMMA = float(gamma)
            except:
                try:
                    GAMMA = complex(gamma)
                except:
                    print("")
                GAMMA_ABS = abs(GAMMA)
        else:
            raise PreventUpdate
        try:
            VSWR = (1 + GAMMA) / (1-GAMMA)
            VSWR_ABS = abs(VSWR)
#            GAMMA = round((VSWR - 1) / (VSWR + 1), 4)
            RL = RL_Update(GAMMA)
            ML_dB = ML_dB_Update(GAMMA)
            ML_P = ML_P_Update(ML_dB)
        except:
            print("GAMMA = {}: InputError".format(gamma))
            textwriter("GAMMA = {}: InputError".format(gamma))

    if trigger_id == "ID_IMP_RL.value":
        if rl != "" and rl != None:
            RL = float(rl)
        else:
            raise PreventUpdate
        try:
            GAMMA =pow(10,RL/20)
            GAMMA_ABS = abs(GAMMA)
            VSWR = (GAMMA + 1) / (GAMMA - 1)
            VSWR_ABS = abs(VSWR)
            # RL = RL_Update(GAMMA)
            ML_dB = ML_dB_Update(GAMMA)
            ML_P = ML_P_Update(ML_dB)
        except:
            print("Return Loss = {}: InputError".format(rl))
            textwriter("Return Loss = {}: InputError".format(rl))

    if trigger_id == "ID_IMP_ML_DB.value":
        if ml_dB != "" and ml_dB != None:
            ML_dB = float(ml_dB)
        else:
            raise PreventUpdate
        try:
            GAMMA = math.sqrt(abs(1 - pow(10, ML_dB / 10)))
            GAMMA_ABS = abs(GAMMA)
            VSWR = (GAMMA + 1) / (GAMMA - 1)
            VSWR_ABS = abs(VSWR)
            RL = RL_Update(GAMMA)
            #ML_dB = ML_dB_Update(GAMMA)
            ML_P = ML_P_Update(ML_dB)
        except:
            print("Matching Loss = {}: InputError".format(ml_dB))
            textwriter("Matching Loss = {}: InputError".format(ml_dB))

    if trigger_id == "ID_IMP_ML_PC.value":
        if ml_p != "" and ml_p != None:
            ML_P = float(ml_p)
        else:
            raise PreventUpdate
        try:
            ML_dB = round((20-10*math.log10(100-ML_P)),4)
            GAMMA = math.sqrt(abs(1 - pow(10, ML_dB / 10)))
            GAMMA_ABS = abs(GAMMA)
            VSWR = (GAMMA + 1) / (GAMMA - 1)
            VSWR_ABS = abs(VSWR)
            RL = RL_Update(GAMMA)
        except:
            print("Matching Loss = {}: InputError".format(ml_dB))
            textwriter("Matching Loss = {}: InputError".format(ml_dB))


    try:
        VSWR_ABS_VIEW = str(round(VSWR_ABS,ROUNDING_NUMBER))
        VSWR_VIEW = str(round(VSWR.real,ROUNDING_NUMBER) +1j*round(VSWR.imag,ROUNDING_NUMBER))[1:][:-1]
        GAMMA_ABS_VIEW = str(round(GAMMA_ABS,ROUNDING_NUMBER))
        if GAMMA != complex(0j):
            GAMMA_VIEW = str(round(GAMMA.real,ROUNDING_NUMBER) +1j*round(GAMMA.imag,ROUNDING_NUMBER))[1:][:-1]
        else:
            GAMMA_VIEW = 0
        if isinstance(RL,str) == False:
            RL_VIEW = str(round(RL,ROUNDING_NUMBER))
        else:
            RL_VIEW = RL
        ML_dB_VIEW = str(round(ML_dB,ROUNDING_NUMBER))
        ML_P_VIEW = str(round(ML_P,ROUNDING_NUMBER))
    except:
        raise PreventUpdate

    if RunningSmithChart != 0:
        RunningSmithChart.DrawingGraph(Zo=Zo,Rs=RSource,Rl=RLoad,Gamma_ABS=GAMMA_ABS,Gamma=GAMMA)
    return [dcc.Input(id='ID_IMP_VSWR_ABS', value=VSWR_ABS_VIEW, debounce=True, style={'textAlign': TEXT_POSITION, 'width': '75%'}, ),
            dcc.Input(id='ID_IMP_VSWR', value=VSWR_VIEW, debounce=True, style={'textAlign': TEXT_POSITION, 'width': BOX_WIDTH}, ),
            dcc.Input(id='ID_IMP_GAMMA_ABS', value=GAMMA_ABS_VIEW, debounce=True, style={'textAlign': TEXT_POSITION, 'width': '75%'}, ),
            dcc.Input(id='ID_IMP_GAMMA', value=GAMMA_VIEW, debounce=True, style={'textAlign': TEXT_POSITION, 'width': BOX_WIDTH}, ),
            dcc.Input(id='ID_IMP_RL', value=RL_VIEW, debounce=True, style={'textAlign': TEXT_POSITION}, ),
            dcc.Input(id='ID_IMP_ML_DB', value=ML_dB_VIEW, debounce=True, style={'textAlign': TEXT_POSITION}, ),
            dcc.Input(id='ID_IMP_ML_PC', value=ML_P_VIEW, debounce=True, style={'textAlign': TEXT_POSITION}, ),
            RunningSmithChart.Fig_2D,
            ]

global file
@app.callback(
    Output('Converter_console-out','srcDoc'),
    [Input('Converter_interval1','n_intervals')])
def Converter_update_output(n):
    TextLine = 15

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

RunningSmithChart = 0
def Run_SmithChart(Z=50):
    global RunningSmithChart
    RunningSmithChart = smithchart()#Z=50)
    return RunningSmithChart

RunningUnitConversion = 0
def Run_UnitConversion():
    RunningUnitConversion = UnitConversion()
    return RunningUnitConversion


RunningResonantFrequency = 0
def Run_ResonantFrequency():
    global RunningResonantFrequency
    RunningResonantFrequency = ResonantFrequency()
    return RunningResonantFrequency
#### --------------------------------------------------------------------
## Pic To Graph Functions -----

def CV_save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    FileLocation = str(pathlib.Path(__file__).parent)
    FileLocation += '\\assets'
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(FileLocation, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

RunningPicToGraph = 0
@app.callback(
    Output(component_id="PicToGraph_Loading_File_Name", component_property="children"),
    [Input(component_id="PicToGraph_upload-data", component_property="filename"),
     Input(component_id="PicToGraph_upload-data", component_property="contents")])
def ImageFileOpenner(uploaded_filenames, uploaded_file_contents):
    global RunningPicToGraph
    """Save uploaded files and regenerate the file list."""
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        starttime = time.time()

        for name, data in zip(['temp.'+str(uploaded_filenames[0].split('.')[1])], uploaded_file_contents):
            try:
                CV_save_file(name, data)
            except:
                print("Close temp."+str(uploaded_filenames[0].split('.')[1]) + " to proceed process")

        Path = str(pathlib.Path(__file__).parent)
        Path += '\\assets\\'+ name

        RunningPicToGraph = PicToGraph(Path)
        RunningPicToGraph.DeployImage()

        elapstedtime = time.time() - starttime
        print("Image File was loaded in {:.3}s".format(elapstedtime))
        textwriter("Image File was loaded in {:.3}s".format(elapstedtime))

    if uploaded_filenames != None:
        return ["File = "+uploaded_filenames[0]]
    else:
        return ["File = "]


@app.callback(
    Output(component_id="Converter_page_contents", component_property="children"),
    [Input(component_id="Converter_tabs-selection", component_property="value"),
    Input(component_id="Converter_url", component_property="pathname")]
)
def Converter_page(DataAnalyzer_Tabselection,pathname):
    global RunningSmithChart
    global RunningUnitConversion
    if DataAnalyzer_Tabselection == 'Impedance':     #Default Page
        RunningSmithChart = Run_SmithChart(50)
        return Converter_Impedance.create_layout(app)

    elif DataAnalyzer_Tabselection == 'Pic-to-Graph':
        return Converter_PicToGraph.create_layout(app)

    elif DataAnalyzer_Tabselection == 'Revision History':
        return Converter_HistoryLog.create_layout(app)

    elif DataAnalyzer_Tabselection == 'ResonantFrequency':
        return Converter_ResonantFrequency.create_layout(app)

    elif DataAnalyzer_Tabselection == 'PCB Pattern':
        return Converter_PCB_Pattern_Impedance.create_layout(app)

    elif DataAnalyzer_Tabselection == 'Unit':
        RunningUnitConversion = Run_UnitConversion()
        return Converter_UnitConversion.create_layout(app)

    else:
        return html.Div("not yet")

#### Unit Conversion Tool

@app.callback(
    [Output(component_id="DD_UnitConversion_Category", component_property="options"),
     Output(component_id="DD_UnitConversion_To", component_property="options"),
     Output(component_id="DD_UnitConversion_From", component_property="options"),
     Output(component_id="ID_Param_1_Name", component_property="children"),
     Output(component_id="ID_Param_2_Name", component_property="children"),
     Output(component_id="ID_Param_3_Name", component_property="children"),
     Output(component_id="ID_Param_4_Name", component_property="children"),
     Output(component_id="ID_Param_5_Name", component_property="children"),
     Output(component_id="ID_Param_6_Name", component_property="children"),
     Output(component_id="ID_Param_7_Name", component_property="children"),
     Output(component_id="ID_Param_8_Name", component_property="children"),
     ],
    [Input(component_id='DD_UnitConversion_Category', component_property='value'),
     Input(component_id='DD_UnitConversion_From', component_property='value'),
     Input(component_id='DD_UnitConversion_To', component_property='value'),
     ]
)
def Conversion_Name_update(Category,From, To):
    global RunningUnitConversion
    trigger_id = dash.callback_context.triggered[0]["prop_id"]
    if RunningUnitConversion == 0:
        print("Conversion List of To Update")
        textwriter("Conversion List of To Update")

    if trigger_id ==  "DD_UnitConversion_Category.value":
        RunningUnitConversion.FromList(Category=Category, To=To)
        RunningUnitConversion.ToList(Category=Category, From=From)
    elif trigger_id == "DD_UnitConversion_From.value":
        RunningUnitConversion.CategoryList(From=From, To=To)
        RunningUnitConversion.ToList(From=From, Category=Category)
    elif trigger_id == "DD_UnitConversion_To.value":
        RunningUnitConversion.CategoryList(To=To, From=From)
        RunningUnitConversion.FromList(To=To, Category=Category)

    ####--Name ------------
    RunningUnitConversion.RemainintParts(To=To, From=From, Category=Category)
    if RunningUnitConversion.GraphState:
        RunningUnitConversion.InputWidgetUpdate()
        Param1_Name = RunningUnitConversion.ParamList[0]
        try:
            Param2_Name = RunningUnitConversion.ParamList[1]
        except:
            Param2_Name = "Param2"
        try:
            Param3_Name = RunningUnitConversion.ParamList[2]
        except:
            Param3_Name = "Param3"
        try:
            Param4_Name = RunningUnitConversion.ParamList[3]
        except:
            Param4_Name = "Param4"
        try:
            Param5_Name = RunningUnitConversion.ParamList[4]
        except:
            Param5_Name = "Param5"
        try:
            Param6_Name = RunningUnitConversion.ParamList[5]
        except:
            Param6_Name = "Param6"
        try:
            Param7_Name = RunningUnitConversion.ParamList[6]
        except:
            Param7_Name = "Param7"
        try:
            Param8_Name = RunningUnitConversion.ParamList[7]
        except:
            Param8_Name = "Param8"
    else:
        Param1_Name = "Param1"
        Param2_Name = "Param2"
        Param3_Name = "Param3"
        Param4_Name = "Param4"
        Param5_Name = "Param5"
        Param6_Name = "Param6"
        Param7_Name = "Param7"
        Param8_Name = "Param8"

    return [RunningUnitConversion.CategoryListData,
            RunningUnitConversion.ToListData,
            RunningUnitConversion.FromListData,
            Param1_Name,
            Param2_Name,
            Param3_Name,
            Param4_Name,
            Param5_Name,
            Param6_Name,
            Param7_Name,
            Param8_Name,
            ]



@app.callback(
    [Output(component_id="ID_Param_1_MIN", component_property="value"),
     Output(component_id="ID_Param_1_MAX", component_property="value"),
     Output(component_id="ID_Param_2", component_property="value"),
     Output(component_id="ID_Param_3", component_property="value"),
     Output(component_id="ID_Param_4", component_property="value"),
     Output(component_id="ID_Param_5", component_property="value"),
     Output(component_id="ID_Param_6", component_property="value"),
     Output(component_id="ID_Param_7", component_property="value"),
     Output(component_id="ID_Param_8", component_property="value"),

     ],
    [Input(component_id="ID_Param_1_Name", component_property="children"),
     Input(component_id="ID_Param_2_Name", component_property="children"),
     Input(component_id="ID_Param_3_Name", component_property="children"),
     Input(component_id="ID_Param_4_Name", component_property="children"),
     Input(component_id="ID_Param_5_Name", component_property="children"),
     Input(component_id="ID_Param_6_Name", component_property="children"),
     Input(component_id="ID_Param_7_Name", component_property="children"),
     Input(component_id="ID_Param_8_Name", component_property="children"),
     ]
)
def Conversion_Value_update(P1,P2,P3,P4,P5,P6,P7,P8):
    global RunningUnitConversion
    if RunningUnitConversion.GraphState:
        RunningUnitConversion.InputParameterValueUpdate()
        Param1_min = float(RunningUnitConversion.Param1_min_value)
        Param1_max = float(RunningUnitConversion.Param1_max_value)
        try:
            Param2 = float(RunningUnitConversion.Param2_value)
        except:
            Param2 = ""

        try:
            Param3 = float(RunningUnitConversion.Param3_value)
        except:
            Param3 = ""

        try:
            Param4 = float(RunningUnitConversion.Param4_value)
        except:
            Param4 = ""

        try:
            Param5 = float(RunningUnitConversion.Param5_value)
        except:
            Param5 = ""

        try:
            Param6 = float(RunningUnitConversion.Param6_value)
        except:
            Param6 = ""

        try:
            Param7 = float(RunningUnitConversion.Param7_value)
        except:
            Param7 = ""

        try:
            Param8 = float(RunningUnitConversion.Param8_value)
        except:
            Param8 = ""
        return [
            Param1_min,
            Param1_max,
            Param2,
            Param3,
            Param4,
            Param5,
            Param6,
            Param7,
            Param8,
        ]
    else:
        return [
            dash.no_update,
            dash.no_update,
            dash.no_update,
            dash.no_update,
            dash.no_update,
            dash.no_update,
            dash.no_update,
            dash.no_update,
            dash.no_update,
        ]

@app.callback(
    [Output(component_id="id_UnitConversion_Formula",component_property="figure"),
     ],
    [Input(component_id='ID_Param_1_MIN', component_property='value'),
     Input(component_id='ID_Param_1_MAX', component_property='value'),
     Input(component_id='ID_Param_2', component_property='value'),
     Input(component_id='ID_Param_3', component_property='value'),
     Input(component_id='ID_Param_4', component_property='value'),
     Input(component_id='ID_Param_5', component_property='value'),
     Input(component_id='ID_Param_6', component_property='value'),
     Input(component_id='ID_Param_7', component_property='value'),
     Input(component_id='ID_Param_8', component_property='value'),
     ]
)
def Latex_Graph_update(Param1_MIN,Param1_MAX,Param2,Param3,Param4,Param5,Param6,Param7,Param8):
    global RunningUnitConversion
    if RunningUnitConversion != 0 and Param1_MIN !="":
        if RunningUnitConversion.GraphState:
            GraphData = RunningUnitConversion.RelationShipGraphGenerator(Param1_MAX=Param1_MAX,
                                                                     Param1_MIN=Param1_MIN,
                                                                     Param2=Param2,
                                                                     Param3=Param3,
                                                                     Param4=Param4,
                                                                     Param5=Param5,
                                                                     Param6=Param6,
                                                                     Param7=Param7,
                                                                     Param8=Param8,
                                                                     )
    try:
        return [GraphData]
    except:
        return [dash.no_update]

###### Resonant Frequency Tool
RESO_FREQ= 0
FREQ_UNIT = ""
@app.callback(
    [Output(component_id="ID_RESONANT_FREQUENCY_GRAPH",component_property="figure"),
     ],
    [Input(component_id='Resonant_Frequency_Input_ID', component_property='value'),
     Input(component_id='ID_UnitList', component_property='value'),
     Input(component_id='ID_ChipSIze', component_property='value')
     ]
)
def RESONANT_update(resonant_freq,freq_unit,Chipsize):
    global RESO_FREQ, FREQ_UNIT, RunningResonantFrequency
    if RunningResonantFrequency == 0:
        print("Resonant Frequency Finder Mode")
        textwriter("Resonant Frequency Finder Mode")
    ResonatFrequencyInstance = Run_ResonantFrequency()

    NewGraph = ResonatFrequencyInstance.FindingResonant(ResonantFrequency=resonant_freq, ChipInductance=Chipsize,Resonant_Frequency_Unit=freq_unit)

    return [NewGraph]

@app.callback(
    [Output(component_id="ID_PCB_Pattern_Graph",component_property="children"),
     Output(component_id="ID_PCB_Pattern_Formula",component_property="children"),
     Output(component_id='ID_PCB_Param_3_Name', component_property="children"),
     Output(component_id='ID_PCB_Param_4_Name', component_property="children"),
     Output(component_id='ID_PCB_Param_5_Name', component_property="children"),
     ],
    [Input(component_id='Variation_tabs-selection', component_property='value'),
     ]
)
def PCB_Pattern_update(PCB_Pattern_Tab_Selection):

    if PCB_Pattern_Tab_Selection == "Microstrip":
        Microstrip_path = "Converter/assets/ImageData/Microstrip-2.png"
        Microstrip_image = base64.b64encode(open(Microstrip_path, "rb").read()).decode()

        Graph = html.Img(src=f"data:image/png;base64,{Microstrip_image}", style={'width': '100%', 'height': 'auto'})
        Formula = html.Div([
            dcc.Markdown(r'''
                $$ 
                \large
                \begin{aligned}
                    \epsilon_{e} &=
                    \left\{
                    \begin{array}{ll}
                        \frac{\epsilon_{r}+1}{2} + \frac{\epsilon_{r}-1}{2} 
                        \biggl[ \frac{1}{\sqrt{1+12(\frac{h}{W})}} +0.4(1-\frac{W}{h})^{2} \biggr] & ( W < h) \\[10pt]
                        \frac{\epsilon_{r}+1}{2} + \biggl[ \frac{\epsilon_{r}-1}{2 \sqrt{1+12 (\frac{h}{W})}} \biggr] & ( W > h) 
                    \end{array}
                    \right. \\[15pt]
                    Z_{o} &=
                    \left\{
                    \begin{array}{ll}
                        \frac{60}{\sqrt{\epsilon_{e}}} \ln \left( 8 \frac{h}{W} + 0.25 \frac{W}{h} \right)  & ( W < h) \\[10pt]
                        \frac{120\pi}{\sqrt{\epsilon_{e}} \left[ \frac{W}{h} + 1.393 + \frac{2}{3} \ln \left( \frac{W}{h} + 1.444 \right) \right]} & ( W > h ) \\[10pt]
                    \end{array}
                    \right.
                \end{aligned}
                $$
                ''',mathjax=True)
        ])
        Param3= "Height (h)"
        Param4= html.Pre("           ")
        Param5= html.Pre("           ")


    elif PCB_Pattern_Tab_Selection == "Stripline":
        Stripline_path = "Converter/assets/ImageData/Stripline-2.png"
        Stripline_image = base64.b64encode(open(Stripline_path, "rb").read()).decode()
        Graph = html.Img(src=f"data:image/png;base64,{Stripline_image}", style={'width': '100%', 'height': 'auto'})

        Formula = html.Div([
            dcc.Markdown(r'''
                $$ 
                \large
                Z_o = \frac{60}{\sqrt{\varepsilon_r}} \times \ln \left( \frac{1.9(2h + t)}{(0.8w + t)} \right)
                $$
                ''',mathjax=True)
        ])
        Param3= "Height (h)"
        Param4= html.Pre("           ")
        Param5= html.Pre("           ")



    elif PCB_Pattern_Tab_Selection == "Asymmetric Stripline":
        Asymmetric_Stripline_path = "Converter/assets/ImageData/Asymmetric Stripline-2.png"
        Asymmetric_Stripline_image = base64.b64encode(open(Asymmetric_Stripline_path, "rb").read()).decode()
        Graph = html.Img(src=f"data:image/png;base64,{Asymmetric_Stripline_image}", style={'width': '100%', 'height': 'auto'})

        Formula = html.Div([
            dcc.Markdown(r'''
                $$ 
                \large
                Z_o = \frac{80}{\sqrt{\varepsilon_r}} \times \ln \left( \frac{1.9(2h_a + t)}{(0.8w + t)} \right) \times \left( 1 - \frac{h_a}{4h_b} \right)
                $$
                ''',mathjax=True)
        ])
        Param3 = "Height (ha)"
        Param4 = "Height (hb)"
        Param5= html.Pre("           ")


    elif PCB_Pattern_Tab_Selection == "Embedded Microstrip":
        Embedded_Microstrip_path = "Converter/assets/ImageData/Embedded Microstrip-2.png"
        Embedded_Microstrip_image = base64.b64encode(open(Embedded_Microstrip_path, "rb").read()).decode()
        Graph = html.Img(src=f"data:image/png;base64,{Embedded_Microstrip_image}", style={'width': '100%', 'height': 'auto'})

        Formula = html.Div([
            dcc.Markdown(r'''
               $$ 
               \large
               Z_o = \frac{60}{\sqrt{\varepsilon_{rp}}} \times \ln \left( \frac{5.98h_{p}}{0.8w + t} \right)
               $$

               $$ 
               \large
               \varepsilon_{rp} = \varepsilon_{r} \left[ 1 - \exp \left( -1.55 \frac{h}{h_{p}} \right) \right]
               $$ 
               ''', mathjax=True)
        ])
        Param3 = "Height (h)"
        Param4 = "Height (hp)"
        Param5= html.Pre("           ")


    elif PCB_Pattern_Tab_Selection == "Edge Coupled Microstrip":
        Edge_Coupled_Microstrip_path = "Converter/assets/ImageData/Edge Coupled Microstrip-2.png"
        Edge_Coupled_Microstrip_image = base64.b64encode(open(Edge_Coupled_Microstrip_path, "rb").read()).decode()
        Graph = html.Img(src=f"data:image/png;base64,{Edge_Coupled_Microstrip_image}", style={'width': '100%', 'height': 'auto'})

        Formula = html.Div([
            dcc.Markdown(r'''
                       $$ 
                       \large
                       Z_d = \frac{174}{\sqrt{\varepsilon_r} + 1.41} \times \ln \left( \frac{5.98h}{0.8w + t} \right) \times \left[ 1 - 0.48 \exp \left( -0.96 \frac{s}{h} \right) \right]
                       $$
                       ''', mathjax=True)
        ])
        Param3 = "Height (h)"
        Param4 = "Gap (S)"
        Param5= html.Pre("           ")

    elif PCB_Pattern_Tab_Selection == "Edge Coupled Stripline":
        Edge_Coupled_Stripline_path = "Converter/assets/ImageData/Edge Coupled Stripline-2.png"
        Edge_Coupled_Stripline_image = base64.b64encode(open(Edge_Coupled_Stripline_path, "rb").read()).decode()
        Graph = html.Img(src=f"data:image/png;base64,{Edge_Coupled_Stripline_image}", style={'width': '100%', 'height': 'auto'})

        Formula = html.Div([
            dcc.Markdown(r'''
               $$ 
               \large
               Z_o = \frac{60}{\sqrt{\varepsilon_r}} \times \ln \left( \frac{1.9(2h + t)}{(0.8w + t)} \right)
               $$

               $$ 
               \large
               Z_d = 2Z_o \left[ 1 - 0.347 \exp \left( -\frac{2.9s}{2h + t} \right) \right]
               $$ 
               ''', mathjax=True)
        ])
        Param3 = "Height (h)"
        Param4 = "Gap (S)"
        Param5 = html.Pre("           ")


    elif PCB_Pattern_Tab_Selection == "Broadside Coupled Stripline":
        Broadside_Coupled_Stripline_path = "Converter/assets/ImageData/Broadside Coupled Stripline-2.png"
        Broadside_Coupled_Stripline_image = base64.b64encode(open(Broadside_Coupled_Stripline_path, "rb").read()).decode()
        Graph = html.Img(src=f"data:image/png;base64,{Broadside_Coupled_Stripline_image}", style={'width': '100%', 'height': 'auto'})

        Formula = html.Div([
            dcc.Markdown(r'''
               $$ 
               \large
               Z_o = \frac{80}{\sqrt{\varepsilon_r}} \times \ln \left( \frac{1.9(2h_p + t)}{(0.8w + t)} \right) \times \left( 1 - \frac{h_p}{4(h_{t} + h_p + t)} \right)
               $$
               ''', mathjax=True)
        ])
        Param3 = "Height (hp)"
        Param4 = "Height (ht)"
        Param5= html.Pre("           ")

    elif PCB_Pattern_Tab_Selection == "Coplanar Waveguide With Ground":
        Coplanar_Waveguide_With_Ground_path = "Converter/assets/ImageData/Coplanar Waveguide With Ground-2.png"
        Coplanar_Waveguide_With_Ground_image = base64.b64encode(open(Coplanar_Waveguide_With_Ground_path, "rb").read()).decode()
        Graph = html.Img(src=f"data:image/png;base64,{Coplanar_Waveguide_With_Ground_image}", style={'width': '100%', 'height': 'auto'})


        Formula = html.Div([
            dcc.Markdown(r'''
                $$
                \large
                Z_0 = \frac{60\pi}{\sqrt{\varepsilon_{\mathrm{eff}}}} \cdot \left( \frac{1}{\dfrac{K(k)}{K(k')} + \dfrac{K(k_1)}{K(k_1')}} \right)
                $$
                
                $$
                \large
                k = \frac{W}{W + 2s}, \quad
                k' = \sqrt{1 - k^2}
                $$
                
                $$
                \large
                k_1 = \frac{\tanh\left( \dfrac{\pi W}{4h} \right)}{\tanh\left( \dfrac{\pi(W + 2s)}{4h} \right)}, \quad
                k_1' = \sqrt{1 - k_1^2}
                $$
                
                $$
                \large
                \varepsilon_{\mathrm{eff}} = \frac{1 + \varepsilon_r \cdot \dfrac{K(k')}{K(k)} \cdot \dfrac{K(k_1)}{K(k_1')}}{1 + \dfrac{K(k')}{K(k)} \cdot \dfrac{K(k_1)}{K(k_1')}}
                $$
                ''', mathjax=True)
        ])
        Param3 = "Gap (S)"
        Param4 = "Height (h)"
        Param5= html.Pre("           ")

    elif PCB_Pattern_Tab_Selection == "Asymmetric Coplanar Waveguide":
        Asymmetric_Coplanar_Waveguide_path = "Converter/assets/ImageData/Asymmetric CPW-2.png"
        Asymmetric_Coplanar_Waveguide_image = base64.b64encode(
            open(Asymmetric_Coplanar_Waveguide_path , "rb").read()).decode()
        Graph = html.Img(src=f"data:image/png;base64,{Asymmetric_Coplanar_Waveguide_image}",
                         style={'width': '100%', 'height': 'auto'})

        Formula = html.Div([
            dcc.Markdown(r'''
            $$
            \large
            Z_0 = \frac{60\pi}{\sqrt{\varepsilon_{\mathrm{eff}}}} \cdot \left( \frac{1}{\dfrac{K(k)}{K(k')} + \dfrac{K(k_1)}{K(k_1')}} \right)
            $$

            $$
            \large
            k = \frac{W}{W + 2s}, \quad
            k' = \sqrt{1 - k^2}
            $$

            $$
            \large
            k_1 = \frac{\tanh\left( \dfrac{\pi W}{4 h_{\text{eff}}} \right)}{\tanh\left( \dfrac{\pi(W + 2s)}{4 h_{\text{eff}}} \right)}, \quad
            k_1' = \sqrt{1 - k_1^2}
            $$

            $$
            \large
            h_{\text{eff}} = \frac{2 h_a h_b}{h_a + h_b}
            $$

            $$
            \large
            \varepsilon_{\mathrm{eff}} =
            \frac{1 + \varepsilon_r \cdot \dfrac{K(k')}{K(k)} \cdot \dfrac{K(k_1)}{K(k_1')}}{1 + \dfrac{K(k')}{K(k)} \cdot \dfrac{K(k_1)}{K(k_1')}}
            $$
            ''', mathjax=True)
        ])
        Param3 = "Gap (S)"
        Param4 = "Height (ha)"
        Param5 = "Height (hb)"

    return [Graph, Formula, Param3, Param4, Param5]

@app.callback(
    [Output(component_id="ID_PCB_Param_1_Input",component_property="value"),
     ],
    [Input(component_id='ID_PCB_Material_List', component_property='value'),
     ]
)
def PCB_DirectConstant_update(ListInput):
    return [ListInput]

@app.callback(
    [Output(component_id="ID_PCB_Graph",component_property="figure"),
     ],
    [Input(component_id='Variation_tabs-selection', component_property='value'),
     Input(component_id='ID_PCB_Param_0_MIN', component_property='value'),
     Input(component_id='ID_PCB_Param_0_MAX', component_property='value'),
     Input(component_id="ID_Param_0_unit_selector", component_property='value'),
     Input(component_id='ID_PCB_Param_1_Input', component_property='value'),
     Input(component_id='ID_PCB_Param_2', component_property='value'),
     Input(component_id="ID_Param_2_unit_selector", component_property='value'),
     Input(component_id='ID_PCB_Param_3', component_property='value'),
     Input(component_id="ID_Param_3_unit_selector", component_property='value'),
     Input(component_id='ID_PCB_Param_4', component_property='value'),
     Input(component_id="ID_Param_4_unit_selector", component_property='value'),
     Input(component_id='ID_PCB_Param_5', component_property='value'),
     Input(component_id="ID_Param_5_unit_selector", component_property='value'),
     ]
)
def PCB_Width_vs_Impedance_Calculation(MODE, Width_MIN,Width_MAX,Width_Unit,Param1,Param2,Param2_Unit,Param3,Param3_Unit,Param4,Param4_Unit,Param5,Param5_Unit,):
    if Width_MIN != "" and Width_MAX != "" and Param1 != None and Param2 != None and Param3 != None:
        width_min = float(Width_MIN) * 0.001 if Width_Unit == "mm" else 0.001 * 0.0254
        width_max = float(Width_MAX) * 0.001 if Width_Unit == "mm" else 0.001 * 0.0254

        param1 = float(Param1)

        if Param2_Unit == "oz":
            Param2_multiply = 0.0305e-4 / 8.96
        elif Param2_Unit == "um":
            Param2_multiply = 1e-6
        elif Param2_Unit == "mm":
            Param2_multiply = 0.001
        elif Param2_Unit == "mil":
            Param2_multiply = 0.001 * 0.0254

        param2 = float(Param2) * Param2_multiply

        if Param3_Unit == "um":
            Param3_multiply = 1e-6
        elif Param3_Unit == "mm":
            Param3_multiply = 0.001
        elif Param3_Unit == "mil":
            Param3_multiply = 0.001 * 0.0254

        try:
            param3 = float(Param3) * Param3_multiply
        except:
            param3 = 0



        if (MODE == "Asymmetric Stripline"
                or MODE == "Embedded Microstrip"
                or MODE == "Edge Coupled Microstrip"
                or MODE == "Edge Coupled Stripline"
                or MODE == "Broadside Coupled Stripline"
                or MODE == "Coplanar Waveguide With Ground"
                or MODE == "Asymmetric Coplanar Waveguide"
        ):
            if Param4 != None and Param4 != '':
                if Param4_Unit == "um":
                    Param4_multiply = 1e-6
                elif Param4_Unit == "mm":
                    Param4_multiply = 0.001
                elif Param4_Unit == "mil":
                    Param4_multiply = 0.001 * 0.0254
            try:
                param4 = float(Param4) * Param4_multiply
            except:
                param4 = 0

            if Param5 != None and Param5 != '':
                if Param5_Unit == "um":
                    Param5_multiply = 1e-6
                elif Param5_Unit == "mm":
                    Param5_multiply = 0.001
                elif Param5_Unit == "mil":
                    Param5_multiply = 0.001 * 0.0254

            try:
                param5 = float(Param5) * Param5_multiply
            except:
                param5 = 0

            PCB_Width = PCB_Pattern_Width(Mode = MODE,
                                        Width_min=width_min,
                                        Width_max=width_max,
                                        Param1=param1,
                                        Param2=param2,
                                        Param3=param3,
                                        Param4=param4,
                                        Param5=param5,
                                        )
            Graph_Data = PCB_Width.Graph_Gnerator()
            return [Graph_Data]

        if MODE == "Microstrip" or MODE == "Stripline":
            PCB_Width = PCB_Pattern_Width(Mode = MODE,
                                        Width_min=width_min,
                                        Width_max=width_max,
                                        Param1=param1,
                                        Param2=param2,
                                        Param3=param3,
                                        Param4=0,
                                        Param5=0,
                                        )

            Graph_Data = PCB_Width.Graph_Gnerator()
            return [Graph_Data]

    return[""]
