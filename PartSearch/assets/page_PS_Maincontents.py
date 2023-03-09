import dash
from dash import dcc
from dash import html

from dash import dash_table
import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../assets").resolve()
PAGE_SIZE=10000

from PartSearch.PartSearch_Functions import *


def create_layout(app):
	return html.Div([
		html.Div([
			html.Div([
					html.Div([
						html.H4("Search"),
						# html.Br([]),
						html.Div([
							html.Div([
								html.Label('Sheet Names'),
							],#className = 'six columns'
							),

							html.Div([
								dcc.Dropdown(
									value='All',
									#options= will be updated by callback,
									id="id_DD_SheetNames",
									style={'width': '100%'},
								),
							],#className = 'six columns'
							),
						],#className='row',
						),
					],className = 'six columns'),
					html.Div([
						html.H4("Export"),
						#html.Br([]),
						html.Div([
							html.Div(children="Click if you want to export Searched Result Table"),
							html.Button('Download Table with CSV', id='PS_btn_Export_Table'),
							dcc.Download(id='PS_download_dataframe_csv'),
						]),
						html.Br([]),
						html.Br([]),
					],className = 'six columns',
					),

			],className='row',
			),

			html.Div([
				#html.Center(html.H6("Searched Result Table", )),
				html.P(id='Table_Selected_Out'),
				dash_table.DataTable(
					id='PS_table-paging-and-sorting',
					columns="",
					page_current=0,
					page_size=PAGE_SIZE,
					editable=True,
					page_action='native',
					filter_action='native',
					filter_options={
						'case': 'insensitive',
					},

					sort_action='custom',
					sort_mode='single',
					sort_by=[],
					style_cell={
						'font_family': "Open Sans",
						'font_size': '15px',
						'text_align': 'center',
					},
				),
			], className='twelve columns'),

		], className='row'
		),

		html.Div([
			html.Div([
				html.Div(["Operation Log:"]),
				dcc.Interval(
					id='interval_PS',
					interval=1 * 1000, # in milliseconds
					n_intervals=0,
				),
				html.Div([
					html.Iframe(id='PS_console-out',
								srcDoc='',
								style=dict(height='300px',
											width="100%",
											overflow='auto')
					)
				],className='twelve',
				)
			],className= 'row',
			style = {"border": "1px black solid"},
			),
		]),
	]
	)


