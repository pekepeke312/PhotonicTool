from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pathlib
from server import app
import codecs

#get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../assets").resolve()

def create_layout(app):
	return html.Div([
		    html.Div([
				html.Div(["Author: This program was written by Isao Yoneda"]),
		        html.Div(["Copyright: The copyright of this program and source code belongs to Isao Yoneda"]),
		    ],
		    style={"border": "1px black solid"},
		    ),

		    html.Div([
		        html.Div([
		            html.Iframe(id='EG_HistoryLog',
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

@app.callback(
    Output('EG_HistoryLog','srcDoc'),
    [Input(component_id="ExcelGraph_tabs-selection", component_property="value")])
def update_historylog(Tabselection):
    data = ''
    if Tabselection == 'Revision History':
        Toppath = str(pathlib.Path(__file__).parent.parent.resolve())
        path = Toppath + str('\\assets\\')

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