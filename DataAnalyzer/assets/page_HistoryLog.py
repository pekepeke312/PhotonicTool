# import dash_html_components as html
# import dash_core_components as dcc
from dash import html
from dash import dcc

import pathlib

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
		            html.Iframe(id='HistoryLog',
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