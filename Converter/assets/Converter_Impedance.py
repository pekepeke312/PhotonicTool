from dash import html
from dash import dcc
import pathlib
import Converter.Converter_Functions

#get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../assets").resolve()

TEXT_POSITION = 'center'

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
								html.H6('Impedance'),
							], className='five columns',
							),

							html.Div([
							], className='seven columns',
							),

						], className='row',
							# style={"margin": "5px",
							# 	   "padding": "5px",
							# 	   },
						),
						###------------------
						html.Div([
							html.Div([
								html.H6('Source'),
							], className='five columns',
								style={'textAlign': 'center'},
							),


							html.Div([
								dcc.Input(id='IMP_SOURCE_IMP_INPUT',
										  debounce=True,
										  value=50,
										  style={'textAlign': TEXT_POSITION,
												 #'width' : '20%'
												 },
										  ),
							], className='seven columns',
								id='IMP_SOURCE_IMP_INPUT_Wrapper',
							),


						], className='row',
							# style={"margin": "5px",
							# 	   "padding": "5px",
							# 	   },
						),
						###-----------------
						###------------------
						html.Div([
							html.Div([
								html.H6('Load'),
							], className='five columns',
								style={'textAlign': 'center'},
							),

							# html.Div([
							# ], className='one columns',
							# 	style={"margin": "5px",
							# 		   "padding": "5px",
							# 		   },
							# ),

							html.Div([
								dcc.Input(id='IMP_LOAD_IMP_INPUT',
										  value=50,
										  debounce=True,
										  style={'textAlign': TEXT_POSITION},
										  ),
							], className='seven columns',
							id='IMP_LOAD_IMPL_INPUT_Wrapper',
							),
						], className='row',
							style={"margin": "5px",
								   "padding": "5px",
								   },
						),
						###-----------------
						###################
					],
						style={"border": "1px black dashed",
							   "margin": "5px",
							   "padding": "5px",
							   "borderRadius": "5px", },
					),
				], ),
				###################
				###################
				html.Div([
					html.Div([
						###------------------
						##//////////////////
						html.Div([

							html.Div([
								html.H6('|VSWR|'),
							], className='two columns',
							),

							html.Div([
								dcc.Input(id='ID_IMP_VSWR_ABS',
										  debounce=True,
										  style={'textAlign': TEXT_POSITION,
												 'width': '75%'},
										  ),
							], className='four columns',
								id='ID_IMP_VSWR_ABS_Wrapper',
							),

							html.Div([
								html.H6('VSWR'),
							], className='two columns',
							),

							html.Div([
								dcc.Input(id='ID_IMP_VSWR',
										  debounce=True,
										  style={'textAlign': TEXT_POSITION,
												 'width': '100%'},
										  ),
							], className='four columns',
								id='ID_IMP_VSWR_Wrapper',
							),

						##////////////////////
						], className='row',
							style={"margin": "5px",
								   "padding": "5px",
								   },
						),
						###-----------------
						###------------------
						html.Div([
							html.Div([
								html.H6('|Γ|'),
							], className='two columns',
							),

							html.Div([
								dcc.Input(id='ID_IMP_GAMMA_ABS',
										  debounce=True,
										  style={'textAlign': TEXT_POSITION,
												 'width': '75%',
												 },
										  ),
							], className='four columns',
								id='ID_IMP_GAMMA_ABS_Wrapper',
							),


							html.Div([
								html.H6('Γ'),
							], className='two columns',
							),

							html.Div([
								dcc.Input(id='ID_IMP_GAMMA',
										  debounce=True,
										  style={'textAlign': TEXT_POSITION,
												 'width': '100%',
												 },
										  ),
							], className='four columns',
								id='ID_IMP_GAMMA_Wrapper',
							),

						], className='row',
							style={"margin": "5px",
								   "padding": "5px",
								   },
						),
						###-----------------
						###------------------
						html.Div([
							html.Div([
								html.H6('Return Loss'),
							], className='five columns',
							),


							html.Div([
								dcc.Input(id='ID_IMP_RL',
										  debounce=True,
										  style={'textAlign': TEXT_POSITION},
										  ),
							], className='six columns',
								id='ID_IMP_RL_Wrapper',
							),

							html.Div([
								html.H6('[dB]')
							], className='one columns',
								style={'textAlign': 'left'},
							),
						], className='row',
							style={"margin": "5px",
								   "padding": "5px",
								   },
						),
						###-----------------
						###------------------
						html.Div([
							html.Div([
								html.H6('Matching Loss'),
							], className='five columns',
							),

							html.Div([
								dcc.Input(id='ID_IMP_ML_DB',
										  debounce=True,
										  style={'textAlign': TEXT_POSITION},
										  ),
							], className='six columns',
								id='ID_IMP_ML_DB_Wrapper',
							),
							html.Div([
								html.H6('[dB]')
							], className='one columns',
							style={'textAlign': 'left'},
							),

						], className='row',
							style={"margin": "5px",
								   "padding": "5px",
								   },
						),
						###-----------------
						###------------------
						html.Div([
							html.Div([
								html.H6('Matching Loss'),
							], className='five columns',
							),

							html.Div([
								dcc.Input(id='ID_IMP_ML_PC',
										  debounce=True,
										  style={'textAlign': TEXT_POSITION},
										  ),
							], className='six columns',
								id='ID_IMP_ML_PC_Wrapper',
							),
							html.Div([
								html.H6('[%]')
							], className='one columns',
								style={'textAlign': 'left'},
							),

						], className='row',
							style={"margin": "5px",
								   "padding": "5px",
								   },
						),
						###-----------------
						###################
					],
						style={"border": "1px black dashed",
							   "margin": "5px",
							   "padding": "5px",
							   "borderRadius": "5px", },
					),
				], ),
				###################

			], className='five columns',
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
				html.H5("Smith View"),
				###-------------------
				html.Div([
					###------------------
					html.Div([
						html.Div([
							html.H6('Characteristic Impedance'),
						], className='five columns',
							style={'textAlign': 'left'},
						),

						html.Div([
							dcc.Input(id='IMP_CHARAC_IMP_INPUT',
									  value=50,
									  debounce=True,
									  style={'textAlign': TEXT_POSITION},
									  ),
						], className='five columns',
						),

						html.Div([
							html.H6('[\u03A9]')
						], className='two columns',
							style={'textAlign': 'left'},
						),

					], className='row',
						# style={"margin": "5px",
						# 	   "padding": "5px",
						# 	   },
					),
					###-----------------
				],
					style={"border": "1px black dashed",
						   "margin": "5px",
						   "padding": "5px",
						   "borderRadius": "5px", },
				),
				###-------------------

				html.Div([
					dcc.Graph(
						id="ID_IMP_SMITH_GRAPH",
						style={"display": "true",
							   'textAlign': 'center',
							   },
					),
				],
				),

				######################
			], className='seven columns',
				style={"border": "1px black solid",
					   "margin": "5px",
					   "padding": "5px",
					   "borderRadius": "5px",
					   },
			),
		], className='row',
			style={"margin": "5px",
				   "padding": "5px",
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