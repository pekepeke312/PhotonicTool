from dash import html
from dash import dcc
from dash.dependencies import Input, Output


from .assets import (
    Converter_Impedance,
    Converter_HistoryLog,
    Converter_ResonantFrequency,
    Converter_PicToGraph,
)

from server import app, server
from kill_server import kill_server
from textwriter import *

########################################################################
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}
##########################################################################

def Converter_tab_menu():
    menu = html.Div(
        [
            dcc.Tabs(id='Converter_tabs-selection',
                     value='Unit',
                     children=[
                         dcc.Tab(label='Unit', value='Unit', style=tab_style,
                                 selected_style=tab_selected_style),
                         dcc.Tab(label='Resonant Frequency', value='ResonantFrequency', style=tab_style,
                                 selected_style=tab_selected_style),
                         dcc.Tab(label='Impedance', value='Impedance', style=tab_style,
                                 selected_style=tab_selected_style),
                         dcc.Tab(label='PCB Pattern', value='PCB Pattern', style=tab_style,
                                 selected_style=tab_selected_style),
                         # dcc.Tab(label='Pic-to-Graph', value='Pic-to-Graph', style=tab_style,
                         #         selected_style=tab_selected_style),
                         dcc.Tab(label='Revision History', value='Revision History', style=tab_style,
                                 selected_style=tab_selected_style),
                     ],
                     style=tabs_styles,
                     ),

        ],
        className="row all-tabs",
    )
    return menu

def Converter_layout(app):
    return html.Div([
        Converter_tab_menu(),
        html.Div([
            dcc.Location(id="Conveter_page_url",
                         refresh=False),
        ]
        ),

        html.Div([
            dcc.Location(id="Converter_url", refresh=False),
            html.Div(id="Converter_page_contents")

        ]
        ),
    ])

