from dash import html
from dash import dcc
from dash.dependencies import Input, Output

from .Functions import Running_SpectrumAnalyzer#, tab_menu
from .Functions import Running_RFAnalyzer
from .Functions import Running_API_Mouser

from .assets import (
    page_Maincontents,
    page_HistoryLog,
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

def DataAnalyzer_tab_menu():
    menu = html.Div(
        [
            dcc.Tabs(id='DataAnalyzer_tabs-selection',
                     value='Data Analyzer',
                     children=[
                         dcc.Tab(label='Data Analyzer Main Contents', value='Data Analyzer', style=tab_style,
                                 selected_style=tab_selected_style),
                         dcc.Tab(label='Data Analyzer Revision History', value='Revision History', style=tab_style,
                                 selected_style=tab_selected_style),
                     ],
                     style=tabs_styles,
                     ),

        ],
        className="row all-tabs",
    )
    return menu

def DataAnalyzer_layout(app):
    return html.Div([
        DataAnalyzer_tab_menu(),
        html.Div([
            dcc.Location(id="DataAnalyzer_page_url",
                         refresh=False),
        ]
        ),

        html.Div([
            dcc.Location(id="DataAnalyzer_url", refresh=False),
            html.Div(id="DataAnalyzer_page_contents")

        ]
        ),
    ])

@app.callback(
    Output(component_id="DataAnalyzer_page_contents", component_property="children"),
    [Input(component_id="DataAnalyzer_tabs-selection", component_property="value"),
    Input(component_id="DataAnalyzer_url", component_property="pathname")]
)
def DataAnalyzer_page(DataAnalyzer_Tabselection,pathname):
    if DataAnalyzer_Tabselection == 'Data Analyzer':     #Default Page
        return page_Maincontents.create_layout(app)
    elif DataAnalyzer_Tabselection == 'Revision History':
        return page_HistoryLog.create_layout(app)
    else:
        return html.Div("not yet")


