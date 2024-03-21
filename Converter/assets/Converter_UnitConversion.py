import dash
from dash import dcc
from dash import html

from dash import dash_table
import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../assets").resolve()
PAGE_SIZE=10000
TEXT_POSITION = 'center'

from ..UnitConversion import *


def create_layout(app):
    return html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H4("Search"),
						# html.Br([]),
						html.Div([
							html.Div([
								html.Label('Category'),
							],  # className = 'six columns'
							),
							html.Div([
								dcc.Dropdown(
									value='',
									options="",  # UnitConversion.CategoryList(),
									id="DD_UnitConversion_Category",
									style={'width': '100%'},
								),
							],  # className = 'six columns'
							),

							# html.Br([]),
							html.Div([
								html.Div([
									html.Label('From'),
								],#className = 'six columns'
								),
								html.Div([
								dcc.Dropdown(
									value='',
									options="",#UnitConversion.CategoryList(),
									id="DD_UnitConversion_From",
									style={'width': '100%'},
								),
							],#className = 'six columns'
							),
							],#className='row',
							),

							# html.Br([]),
							html.Div([
								html.Div([
								html.Label('To'),
							],# className='six columns'),
							),

								html.Div([
								dcc.Dropdown(
									value='',
									options="",
									id="DD_UnitConversion_To",
									style={'width': '100%'},
								),
							], #className='six columns'),
							),

							], #className='row'
							),
						],
						style={"border": "1px black dashed",
							   "margin": "5px",
							   "padding": "5px",
							   "borderRadius": "5px",
						},
						),

						html.Br([]),
						html.Div([
							html.Div([
								html.Label('Input Parameter'),
							],  # className = 'six columns'
							),

							html.Div([
								html.Div([
									html.Label("Param1",
										id='ID_Param_1_Name'),
								],  className = 'two columns',
									id='ID_Param_1_Name_Wrapper',
								),
								html.Div([
									html.Label("MIN:"),
								],  className = 'one columns',
								),
								html.Div([
									dcc.Input(id='ID_Param_1_MIN',
											  value="",
											  debounce=True,
											  style={'textAlign': TEXT_POSITION,
													 'width': '75%'},
											  ),
								], className='four columns',
									id='ID_Param_1_MIN_Wrapper',
								),
								html.Div([
									html.Label("MAX:"),
								],  className = 'one columns',
								),
								html.Div([
									dcc.Input(id='ID_Param_1_MAX',
											  # value=100,
											  debounce=True,
											  style={'textAlign': TEXT_POSITION,
													 'width': '75%'},
											  ),
								], className='four columns',
									id='ID_Param_1_MAX_Wrapper',
								),

							], className='row', ),
							html.Div([
								html.Div([
									html.Label("Param2",
											   id='ID_Param_2_Name'),
								], className='four columns',
									id='ID_Param_2_Name_Wrapper',
								),
								html.Div([
									dcc.Input(id='ID_Param_2',
											  debounce=True,
											  style={'textAlign': TEXT_POSITION,
													 'width': '75%'},
											  ),
								], className='eight columns',
									id='ID_Param_2_Wrapper',
								),

							], className='row', ),
							html.Div([
								html.Div([
									html.Label("Param3",
											   id='ID_Param_3_Name'),
								], className='four columns',
									id='ID_Param_3_Name_Wrapper',
								),
								html.Div([
									dcc.Input(id='ID_Param_3',
											  debounce=True,
											  style={'textAlign': TEXT_POSITION,
													 'width': '75%'},
											  ),
								], className='eight columns',
									id='ID_Param_3_Wrapper',
								),

							], className='row', ),
							html.Div([
								html.Div([
									html.Label("Param4",
											   id='ID_Param_4_Name'),
								], className='four columns',
									id='ID_Param_4_Name_Wrapper',
								),
								html.Div([
									dcc.Input(id='ID_Param_4',
											  debounce=True,
											  style={'textAlign': TEXT_POSITION,
													 'width': '75%'},
											  ),
								], className='eight columns',
									id='ID_Param_4_Wrapper',
								),

							], className='row', ),
							html.Div([
								html.Div([
									html.Label("Param5",
											   id='ID_Param_5_Name'),
								], className='four columns',
									id='ID_Param_5_Name_Wrapper',
								),
								html.Div([
									dcc.Input(id='ID_Param_5',
											  debounce=True,
											  style={'textAlign': TEXT_POSITION,
													 'width': '75%'},
											  ),
								], className='eight columns',
									id='ID_Param_5_Wrapper',
								),

							], className='row', ),
							html.Div([
								html.Div([
									html.Label("Param6",
											   id='ID_Param_6_Name'),
								], className='four columns',
									id='ID_Param_6_Name_Wrapper',
								),
								html.Div([
									dcc.Input(id='ID_Param_6',
											  debounce=True,
											  style={'textAlign': TEXT_POSITION,
													 'width': '75%'},
											  ),
								], className='eight columns',
									id='ID_Param_6_Wrapper',
								),

							], className='row', ),
							html.Div([
								html.Div([
									html.Label("Param7",
											   id='ID_Param_7_Name'),
								], className='four columns',
									id='ID_Param_7_Name_Wrapper',
								),
								html.Div([
									dcc.Input(id='ID_Param_7',
											  debounce=True,
											  style={'textAlign': TEXT_POSITION,
													 'width': '75%'},
											  ),
								], className='eight columns',
									id='ID_Param_7_Wrapper',
								),

							], className='row', ),
							html.Div([
								html.Div([
									html.Label("Param8",
											   id='ID_Param_8_Name'),
								], className='four columns',
									id='ID_Param_8_Name_Wrapper',
								),
								html.Div([
									dcc.Input(id='ID_Param_8',
											  debounce=True,
											  style={'textAlign': TEXT_POSITION,
													 'width': '75%'},
											  ),
								], className='eight columns',
									id='ID_Param_8_Wrapper',
								),

							], className='row', ),
						],
						style={"border": "1px black dashed",
							   "margin": "5px",
						       "padding": "5px",
						       "borderRadius": "5px",
						},
						),
					],
					),

				],className='five columns',),

				html.Div([
					html.H4("Formula"),
					dcc.Graph(
						id="id_UnitConversion_Formula",
						style={"display": "true",
								'textAlign': 'center',
							   # 'width': '95vw',
							   # 'height': '100vh',
								},
						mathjax=True,
					),
				], className='seven columns',
				),


			],className='row',
			style={"margin": "10px",
				   "padding": "10px",
				   "border": "1px black solid",
				   "borderRadius": "5px",
			},
			# style={"border":"1px black solid"},
		),

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
	])

