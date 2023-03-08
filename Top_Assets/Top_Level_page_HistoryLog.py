from dash import html
from server import app
from dash.dependencies import Input, Output
import os
import pathlib
import codecs

#get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../assets").resolve()

def Analysis_Tool_History_layout(app):
	return html.Div([
		    html.Div([
				html.Div(["Author: This program was written by Isao Yoneda"]),
		        html.Div(["Copyright: The copyright of this program and source code belongs to Isao Yoneda"]),
		    ],
		    style={"border": "1px black solid"},
		    ),

		    html.Div([
		        html.Div([
		            html.Iframe(id='Top_Level_HistoryLog',
		                        srcDoc='',
		                        style=dict(height='600px',
		                                    width="100%",
		                                    overflow='auto')
		            )
		        ],className= 'twelve',
		        )
		    ],className= 'row',
		    style = {"border": "1px black solid"},
		),
])

global TOP_HISTORY_FILE
global FILE
@app.callback(
    Output(component_id='Top_Level_HistoryLog',component_property='srcDoc'),
    [Input(component_id="tabs-selection", component_property="value")])
def update_historylog(Tabselection):
    data = ''
    if Tabselection == 'Revision History':
        Toppath = str(pathlib.Path(__file__).parent.parent.resolve())
        path = Toppath + str('\\Top_Assets\\')
        # try:
        #     path = os.environ['DataAnalyzerPath'] + str('\\Top_Assets\\')
        # except:
        #     path = os.getcwd() + str('\\Top_Assets\\')

        global TOP_HISTORY_FILE
        global FILE
        try:
            file = open(path + 'Top_Level_History_Log.txt', 'r')
        except:
            pass

        try:
            lines = file.readlines()
        except:
            fd = codecs.open(path + 'Top_Level_History_Log.txt', 'r', encoding='utf-8')
            lines = fd.read()

        for line in lines:
           data = data + line + '<BR>'

        file.close()
    return data
