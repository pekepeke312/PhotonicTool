from dash import html
from dash.dependencies import Input, Output, State
import pathlib
from server import app
import codecs

def create_layout(app):
	return html.Div([
			html.Div([
				html.Div(["Author: Isao Yoneda"]),
				html.Div(["Copyright: The copyright of this program belongs to Photonic Inc."]),
			],
			style={"border": "1px black solid"},
			),

			html.Div([
				html.Div([
					html.Iframe(id='PS_HistoryLog',
								srcDoc='',
								style=dict(height='600px',
											width="100%",
											overflow='auto')
					)
				],className= 'twelve',
				),
			],className= 'row',
			style = {"border": "1px black solid"},
			),
	])

global history_file
@app.callback(
    Output('PS_HistoryLog','srcDoc'),
    [Input(component_id="PartSearch-tabs-selection", component_property="value")])
def update_historylog(Tabselection):
    data = ''
    if Tabselection == 'Revision History':
        Toppath = str(pathlib.Path(__file__).parent.parent.resolve())
        path = Toppath + str('\\assets\\')
        #path = os.getcwd() + str('\\PowerModuleCheck\\assets\\')

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
