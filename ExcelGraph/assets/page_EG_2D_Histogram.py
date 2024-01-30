# import dash_html_components as html
# import dash_core_components as dcc
from dash import html
from dash import dcc

import pathlib

#get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../assets").resolve()

from ExcelGraph.EG_Functions import ColourTable, ColourTable_Dash

def create_layout(app):
	#return html.Div("Not Yet")
	return html.Div([
		###############################
		html.Div([
			html.Div([
				html.Div([
					html.Div([
						html.H5("Graph Gerenate"),
					],className='four columns'
					),

					html.Div([
						html.Button('Graph Generate', id='HT2D_BT_Graph_Generate', n_clicks=0),
					], className='four columns',
						style={"margin": "3px",
							"padding": "3px",
						   },
					),

					html.Div([
						html.Label(id='HT2D_BT_Graph_Generate_Status'),
					], className='four columns'
					),

				],className='row',
				)
			], className='six columns',
				style={"border": "1px black solid",
					   "margin": "5px",
					   "padding": "5px",
					   "borderRadius": "5px",
					   },
			),

			html.Div([
			], className='six columns',
			),
		], className='row',
			style={"margin": "5px",
				   "padding": "5px",
				   },
		),
		# html.Br([]),
		###############################
		html.Div([
			html.Div([
				html.H5("Input Parameters"),
				###################
				html.Div([
					html.Div([

						###------------------
						html.H6("X1 data"),
						html.Div([

							html.Div([
								html.Label('Data'),
							],className='one columns',
							),

							html.Div([
								html.Button('SET', id='HT2D_BT_X1_DATA_SET', n_clicks=0),
							], className='two columns',
							),

							html.Div([
								html.Button('CLEAR', id='HT2D_BT_X1_DATA_CLEAR', n_clicks=0),
							], className='two columns',
							),

							html.Div([
							], className='one columns',
								style={"margin": "5px",
									   "padding": "5px",
									   },
							),

							html.Div([
								dcc.Input(id='HT2D_BT_X1_DATA_INPUT'),
							], className='six columns',
							),
						],className='row',
							style={"margin": "5px",
								   "padding": "5px",
									},
						),
						###------------------
						html.Div([
							html.Div([
								html.Label('Name'),
							], className='one columns',
							),

							html.Div([
								html.Button('SET', id='HT2D_BT_X1_NAME_SET', n_clicks=0),
							], className='two columns',
							),

							html.Div([
								html.Button('CLEAR', id='HT2D_BT_X1_NAME_CLEAR', n_clicks=0),
							], className='two columns',
							),

							html.Div([
							], className='one columns',
								style={"margin": "5px",
									   "padding": "5px",
									   },
							),

							html.Div([
								dcc.Input(id='HT2D_BT_X1_NAME_INPUT'),
							], className='six columns',
							),
						], className='row',
							style={"margin": "5px",
								   "padding": "5px",
								   },
						),

						###------------------
						html.Div([
								html.Div([
									html.Label('Unit'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='HT2D_BT_X1_UNIT_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='HT2D_BT_X1_UNIT_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='HT2D_BT_X1_UNIT_INPUT'),
								], className='six columns',
								),
							], className='row',
							style={"margin": "5px",
								 "padding": "5px",
									},
						),
						###------------------
						html.Div([
							html.Div([
								html.Label('Font Color'),
							], className='four columns',
							),

							html.Div([
							], className='three columns',
								style={"margin": "5px",
									   "padding": "5px",
									   },
							),
							html.Div([
								dcc.Dropdown(
									value=ColourTable[2],
									options=ColourTable_Dash,
									id="HT2D_BT_X1_COLOUR",
									style={'width': '100%'},
								),
							], className='four columns',
							),

						], className='row',
							style={"margin": "5px",
								   "padding": "5px",
								   },
						)
						###################
					],
					style={"border": "1px black dashed",
						   "margin": "5px",
						   "padding": "5px",
						   "borderRadius": "5px",},
					),
				],),
				###################
				html.Div([
					html.Div([

						###------------------
						html.H6("X2 data"),
						html.Div([

							html.Div([
								html.Label('Data'),
							], className='one columns',
							),

							html.Div([
								html.Button('SET', id='HT2D_BT_X2_DATA_SET', n_clicks=0),
							], className='two columns',
							),

							html.Div([
								html.Button('CLEAR', id='HT2D_BT_X2_DATA_CLEAR', n_clicks=0),
							], className='two columns',
							),

							html.Div([
							], className='one columns',
								style={"margin": "5px",
									   "padding": "5px",
									   },
							),

							html.Div([
								dcc.Input(id='HT2D_BT_X2_DATA_INPUT'),
							], className='six columns',
							),
						], className='row',
							style={"margin": "5px",
								   "padding": "5px",
								   },
						),
						###------------------
						html.Div([
							html.Div([
								html.Label('Name'),
							], className='one columns',
							),

							html.Div([
								html.Button('SET', id='HT2D_BT_X2_NAME_SET', n_clicks=0),
							], className='two columns',
							),

							html.Div([
								html.Button('CLEAR', id='HT2D_BT_X2_NAME_CLEAR', n_clicks=0),
							], className='two columns',
							),

							html.Div([
							], className='one columns',
								style={"margin": "5px",
									   "padding": "5px",
									   },
							),

							html.Div([
								dcc.Input(id='HT2D_BT_X2_NAME_INPUT'),
							], className='six columns',
							),
						], className='row',
							style={"margin": "5px",
								   "padding": "5px",
								   },
						),

						###------------------
						html.Div([
							html.Div([
								html.Label('Unit'),
							], className='one columns',
							),

							html.Div([
								html.Button('SET', id='HT2D_BT_X2_UNIT_SET', n_clicks=0),
							], className='two columns',
							),

							html.Div([
								html.Button('CLEAR', id='HT2D_BT_X2_UNIT_CLEAR', n_clicks=0),
							], className='two columns',
							),

							html.Div([
							], className='one columns',
								style={"margin": "5px",
									   "padding": "5px",
									   },
							),

							html.Div([
								dcc.Input(id='HT2D_BT_X2_UNIT_INPUT'),
							], className='six columns',
							),
						], className='row',
							style={"margin": "5px",
								   "padding": "5px",
								   },
						),
						###------------------
						html.Div([
							html.Div([
								html.Label('Font Color'),
							], className='four columns',
							),

							html.Div([
							], className='three columns',
								style={"margin": "5px",
									   "padding": "5px",
									   },
							),
							html.Div([
								dcc.Dropdown(
									value=ColourTable[4],
									options=ColourTable_Dash,
									id="HT2D_BT_X2_COLOUR",
									style={'width': '100%'},
								),
							], className='four columns',
							),

						], className='row',
							style={"margin": "5px",
								   "padding": "5px",
								   },
						)
						###################
					],
						style={"border": "1px black dashed",
							   "margin": "5px",
							   "padding": "5px",
							   "borderRadius": "5px", },
					),
				], ),

			], className='six columns',
			style={"border": "1px black solid",
				   "margin": "5px",
				   "padding": "5px",
				   "borderRadius": "5px",
				   },
			),

			html.Div([
				######################
				html.H5("Limit Setting"),
				###-------------------
				html.Div([
					html.H6("X1 data"),
					html.Div([
						html.Div([
							html.Label('Upper Limit:'),
						], className='two columns',
						),

						html.Div([
							html.Button('SET', id='HT2D_BT_X1_UP_LIMIT_SET', n_clicks=0),
						], className='two columns',
						),

						html.Div([
							html.Button('CLEAR', id='HT2D_BT_X1_UP_LIMIT_CLEAR', n_clicks=0),
						], className='two columns',
						),

						html.Div([
						], className='one columns',
							style={"margin": "5px",
								   "padding": "5px",
								   },
						),

						html.Div([
							dcc.Input(id='HT2D_BT_X1_UP_LIMIT_INPUT'),
						], className='five columns',
						),
					], className='row',
						style={"margin": "5px",
							   "padding": "5px",
							   },
					),
					html.Div([
						html.Div([
							html.Label('Lower Limit:'),
						], className='two columns',
						),

						html.Div([
							html.Button('SET', id='HT2D_BT_X1_LOW_LIMIT_SET', n_clicks=0),
						], className='two columns',
						),

						html.Div([
							html.Button('CLEAR', id='HT2D_BT_X1_LOW_LIMIT_CLEAR', n_clicks=0),
						], className='two columns',
						),

						html.Div([
						], className='one columns',
							style={"margin": "5px",
								   "padding": "5px",
								   },
						),

						html.Div([
							dcc.Input(id='HT2D_BT_X1_LOW_LIMIT_INPUT'),
						], className='five columns',
						),
					], className='row',
						style={"margin": "5px",
							   "padding": "5px",
								},
					)

				],
					style={"border": "1px black dashed",
						   "margin": "5px",
						   "padding": "5px",
						   "borderRadius": "5px", },
				),
				###-------------------
				###-------------------
				html.Div([
					html.H6("X2 data"),
					html.Div([
						html.Div([
							html.Label('Upper Limit:'),
						], className='two columns',
						),

						html.Div([
							html.Button('SET', id='HT2D_BT_X2_UP_LIMIT_SET', n_clicks=0),
						], className='two columns',
						),

						html.Div([
							html.Button('CLEAR', id='HT2D_BT_X2_UP_LIMIT_CLEAR', n_clicks=0),
						], className='two columns',
						),

						html.Div([
						], className='one columns',
							style={"margin": "5px",
								   "padding": "5px",
								   },
						),

						html.Div([
							dcc.Input(id='HT2D_BT_X2_UP_LIMIT_INPUT'),
						], className='five columns',
						),
					], className='row',
						style={"margin": "5px",
							   "padding": "5px",
							   },
					),
					html.Div([
						html.Div([
							html.Label('Lower Limit:'),
						], className='two columns',
						),

						html.Div([
							html.Button('SET', id='HT2D_BT_X2_LOW_LIMIT_SET', n_clicks=0),
						], className='two columns',
						),

						html.Div([
							html.Button('CLEAR', id='HT2D_BT_X2_LOW_LIMIT_CLEAR', n_clicks=0),
						], className='two columns',
						),

						html.Div([
						], className='one columns',
							style={"margin": "5px",
								   "padding": "5px",
								   },
						),

						html.Div([
							dcc.Input(id='HT2D_BT_X2_LOW_LIMIT_INPUT'),
						], className='five columns',
						),
					], className='row',
						style={"margin": "5px",
							   "padding": "5px",
							   },
					)

				],
					style={"border": "1px black dashed",
						   "margin": "5px",
						   "padding": "5px",
						   "borderRadius": "5px", },
				),
				###-------------------

				######################
			], className='six columns',
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
		# html.Br([]),
		html.Div([
			html.Div([
				######################
				html.H5("Graph layout Setting"),
				html.Div([
					html.H6("Title"),
					html.Div([
						html.Div([
							html.Label('Text'),
						], className='two columns',
						),

						html.Div([
							html.Button('SET', id='HT2D_BT_TITLE_TEXT_SET', n_clicks=0),
						], className='two columns',
						),

						html.Div([
							html.Button('CLEAR', id='HT2D_BT_TITLE_TEXT_CLEAR', n_clicks=0),
						], className='two columns',
						),

						html.Div([
						], className='one columns',
							style={"margin": "5px",
								   "padding": "5px",
								   },
						),

						html.Div([
							dcc.Input(id='HT2D_BT_TITLE_TEXT_INPUT'),
						], className='five columns',
						),
					], className='row',
						style={"margin": "5px",
							   "padding": "5px",
							   },
					),
					html.Div([
						html.Div([
							html.Label('Font Size'),
						], className='two columns',
						),

						html.Div([
							html.Button('SET', id='HT2D_BT_TITLE_SIZE_SET', n_clicks=0),
						], className='two columns',
						),

						html.Div([
							html.Button('CLEAR', id='HT2D_BT_TITLE_SIZE_CLEAR', n_clicks=0),
						], className='two columns',
						),

						html.Div([
						], className='one columns',
							style={"margin": "5px",
								   "padding": "5px",
								   },
						),

						html.Div([
							dcc.Input(id='HT2D_BT_TITLE_SIZE_INPUT',value=10),
						], className='five columns',
						),
					], className='row',
						style={"margin": "5px",
							   "padding": "5px",
							   },
					),
					html.Div([
						html.Div([
							html.Label('Font Color'),
						], className='four columns',
						),

						html.Div([
						], className='three columns',
							style={"margin": "5px",
								   "padding": "5px",
								   },
						),
						html.Div([
							dcc.Dropdown(
								value='black',
								options=ColourTable_Dash,
								id="HT2D_BT_TITLE_COLOUR",
								style={'width': '100%'},
							),
						],className='four columns',
						),

					], className='row',
						style={"margin": "5px",
							   "padding": "5px",
							   },
					)



				],
					style={"border": "1px black dashed",
						   "margin": "5px",
						   "padding": "5px",
						   "borderRadius": "5px", },
				),
				######################
			], className='six columns',
				style={"border": "1px black solid",
					   "margin": "5px",
					   "padding": "5px",
					   "borderRadius": "5px",
					   },
			),
		],className='row',
			style={"margin": "5px",
				 "padding": "5px",
				},
		),

		#########
		html.Div([
			html.Div([
				html.Div(["Operation Log:"]),
				dcc.Interval(
					id='interval1',
					interval=1 * 1000,  # in milliseconds
					n_intervals=0,
				),
				html.Div([
					html.Iframe(id='HT2D_console-out',
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
	])