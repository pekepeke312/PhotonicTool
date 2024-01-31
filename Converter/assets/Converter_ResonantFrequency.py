from dash import html
from dash import dcc
import pathlib
import Converter.Converter_Functions

#get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../assets").resolve()

TEXT_POSITION = 'center'

UnitList = [
	{'label': 'Hz', 'value': '1' },
    {'label': 'kHz', 'value': '1e3' },
	{'label': 'MHz', 'value': '1e6' },
	{'label': 'GHz', 'value': '1e9' },
]

ChipSizeList = [
	{'label': '0402', 'value': '400e-12'},
	{'label': '0603', 'value': '870e-12'},
	{'label': '0805', 'value': '1050e-12'},
	{'label': '1206', 'value': '1200e-12'},
	{'label': '1210', 'value': '980e-12'},
]

def create_layout(app):
	return html.Div([

		html.Div([
			## Data Input #################
			html.Div([
				html.H5("Input Parameters"),
				###################
				html.Div([
					html.Div([
						html.Div([
							html.Div([
								html.Label('Chip Size'),
							], className='twelve columns',
								style={'textAlign': 'left'},
							),
						],
						),
						html.Div([
							html.Div([
								dcc.Dropdown(
									value='400e-12',
									options=ChipSizeList,
									id="ID_ChipSIze",
									style={'width': '100%',
										   'textAlign': TEXT_POSITION
										   },
								),
							], className='twelve columns',
								#id='Resonant_Frequency_Input_Wrapper',
							),
						], className='row',
							style={"margin": "5px",
								   # 	   "padding": "5px",
								   },
						),


						###------------------
						html.Div([
							html.Div([
								html.Label('Target Frequency'),
							], className='twelve columns',
								style={'textAlign': 'left'},
							),
						],
						),
						html.Div([
							html.Div([
								dcc.Input(id='Resonant_Frequency_Input_ID',
										  value=100,
										  debounce=True,
										  style={'textAlign': TEXT_POSITION},
										  ),
								], className='seven columns',
							id='Resonant_Frequency_Input_Wrapper',
							),

							html.Div([
								dcc.Dropdown(
									value='1e6',
									options=UnitList,
									id="ID_UnitList",
									style={'width': '100%'},
								),
							],  className = 'five columns'
							),
						],className='row',
							style={"margin": "5px",
							# 	   "padding": "5px",
							 	   },
						),
						###-----------------
						###################
					],
					),
				], 	style={"border": "1px black dashed",
						   "margin": "5px",
						   "padding": "5px",
						   "borderRadius": "5px", },
				),


			], className='three columns',
				style={"border": "1px black solid",
					   "margin": "5px",
					   "padding": "5px",
					   "borderRadius": "5px",
					   },
				#id='IMP_Wrapper_Input',
			),
			## Graph View #################
			html.Div([
				######################
				html.H5("Frequency Domain View"),

				html.Div([
					dcc.Graph(
						id="ID_RESONANT_FREQUENCY_GRAPH",
						style={"display": "true",
							   'textAlign': 'center',
							   },
					),
				],
				),

				######################
			], className='nine columns',
				style={"border": "1px black solid",
					   "margin": "5px",
					   "padding": "5px",
					   "borderRadius": "5px",

					   },
			),
		], className='row',
			style={"margin": "5px",
				   "padding": "5px",
				   # 'height': '500px',
				   # 'width': "100%",
				   # 'overflow': 'auto'
				   },
		),

		#########
		html.Div([
			html.Div([
				html.Div(["Operation Log:"]),
				dcc.Interval(
					id='Converter_interval1',
					interval=1 * 1000,  # in milliseconds
					n_intervals=0,
				),
				html.Div([
					html.Iframe(id='Converter_console-out',
								srcDoc='',
								style=dict(height='300px',
										   width="100%",
										   overflow='auto')
								)
				], className='twelve',
				)
			], className='row',
				style={"border": "1px black solid",
					   "margin": "5px",
					   "padding": "5px",
					   "borderRadius": "5px",
					   },
			),
		],
			style={"margin": "5px",
				   "padding": "5px",
				   },
		),
	]
)