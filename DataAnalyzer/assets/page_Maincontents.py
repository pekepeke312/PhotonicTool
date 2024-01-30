from dash import html
from dash import dcc
import pathlib

#get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../assets").resolve()

def create_layout(app):
	return html.Div([
		    html.Div([
		        html.Div([
		            html.H2("CSV, S2P, BOM or Promira file"),
		            dcc.Upload(
		                id="upload-data",
		                children=html.Div(
		                    ["Drag and drop or click to select a file to upload."]
		                ),
		                style={
		                    "width": "90%",
		                    "height": "60px",
		                    "lineHeight": "60px",
		                    "borderWidth": "2px",
		                    "borderStyle": "dashed",
		                    "borderRadius": "5px",
		                    "textAlign": "center",
		                    "margin": "10px",
		                },
		                multiple=True,
		            ),
		        ],className = 'six columns'
		        ),

		        html.Div([
		            html.H2("Showing File"),
		            html.Ul(id="showing-File"),
		        ], className='three columns',
		        ),

		        html.Div([
		            html.H2("Stored File List"),
		            html.Ul(id="file-list"),
		        ],className = 'three columns'
		        ),

		    ],className='row',
		    style={"border":"1px black solid"},
		    ),

		    html.Div([
		        html.Div(["Supporting file formats:"]),
		        html.Div(["1. .CSV from Oscilloscope\n"]),
		        html.Div(["2. .S2P from Network Analyzer\n"]),
		        html.Div(["3. 'BOM' file name in xls/xlsx/xlsm file for BOM check\n"],),
				html.Div(["4. 'Promira' file name in xls/xlsx/xlsm file for Promira Serial Batch Creator\n"],),
		    ],
		    style={"border": "1px black solid"},
		    ),

		    html.Div([
		        html.Div(["Operation Log:"]),
		        dcc.Interval(
		            id='interval1',
		            interval=1 * 1000, # in milliseconds
		            n_intervals=0,
		        ),
		        html.Div([
		            html.Iframe(id='console-out',
		                        srcDoc='',
		                        style=dict(height='300px',
		                                    width="100%",
		                                    overflow='auto')
		            )
		        ],className= 'twelve',
		        )
		    ],className= 'row',
		    style = {"border": "1px black solid"},
		),
])