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
	return html.Div([
		###############################

		html.Div([
			html.Div([
				html.Div([
					html.Div([
						html.H5("Graph Gerenate"),
					], className='four columns'
					),

					html.Div([
						html.Button('Graph Generate', id='SC_BT_Graph_Generate', n_clicks=0),
					], className='four columns',
						style={"margin": "3px",
							   "padding": "3px",
							   },
					),

					html.Div([
						html.Label(id='SC_BT_Graph_Generate_Status'),
					], className='four columns'
					),

				], className='row',
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
		###############################

		##-----------------------------
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
							html.Button('SET', id='SC_BT_TITLE_TEXT_SET', n_clicks=0),
						], className='two columns',
						),

						html.Div([
							html.Button('CLEAR', id='SC_BT_TITLE_TEXT_CLEAR', n_clicks=0),
						], className='two columns',
						),

						html.Div([
						], className='one columns',
							style={"margin": "5px",
								   "padding": "7px",
								   },
						),

						html.Div([
							dcc.Input(id='SC_BT_TITLE_TEXT_INPUT'),
						], className='five columns',
						),
					], className='row',
						style={"margin": "5px",
							   "padding": "7px",
							   },
					),
					html.Div([
						html.Div([
							html.Label('Font Size'),
						], className='two columns',
						),

						html.Div([
							html.Button('SET', id='SC_BT_TITLE_SIZE_SET', n_clicks=0),
						], className='two columns',
						),

						html.Div([
							html.Button('CLEAR', id='SC_BT_TITLE_SIZE_CLEAR', n_clicks=0),
						], className='two columns',
						),

						html.Div([
						], className='one columns',
							style={"margin": "5px",
								   "padding": "7px",
								   },
						),

						html.Div([
							dcc.Input(id='SC_BT_TITLE_SIZE_INPUT', value=10),
						], className='five columns',
						),
					], className='row',
						style={"margin": "5px",
							   "padding": "7px",
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
								id="SC_BT_TITLE_COLOUR",
								style={'width': '100%'},
							),
						], className='four columns',
						),

					], className='row',
						style={"margin": "5px",
							   "padding": "7px",
							   },
					)

				],
					style={"border": "1px black dashed",
						   "margin": "5px",
						   "padding": "5px",
						   "borderRadius": "5px", },
				),
				html.Div([
					html.H6("Scale"),
					html.Div([
						html.Div([
							html.Label('Horizontal'),
						], className='two columns',
						),

						html.Div([
							dcc.Dropdown(
								value='Linear',
								options=[
											{'label': 'Linear', 'value': 'Linear'},
											{'label': 'Log', 'value': 'Log'},
										],
								id="SC_BT_Graph_Scale_Horizontal",
								style={'width': '100%'},
							),
						], className='four columns',
						),

						html.Div([
							html.Label('Vertical'),
						], className='two columns',
						),

						html.Div([
							dcc.Dropdown(
								value='Linear',
								options=[
									{'label': 'Linear', 'value': 'Linear'},
									{'label': 'Log', 'value': 'Log'},
								],
								id="SC_BT_Graph_Scale_Vertical",
								style={'width': '100%'},
							),
						], className='four columns',
						),


					], className='row',
						style={"margin": "5px",
							   "padding": "7px",
							   },
					),

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

			html.Div([
				######################
				html.H5("View Range"),
				###-------------------
				html.Div([
					#html.H6("X1 data"),
					html.Div([
						html.Div([
							html.Label('X Upper Limit:'),
						], className='two columns',
						),

						html.Div([
							html.Button('SET', id='SC_BT_X1_UP_VIEW_SET', n_clicks=0),
						], className='two columns',
						),

						html.Div([
							html.Button('CLEAR', id='SC_BT_X1_UP_VIEW_CLEAR', n_clicks=0),
						], className='two columns',
						),

						html.Div([
						], className='one columns',
							style={"margin": "5px",
								   "padding": "1px",
								   },
						),

						html.Div([
							dcc.Input(id='SC_BT_X1_UP_VIEW_INPUT'),
						], className='five columns',
						),
					], className='row',
						style={"margin": "5px",
							   "padding": "1px",
							   },
					),
					html.Div([
						html.Div([
							html.Label('X Lower Limit:'),
						], className='two columns',
						),

						html.Div([
							html.Button('SET', id='SC_BT_X1_LOW_VIEW_SET', n_clicks=0),
						], className='two columns',
						),

						html.Div([
							html.Button('CLEAR', id='SC_BT_X1_LOW_VIEW_CLEAR', n_clicks=0),
						], className='two columns',
						),

						html.Div([
						], className='one columns',
							style={"margin": "5px",
								   "padding": "1px",
								   },
						),

						html.Div([
							dcc.Input(id='SC_BT_X1_LOW_VIEW_INPUT'),
						], className='five columns',
						),
					], className='row',
						style={"margin": "5px",
							   "padding": "1px",
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
					#html.H6("X2 data"),
					html.Div([
						html.Div([
							html.Label('Y Upper Limit:'),
						], className='two columns',
						),

						html.Div([
							html.Button('SET', id='SC_BT_Y_UP_VIEW_SET', n_clicks=0),
						], className='two columns',
						),

						html.Div([
							html.Button('CLEAR', id='SC_BT_Y_UP_VIEW_CLEAR', n_clicks=0),
						], className='two columns',
						),

						html.Div([
						], className='one columns',
							style={"margin": "5px",
								   "padding": "1px",
								   },
						),

						html.Div([
							dcc.Input(id='SC_BT_Y_UP_VIEW_INPUT'),
						], className='five columns',
						),
					], className='row',
						style={"margin": "5px",
							   "padding": "1px",
							   },
					),
					html.Div([
						html.Div([
							html.Label('Y Lower Limit:'),
						], className='two columns',
						),

						html.Div([
							html.Button('SET', id='SC_BT_Y_LOW_VIEW_SET', n_clicks=0),
						], className='two columns',
						),

						html.Div([
							html.Button('CLEAR', id='SC_BT_Y_LOW_VIEW_CLEAR', n_clicks=0),
						], className='two columns',
						),

						html.Div([
						], className='one columns',
							style={"margin": "5px",
								   "padding": "1px",
								   },
						),

						html.Div([
							dcc.Input(id='SC_BT_Y_LOW_VIEW_INPUT'),
						], className='five columns',
						),
					], className='row',
						style={"margin": "5px",
							   "padding": "1px",
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
		##-----------------------------

		##*****************************
		html.Div([
			html.Div([
				html.Div([
					html.H5("Horizontal Data"),
					###################
					html.Div([
						html.Div([

							###------------------
							html.H6("X1 data"),
							html.Div([

								html.Div([
									html.Label('Data'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_X1_DATA_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X1_DATA_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X1_DATA_INPUT'),
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
									html.Button('SET', id='SC_BT_X1_NAME_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X1_NAME_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X1_NAME_INPUT'),
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
									html.Button('SET', id='SC_BT_X1_UNIT_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X1_UNIT_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X1_UNIT_INPUT'),
								], className='six columns',
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
					], ), #X1
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
									html.Button('SET', id='SC_BT_X2_DATA_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X2_DATA_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X2_DATA_INPUT'),
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
									html.Button('SET', id='SC_BT_X2_NAME_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X2_NAME_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X2_NAME_INPUT'),
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
									html.Button('SET', id='SC_BT_X2_UNIT_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X2_UNIT_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X2_UNIT_INPUT'),
								], className='six columns',
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
					], ), #X2
					###################
					html.Div([
						html.Div([

							###------------------
							html.H6("X3 data"),
							html.Div([

								html.Div([
									html.Label('Data'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_X3_DATA_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X3_DATA_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X3_DATA_INPUT'),
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
									html.Button('SET', id='SC_BT_X3_NAME_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X3_NAME_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X3_NAME_INPUT'),
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
									html.Button('SET', id='SC_BT_X3_UNIT_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X3_UNIT_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X3_UNIT_INPUT'),
								], className='six columns',
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
					], ),  # X3
					###################
					html.Div([
						html.Div([
							###------------------
							html.H6("X4 data"),
							html.Div([

								html.Div([
									html.Label('Data'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_X4_DATA_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X4_DATA_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X4_DATA_INPUT'),
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
									html.Button('SET', id='SC_BT_X4_NAME_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X4_NAME_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X4_NAME_INPUT'),
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
									html.Button('SET', id='SC_BT_X4_UNIT_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X4_UNIT_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X4_UNIT_INPUT'),
								], className='six columns',
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
					], ),  # X4
					###################
					html.Div([
						html.Div([
							###------------------
							html.H6("X5 data"),
							html.Div([

								html.Div([
									html.Label('Data'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_X5_DATA_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X5_DATA_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X5_DATA_INPUT'),
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
									html.Button('SET', id='SC_BT_X5_NAME_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X5_NAME_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X5_NAME_INPUT'),
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
									html.Button('SET', id='SC_BT_X5_UNIT_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X5_UNIT_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X5_UNIT_INPUT'),
								], className='six columns',
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
					], ),  # X5
					###################
					html.Div([
						html.Div([
							###------------------
							html.H6("X6 data"),
							html.Div([

								html.Div([
									html.Label('Data'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_X6_DATA_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X6_DATA_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X6_DATA_INPUT'),
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
									html.Button('SET', id='SC_BT_X6_NAME_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X6_NAME_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X6_NAME_INPUT'),
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
									html.Button('SET', id='SC_BT_X6_UNIT_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X6_UNIT_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X6_UNIT_INPUT'),
								], className='six columns',
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
					], ),  # X6
					###################
					html.Div([
						html.Div([
							###------------------
							html.H6("X7 data"),
							html.Div([

								html.Div([
									html.Label('Data'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_X7_DATA_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X7_DATA_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X7_DATA_INPUT'),
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
									html.Button('SET', id='SC_BT_X7_NAME_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X7_NAME_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X7_NAME_INPUT'),
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
									html.Button('SET', id='SC_BT_X7_UNIT_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_X7_UNIT_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_X7_UNIT_INPUT'),
								], className='six columns',
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
					], ),  # X7
					###################

				],
					className='six columns',
					style={"margin": "5px",
						   "padding": "5px",
						   },
				),

				html.Div([
					html.H5("Vertical Data"),
					###################
					html.Div([
						html.Div([

							###------------------
							#html.H6("Y1 data"),
							html.Div([

								html.Div([
									html.Label('Data'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y1_DATA_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y1_DATA_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y1_DATA_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),
							###------------------
							html.Div([
								html.Div([
									html.Label('Name'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y1_NAME_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y1_NAME_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y1_NAME_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),

							###------------------
							html.Div([
								html.Div([
									html.Label('Unit'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y1_UNIT_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y1_UNIT_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y1_UNIT_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),
							html.Div([
								html.Div([
									html.Label('Color'),
								], className='four columns',
								),

								html.Div([
								], className='two columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),
								html.Div([
									dcc.Dropdown(
										value=ColourTable[0],
										options=ColourTable_Dash,
										id="SC_Y1_COLOUR",
										style={'width': '100%'},
									),
								], className='four columns',
								),

							], className='row',
								style={"margin": "5px",
									   "padding": "3.5px",
									   },
							),
							###################
						],
							style={"border": "1px black dashed",
								   "margin": "5px",
								   "padding": "5px",
								   "borderRadius": "5px", },
						),
					], ), #Y1
					###################
					html.Div([
						html.Div([

							###------------------
							#html.H6("Y2 data"),
							html.Div([

								html.Div([
									html.Label('Data'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y2_DATA_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y2_DATA_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y2_DATA_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),
							###------------------
							html.Div([
								html.Div([
									html.Label('Name'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y2_NAME_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y2_NAME_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y2_NAME_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),

							###------------------
							html.Div([
								html.Div([
									html.Label('Unit'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y2_UNIT_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y2_UNIT_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y2_UNIT_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),
							html.Div([
								html.Div([
									html.Label('Color'),
								], className='four columns',
								),

								html.Div([
								], className='two columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),
								html.Div([
									dcc.Dropdown(
										value=ColourTable[1],
										options=ColourTable_Dash,
										id="SC_Y2_COLOUR",
										style={'width': '100%'},
									),
								], className='four columns',
								),

							], className='row',
								style={"margin": "5px",
									   "padding": "3.5px",
									   },
							),
							###################
						],
							style={"border": "1px black dashed",
								   "margin": "5px",
								   "padding": "5px",
								   "borderRadius": "5px", },
						),
					], ), #Y2
					###################
					html.Div([
						html.Div([
							###------------------
							# html.H6("Y3 data"),
							html.Div([

								html.Div([
									html.Label('Data'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y3_DATA_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y3_DATA_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y3_DATA_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),
							###------------------
							html.Div([
								html.Div([
									html.Label('Name'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y3_NAME_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y3_NAME_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y3_NAME_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),

							###------------------
							html.Div([
								html.Div([
									html.Label('Unit'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y3_UNIT_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y3_UNIT_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y3_UNIT_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),
							html.Div([
								html.Div([
									html.Label('Color'),
								], className='four columns',
								),

								html.Div([
								], className='two columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),
								html.Div([
									dcc.Dropdown(
										value=ColourTable[2],
										options=ColourTable_Dash,
										id="SC_Y3_COLOUR",
										style={'width': '100%'},
									),
								], className='four columns',
								),

							], className='row',
								style={"margin": "5px",
									   "padding": "3.5px",
									   },
							),
							###################
						],
							style={"border": "1px black dashed",
								   "margin": "5px",
								   "padding": "5px",
								   "borderRadius": "5px", },
						),
					], ), #Y3
					###################
					html.Div([
						html.Div([
							###------------------
							# html.H6("Y4 data"),
							html.Div([

								html.Div([
									html.Label('Data'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y4_DATA_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y4_DATA_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y4_DATA_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),
							###------------------
							html.Div([
								html.Div([
									html.Label('Name'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y4_NAME_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y4_NAME_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y4_NAME_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),

							###------------------
							html.Div([
								html.Div([
									html.Label('Unit'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y4_UNIT_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y4_UNIT_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y4_UNIT_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),
							html.Div([
								html.Div([
									html.Label('Color'),
								], className='four columns',
								),

								html.Div([
								], className='two columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),
								html.Div([
									dcc.Dropdown(
										value=ColourTable[3],
										options=ColourTable_Dash,
										id="SC_Y4_COLOUR",
										style={'width': '100%'},
									),
								], className='four columns',
								),

							], className='row',
								style={"margin": "5px",
									   "padding": "3.5px",
									   },
							),
							###################
						],
							style={"border": "1px black dashed",
								   "margin": "5px",
								   "padding": "5px",
								   "borderRadius": "5px", },
						),
					], ),  # Y4
					###################
					html.Div([
						html.Div([
							###------------------
							# html.H6("Y5 data"),
							html.Div([

								html.Div([
									html.Label('Data'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y5_DATA_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y5_DATA_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y5_DATA_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),
							###------------------
							html.Div([
								html.Div([
									html.Label('Name'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y5_NAME_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y5_NAME_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y5_NAME_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),

							###------------------
							html.Div([
								html.Div([
									html.Label('Unit'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y5_UNIT_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y5_UNIT_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y5_UNIT_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),
							html.Div([
								html.Div([
									html.Label('Color'),
								], className='four columns',
								),

								html.Div([
								], className='two columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),
								html.Div([
									dcc.Dropdown(
										value=ColourTable[4],
										options=ColourTable_Dash,
										id="SC_Y5_COLOUR",
										style={'width': '100%'},
									),
								], className='four columns',
								),

							], className='row',
								style={"margin": "5px",
									   "padding": "3.5px",
									   },
							),
							###################
						],
							style={"border": "1px black dashed",
								   "margin": "5px",
								   "padding": "5px",
								   "borderRadius": "5px", },
						),
					], ),  # Y5
					###################
					html.Div([
						html.Div([
							###------------------
							# html.H6("Y6 data"),
							html.Div([

								html.Div([
									html.Label('Data'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y6_DATA_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y6_DATA_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y6_DATA_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),
							###------------------
							html.Div([
								html.Div([
									html.Label('Name'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y6_NAME_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y6_NAME_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y6_NAME_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),

							###------------------
							html.Div([
								html.Div([
									html.Label('Unit'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y6_UNIT_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y6_UNIT_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y6_UNIT_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),
							html.Div([
								html.Div([
									html.Label('Color'),
								], className='four columns',
								),

								html.Div([
								], className='two columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),
								html.Div([
									dcc.Dropdown(
										value=ColourTable[5],
										options=ColourTable_Dash,
										id="SC_Y6_COLOUR",
										style={'width': '100%'},
									),
								], className='four columns',
								),

							], className='row',
								style={"margin": "5px",
									   "padding": "3.5px",
									   },
							),
							###################
						],
							style={"border": "1px black dashed",
								   "margin": "5px",
								   "padding": "5px",
								   "borderRadius": "5px", },
						),
					], ),  # Y6
					###################
					html.Div([
						html.Div([
							###------------------
							# html.H6("Y7 data"),
							html.Div([

								html.Div([
									html.Label('Data'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y7_DATA_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y7_DATA_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y7_DATA_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),
							###------------------
							html.Div([
								html.Div([
									html.Label('Name'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y7_NAME_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y7_NAME_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y7_NAME_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),

							###------------------
							html.Div([
								html.Div([
									html.Label('Unit'),
								], className='one columns',
								),

								html.Div([
									html.Button('SET', id='SC_BT_Y7_UNIT_SET', n_clicks=0),
								], className='two columns',
								),

								html.Div([
									html.Button('CLEAR', id='SC_BT_Y7_UNIT_CLEAR', n_clicks=0),
								], className='two columns',
								),

								html.Div([
								], className='one columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),

								html.Div([
									dcc.Input(id='SC_BT_Y7_UNIT_INPUT'),
								], className='six columns',
								),
							], className='row',
								style={"margin": "5px",
									   "padding": "4px",
									   },
							),
							html.Div([
								html.Div([
									html.Label('Color'),
								], className='four columns',
								),

								html.Div([
								], className='two columns',
									style={"margin": "5px",
										   "padding": "5px",
										   },
								),
								html.Div([
									dcc.Dropdown(
										value=ColourTable[6],
										options=ColourTable_Dash,
										id="SC_Y7_COLOUR",
										style={'width': '100%'},
									),
								], className='four columns',
								),

							], className='row',
								style={"margin": "5px",
									   "padding": "3.5px",
									   },
							),
							###################
						],
							style={"border": "1px black dashed",
								   "margin": "5px",
								   "padding": "5px",
								   "borderRadius": "5px", },
						),
					], ),  # Y7
					###################
				],
					className='six columns',
					style={"margin": "5px",
						   "padding": "5px",
						   },
				),

			],className='row',
			),
		],
			style={"border": "1px black solid",
				   "margin": "5px",
				   "padding": "5px",
				   "borderRadius": "5px",
				   },
		),
		##*****************************
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
					html.Iframe(id='SC_console-out',
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