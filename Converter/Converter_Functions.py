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

from .PicToGraph import PicToGraph

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
)

from .smithchart import smithchart
from TextWriter import TextWriter
from .ResonantFrequency import ResonantFrequency
from .UnitConversion import UnitConversion

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
            TextWriter(f"Return Loss Calculation Error with GAMMA = {GAMMA}")
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
            TextWriter("Rsource = {}: InputError".format(rsource))

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
            TextWriter("Rload = {}: InputError".format(rload))

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
            TextWriter("VSWR = {}: InputError".format(vswr))

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
            TextWriter("GAMMA = {}: InputError".format(gamma))

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
            TextWriter("Return Loss = {}: InputError".format(rl))

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
            TextWriter("Matching Loss = {}: InputError".format(ml_dB))

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
            TextWriter("Matching Loss = {}: InputError".format(ml_dB))


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
        TextWriter("Image File was loaded in {:.3}s".format(elapstedtime))

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

    elif DataAnalyzer_Tabselection == 'Unit':
        RunningUnitConversion = Run_UnitConversion()
        return Converter_UnitConversion.create_layout(app)

    else:
        return html.Div("not yet")

#### Unit Conversion Tool

# @app.callback(
#     [Output(component_id="DD_UnitConversion_Category", component_property="value"),
#      Output(component_id="DD_UnitConversion_To", component_property="value"),
#      Output(component_id="DD_UnitConversion_From", component_property="value"),
#      ],
#     [Input(component_id='DD_UnitConversion_Category', component_property='value'),
#      Input(component_id='DD_UnitConversion_From', component_property='value'),
#      Input(component_id='DD_UnitConversion_To', component_property='value'),
#      ]
# )
# def Conversion_Value_Reset(Category,From, To):
#     global RunningUnitConversion
#     if Category == None or From == None or To == None:
#         return ["","",""]

@app.callback(
    [Output(component_id="DD_UnitConversion_Category", component_property="options"),
     Output(component_id="DD_UnitConversion_To", component_property="options"),
     Output(component_id="DD_UnitConversion_From", component_property="options"),
     Output(component_id="ID_Param_1_Name", component_property="children"),
     Output(component_id="ID_Param_2_Name", component_property="children"),
     Output(component_id="ID_Param_3_Name", component_property="children"),
     Output(component_id="ID_Param_4_Name", component_property="children"),
     Output(component_id="ID_Param_5_Name", component_property="children"),
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
        TextWriter("Conversion List of To Update")

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
    else:
        Param1_Name = "Param1"
        Param2_Name = "Param2"
        Param3_Name = "Param3"
        Param4_Name = "Param4"
        Param5_Name = "Param5"

    return [RunningUnitConversion.CategoryListData,
            RunningUnitConversion.ToListData,
            RunningUnitConversion.FromListData,
            Param1_Name,
            Param2_Name,
            Param3_Name,
            Param4_Name,
            Param5_Name,
            ]



@app.callback(
    [Output(component_id="ID_Param_1_MIN", component_property="value"),
     Output(component_id="ID_Param_1_MAX", component_property="value"),
     Output(component_id="ID_Param_2", component_property="value"),
     Output(component_id="ID_Param_3", component_property="value"),
     Output(component_id="ID_Param_4", component_property="value"),
     Output(component_id="ID_Param_5", component_property="value"),

     ],
    [Input(component_id="ID_Param_1_Name", component_property="children"),
     Input(component_id="ID_Param_2_Name", component_property="children"),
     Input(component_id="ID_Param_3_Name", component_property="children"),
     Input(component_id="ID_Param_4_Name", component_property="children"),
     Input(component_id="ID_Param_5_Name", component_property="children"),
     ]
)
def Conversion_Value_update(P1,P2,P3,P4,P5):
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
        return [
            Param1_min,
            Param1_max,
            Param2,
            Param3,
            Param4,
            Param5,
        ]
    else:
        return [
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
     ]
)
def Latex_Graph_update(Param1_MIN,Param1_MAX,Param2,Param3,Param4,Param5):
    global RunningUnitConversion
    if RunningUnitConversion != 0:
        if RunningUnitConversion.GraphState:
            GraphData = RunningUnitConversion.RelationShipGraphGenerator(Param1_MAX=Param1_MAX,
                                                                     Param1_MIN=Param1_MIN,
                                                                     Param2=Param2,
                                                                     Param3=Param3,
                                                                     Param4=Param4,
                                                                     Param5=Param5,
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
        TextWriter("Resonant Frequency Finder Mode")
    ResonatFrequencyInstance = Run_ResonantFrequency()

    NewGraph = ResonatFrequencyInstance.FindingResonant(ResonantFrequency=resonant_freq, ChipInductance=Chipsize,Resonant_Frequency_Unit=freq_unit)

    return [NewGraph]