from dash import html
from dash import dcc
import pathlib
import base64
import Converter.Converter_Functions

from Converter.assets.PCB_Material_List import PCB_Material_List

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

########################################################################
tabs_styles = {
    'height': '80px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px',
    'height': '80px'
}
##########################################################################

Microstrip_path = "Converter/assets/ImageData/Microstrip.png"
Microstrip_image = base64.b64encode(open(Microstrip_path, "rb").read()).decode()

Stripline_path = "Converter/assets/ImageData/Stripline.png"
Stripline_image = base64.b64encode(open(Stripline_path, "rb").read()).decode()

Embedded_Microstrip_path = "Converter/assets/ImageData/Embedded Microstrip.png"
Embedded_Microstrip_image = base64.b64encode(open(Embedded_Microstrip_path, "rb").read()).decode()

Edge_Coupled_Microstrip_path = "Converter/assets/ImageData/Edge Coupled Microstrip.png"
Edge_Coupled_Microstrip_image = base64.b64encode(open(Edge_Coupled_Microstrip_path, "rb").read()).decode()

Edge_Coupled_Stripline_path = "Converter/assets/ImageData/Edge Coupled Stripline.png"
Edge_Coupled_Stripline_image = base64.b64encode(open(Edge_Coupled_Stripline_path, "rb").read()).decode()

Asymmetric_Stripline_path = "Converter/assets/ImageData/Asymmetric Stripline.png"
Asymmetric_Stripline_image = base64.b64encode(open(Asymmetric_Stripline_path, "rb").read()).decode()

Broadside_Coupled_Stripline_path = "Converter/assets/ImageData/Broadside Coupled Stripline.png"
Broadside_Coupled_Stripline_image = base64.b64encode(open(Broadside_Coupled_Stripline_path, "rb").read()).decode()

Coplaner_Waveguide_With_Ground_path = "Converter/assets/ImageData/Coplanar Waveguide With Ground.png"
Coplaner_Waveguide_With_Ground_image = base64.b64encode(open(Coplaner_Waveguide_With_Ground_path, "rb").read()).decode()

Asymmetric_Coplanar_Waveguide_path = "Converter/assets/ImageData/Asymmetric CPW.png"
Asymmetric_Coplanar_Waveguide_image = base64.b64encode(open(Asymmetric_Coplanar_Waveguide_path, "rb").read()).decode()

def pcb_pattern_impedance_tab_menu():
    menu = html.Div(
        [
            dcc.Tabs(id='Variation_tabs-selection',
                     # render_mode="hidden",
                     value='Microstrip',
                     children=[
                         dcc.Tab(label='Microstrip', value='Microstrip', className=tab_style,
                                 selected_style=tab_selected_style, ),

                         dcc.Tab(label='Stripline', value='Stripline', style=tab_style,
                                 selected_style=tab_selected_style),
                         dcc.Tab(label='Asymmetric Stripline', value='Asymmetric Stripline', style=tab_style,
                                 selected_style=tab_selected_style),
                         dcc.Tab(label='Embedded Microstrip', value='Embedded Microstrip', style=tab_style,
                                 selected_style=tab_selected_style),
                         dcc.Tab(label='Edge Coupled Microstrip', value='Edge Coupled Microstrip', style=tab_style,
                                 selected_style=tab_selected_style),
                         dcc.Tab(label='Edge Coupled Stripline', value='Edge Coupled Stripline', style=tab_style,
                                 selected_style=tab_selected_style),
                         dcc.Tab(label='Broadside Coupled Stripline', value='Broadside Coupled Stripline',
                                 style=tab_style, selected_style=tab_selected_style),
                         dcc.Tab(label="Coplanar Waveguide With Ground", value="Coplanar Waveguide With Ground",
                                 style=tab_style, selected_style=tab_selected_style),
                         dcc.Tab(label="Asymmetric Coplanar Waveguide", value="Asymmetric Coplanar Waveguide",
                                 style=tab_style, selected_style=tab_selected_style),
                     ],
                     className='custom-tabs',
                     style=tabs_styles,
                     ),

            html.Div([
                html.Div([
                    html.Img(src=f"data:image/png;base64,{Microstrip_image}", style={'width': '100%', 'height': 'auto'})
                ], style={'border': '1px solid #ccc'}),
                html.Div([
                    html.Img(src=f"data:image/png;base64,{Stripline_image}", style={'width': '100%', 'height': 'auto'})
                ], style={'border': '1px solid #ccc'}),
                html.Div([
                    html.Img(src=f"data:image/png;base64,{Asymmetric_Stripline_image}",
                             style={'width': '100%', 'height': 'auto'})
                ], style={'border': '1px solid #ccc'}),
                html.Div([
                    html.Img(src=f"data:image/png;base64,{Embedded_Microstrip_image}", style={'width': '100%', 'height': 'auto'})
                ], style={'border': '1px solid #ccc'}),
                html.Div([
                    html.Img(src=f"data:image/png;base64,{Edge_Coupled_Microstrip_image}", style={'width': '100%', 'height': 'auto'})
                ], style={'border': '1px solid #ccc'}),
                html.Div([
                    html.Img(src=f"data:image/png;base64,{Edge_Coupled_Stripline_image}", style={'width': '100%', 'height': 'auto'})
                ], style={'border': '1px solid #ccc'}),
                html.Div([
                    html.Img(src=f"data:image/png;base64,{Broadside_Coupled_Stripline_image}",
                             style={'width': '100%', 'height': 'auto'})
                ], style={'border': '1px solid #ccc'}),
                html.Div([
                    html.Img(src=f"data:image/png;base64,{Coplaner_Waveguide_With_Ground_image}",
                             style={'width': '100%', 'height': 'auto'})
                ], style={'border': '1px solid #ccc'}),
                html.Div([
                        html.Img(src=f"data:image/png;base64,{Asymmetric_Coplanar_Waveguide_image}",
                             style={'width': '100%', 'height': 'auto'})
                ], style={'border': '1px solid #ccc'}),


            ], style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(9, 1fr)',  # 9 等分のグリッド
                'gap': '0px',
                'width': '100%'
            }),

        ],
        className="row all-tabs",
    )
    return menu

def create_layout(app):
    return html.Div([
        html.Br([]),
		pcb_pattern_impedance_tab_menu(),
        html.Br([]),

        html.Div([
            html.Div([html.H5("Graph"),],
                     className='six columns',
                     id="ID_PCB_Pattern_Graph",
                     ),
            html.Div([html.H5("Formula"),],
                     className='six columns',
                     id="ID_PCB_Pattern_Formula",
                     ),
            ],className='row',
                style={"margin": "5px",
                    "padding": "5px",
                },
        ),

        html.Br([]),
        html.Div([
            html.Div([
            html.Div([
                html.Div([
                    html.H5('Input Parameter'),
                ],  # className = 'six columns'
                ),

                html.Div([
                    html.Div([
                        html.Label("Width (W)",
                                   id='ID_PCB_Param_0_Name'),
                    ], className='three columns',
                        id='ID_PCB_Param_0_Name_Wrapper',
                    ),
                    html.Div([
                        html.Label("MIN:"),
                    ], className='one columns',
                    ),
                    html.Div([
                        dcc.Input(id='ID_PCB_Param_0_MIN',
                                  value="0.01",
                                  debounce=True,
                                  style={'textAlign': TEXT_POSITION,
                                         'width': '100%'},
                                  ),
                    ], className='two columns',
                        id='ID_PCB_Param_0_MIN_Wrapper',
                    ),
                    html.Div([
                        html.Label("MAX:"),
                    ], className='one columns',
                    ),
                    html.Div([
                        dcc.Input(id='ID_PCB_Param_0_MAX',
                                  value="100",
                                  debounce=True,
                                  style={'textAlign': TEXT_POSITION,
                                         'width': '100%'},
                                  ),
                    ], className='two columns',
                        id='ID_PCB_Param_0_MAX_Wrapper',
                    ),
                    html.Div([
                        dcc.RadioItems(
                            id="ID_Param_0_unit_selector",
                            options=[
                                {"label": "mm", "value": "mm"},
                                {"label": "mil", "value": "mil"},
                            ],
                            value="mm",  # Initial value
                            inline=True,  # Horizontal alignment
                        ),
                    ], className='three columns'
                    ),
                ], className='row', ),

                html.Div([
                    html.Div([
                        html.Label("DIELECTRIC CONSTANT (εr)",
                                   id='ID_PCB_Param_1_Name'),
                    ], className='three columns',
                        id='ID_PCB_Param_1_Name_Wrapper',
                    ),
                    html.Div([
                        html.Label("From List:"),
                    ], className='one columns',
                    ),
                    html.Div([
                        dcc.Dropdown(
                            id='ID_PCB_Material_List',
                            options=[{'label': k, 'value': v} for k, v in PCB_Material_List.items()],
                            placeholder="PCB Material",
                            clearable=True
                        ),
                    ], className='four columns',
                        id='ID_PCB_Param_1_List_Wrapper',
                    ),
                    html.Div([
                        html.Label("Number Iunput:"),
                    ], className='one columns',
                    ),
                    html.Div([
                        dcc.Input(id='ID_PCB_Param_1_Input',
                                  # value=100,
                                  debounce=True,
                                  style={'textAlign': TEXT_POSITION,
                                         'width': '75%'},
                                  ),
                    ], className='three columns',
                        id='ID_PCB_Param_1_Input_Wrapper',
                    ),


                ], className='row', ),
                html.Div([
                    html.Div([
                        html.Label("Thickness (t)",
                                   id='ID_PCB_Param_2_Name'),
                    ], className='three columns',
                        id='ID_PCB_Param_2_Name_Wrapper',
                    ),
                    html.Div([
                        dcc.Input(id='ID_PCB_Param_2',
                                  debounce=True,
                                  style={'textAlign': TEXT_POSITION,
                                         'width': '100%'},
                                  ),
                    ], className='four columns',
                        id='ID_PCB_Param_2_Wrapper',
                    ),
                    html.Div([
                        dcc.RadioItems(
                            id="ID_Param_2_unit_selector",
                            options=[
                                {"label": "oz/ft^2", "value": "oz"},
                                {"label": "um", "value": "um"},
                                {"label": "mm", "value": "mm"},
                                {"label": "mil", "value": "mil"},
                            ],
                            value="oz",  # Initial value
                            inline=True,  # Horizontal alignment
                        ),
                    ], className='five columns'
                    )


                ], className='row', ),
                html.Div([
                    html.Div([
                        html.Label("Height (h)",
                                   id='ID_PCB_Param_3_Name'),
                    ], className='three columns',
                        id='ID_PCB_Param_3_Name_Wrapper',
                    ),
                    html.Div([
                        dcc.Input(id='ID_PCB_Param_3',
                                  debounce=True,
                                  style={'textAlign': TEXT_POSITION,
                                         'width': '100%'},
                                  ),
                    ], className='four columns',
                        id='ID_PCB_Param_3_Wrapper',
                    ),
                    html.Div([
                        dcc.RadioItems(
                            id="ID_Param_3_unit_selector",
                            options=[
                                {"label": "um", "value": "um"},
                                {"label": "mm", "value": "mm"},
                                {"label": "mil", "value": "mil"},
                            ],
                            value="mm",  # Initial value
                            inline=True,  # Horizontal alignment
                        ),
                    ], className='five columns'
                    ),

                ], className='row', ),
                html.Div([
                    html.Div([
                        html.Label("Height shorter (ha)",
                                   id='ID_PCB_Param_4_Name'),
                    ], className='three columns',
                        id='ID_PCB_Param_4_Name_Wrapper',
                    ),
                    html.Div([
                        dcc.Input(id='ID_PCB_Param_4',
                                  debounce=True,
                                  style={'textAlign': TEXT_POSITION,
                                         'width': '100%'},
                                  ),
                    ], className='four columns',

                    ),
                    html.Div([
                        dcc.RadioItems(
                            id="ID_Param_4_unit_selector",
                            options=[
                                {"label": "um", "value": "um"},
                                {"label": "mm", "value": "mm"},
                                {"label": "mil", "value": "mil"},
                            ],
                            value="mm",  # Initial value
                            inline=True,  # Horizontal alignment
                        ),
                    ], className='five columns',
                    ),

                ], className='row',
                id='ID_PCB_Param_4_Wrapper',
                ),
                # html.Div([
                #     html.Div([
                #         html.Label("Height bigger (hb)",
                #                    id='ID_PCB_Param_5_Name'),
                #     ], className='four columns',
                #         id='ID_PCB_Param_5_Name_Wrapper',
                #     ),
                #     html.Div([
                #         dcc.Input(id='ID_PCB_Param_5',
                #                   debounce=True,
                #                   style={'textAlign': TEXT_POSITION,
                #                          'width': '100%'},
                #                   ),
                #     ], className='four columns',
                #     ),
                #     html.Div([
                #         dcc.RadioItems(
                #             id="ID_Param_4_unit_selector",
                #             options=[
                #                 {"label": "mm", "value": "mm"},
                #                 {"label": "mil", "value": "mil"},
                #             ],
                #             value="mm",  # Initial value
                #             inline=True,  # Horizontal alignment
                #         ),
                #     ], className='four columns'
                #     ),
                #
                # ], className='row',
                # id='ID_PCB_Param_5_Wrapper',
                # ),
                # html.Div([
                #     html.Div([
                #         html.Label("Param6",
                #                    id='ID_PCB_Param_6_Name'),
                #     ], className='four columns',
                #         id='ID_PCB_Param_6_Name_Wrapper',
                #     ),
                #     html.Div([
                #         dcc.Input(id='ID_PCB_Param_6',
                #                   debounce=True,
                #                   style={'textAlign': TEXT_POSITION,
                #                          'width': '100%'},
                #                   ),
                #     ], className='four columns',
                #     ),
                #
                # ], className='row',
                #     id='ID_PCB_Param_6_Wrapper',
                # ),
                # html.Div([
                #     html.Div([
                #         html.Label("Param7",
                #                    id='ID_PCB_Param_7_Name'),
                #     ], className='four columns',
                #         id='ID_PCB_Param_7_Name_Wrapper',
                #     ),
                #     html.Div([
                #         dcc.Input(id='ID_PCB_Param_7',
                #                   debounce=True,
                #                   style={'textAlign': TEXT_POSITION,
                #                          'width': '100%'},
                #                   ),
                #     ], className='four columns',
                #     ),
                #
                # ], className='row',
                #     id='ID_PCB_Param_7_Wrapper',
                # ),
                # html.Div([
                #     html.Div([
                #         html.Label("Param8",
                #                    id='ID_PCB_Param_8_Name'),
                #     ], className='four columns',
                #         id='ID_PCB_Param_8_Name_Wrapper',
                #     ),
                #     html.Div([
                #         dcc.Input(id='ID_PCB_Param_8',
                #                   debounce=True,
                #                   style={'textAlign': TEXT_POSITION,
                #                          'width': '100%'},
                #                   ),
                #     ], className='four columns',
                #     ),
                #
                # ], className='row',
                # id='ID_PCB_Param_8_Wrapper',
                # ),
                html.Div([
                    html.Div([
                        html.Label("Gap (G)",
                                   id='ID_PCB_Param_5_Name'),
                    ], className='three columns',
                        id='ID_PCB_Param_5_Name_Wrapper',
                    ),
                    html.Div([
                        dcc.Input(id='ID_PCB_Param_5',
                                  debounce=True,
                                  style={'textAlign': TEXT_POSITION,
                                         'width': '100%'},
                                  ),
                    ], className='four columns',

                    ),
                    html.Div([
                        dcc.RadioItems(
                            id="ID_Param_5_unit_selector",
                            options=[
                                {"label": "um", "value": "um"},
                                {"label": "mm", "value": "mm"},
                                {"label": "mil", "value": "mil"},
                            ],
                            value="mm",  # Initial value
                            inline=True,  # Horizontal alignment
                        ),
                    ], className='five columns',
                    ),

                ], className='row',
                    id='ID_PCB_Param_5_Wrapper',
                ),
                # html.Div([
                #     html.Div([
                #         html.Label("Height bigger (hb)",
                #                    id='ID_PCB_Param_5_Name'),
                #     ], className='four columns',
                #         id='ID_PCB_Param_5_Name_Wrapper',
                #     ),
                #     html.Div([
                #         dcc.Input(id='ID_PCB_Param_5',
                #                   debounce=True,
                #                   style={'textAlign': TEXT_POSITION,
                #                          'width': '100%'},
                #                   ),
                #     ], className='four columns',
                #     ),
                #     html.Div([
                #         dcc.RadioItems(
                #             id="ID_Param_4_unit_selector",
                #             options=[
                #                 {"label": "mm", "value": "mm"},
                #                 {"label": "mil", "value": "mil"},
                #             ],
                #             value="mm",  # Initial value
                #             inline=True,  # Horizontal alignment
                #         ),
                #     ], className='four columns'
                #     ),
                #
                # ], className='row',
                # id='ID_PCB_Param_5_Wrapper',
                # ),
                # html.Div([
                #     html.Div([
                #         html.Label("Param6",
                #                    id='ID_PCB_Param_6_Name'),
                #     ], className='four columns',
                #         id='ID_PCB_Param_6_Name_Wrapper',
                #     ),
                #     html.Div([
                #         dcc.Input(id='ID_PCB_Param_6',
                #                   debounce=True,
                #                   style={'textAlign': TEXT_POSITION,
                #                          'width': '100%'},
                #                   ),
                #     ], className='four columns',
                #     ),
                #
                # ], className='row',
                #     id='ID_PCB_Param_6_Wrapper',
                # ),
                # html.Div([
                #     html.Div([
                #         html.Label("Param7",
                #                    id='ID_PCB_Param_7_Name'),
                #     ], className='four columns',
                #         id='ID_PCB_Param_7_Name_Wrapper',
                #     ),
                #     html.Div([
                #         dcc.Input(id='ID_PCB_Param_7',
                #                   debounce=True,
                #                   style={'textAlign': TEXT_POSITION,
                #                          'width': '100%'},
                #                   ),
                #     ], className='four columns',
                #     ),
                #
                # ], className='row',
                #     id='ID_PCB_Param_7_Wrapper',
                # ),
                # html.Div([
                #     html.Div([
                #         html.Label("Param8",
                #                    id='ID_PCB_Param_8_Name'),
                #     ], className='four columns',
                #         id='ID_PCB_Param_8_Name_Wrapper',
                #     ),
                #     html.Div([
                #         dcc.Input(id='ID_PCB_Param_8',
                #                   debounce=True,
                #                   style={'textAlign': TEXT_POSITION,
                #                          'width': '100%'},
                #                   ),
                #     ], className='four columns',
                #     ),
                #
                # ], className='row',
                # id='ID_PCB_Param_8_Wrapper',
                # ),
            ],
                style={"border": "1px black dashed",
                       "margin": "5px",
                       "padding": "5px",
                       "borderRadius": "5px",
                       },
            ),
        ], className='six columns',
        ),
        html.Div([
            # html.H5("Graph"),
            dcc.Graph(
                id="ID_PCB_Graph",
                style={"display": "true",
                       'textAlign': 'center',
                       # 'width': '95vw',
                       'height': '65vh',
                },
                mathjax=True,
            ),
        ], className='six columns',
        ),
        ], className='row',
           style={"margin": "5px",
                  "padding": "5px",
                 },
        ),


	]
)