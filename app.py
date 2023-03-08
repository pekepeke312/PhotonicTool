from dash import html
from dash import dcc
from dash.dependencies import Input, Output

from DataAnalyzer.Functions import Running_SpectrumAnalyzer#, tab_menu
from DataAnalyzer.Functions import Running_RFAnalyzer
from DataAnalyzer.Functions import Running_API_Mouser

#from PowerModuleCheck.PowerModuleCheckFunctions import Run_PMMaintenance

from DataAnalyzer.DataAnalyzer_Contents import (
    DataAnalyzer_layout,
)

from PartSearch.PartSearch_Contensts import (
    PartSearch_layout,
)

from Top_Assets.Top_Level_page_HistoryLog import (
    Analysis_Tool_History_layout,
)

from server import app, server
from kill_server import kill_server
from TextWriter import *

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
    'backgroundColor': '#85929E',
    'color': 'white',
    'padding': '6px'
}
##########################################################################

def tab_menu():
    menu = html.Div(
        [
            dcc.Tabs(id='tabs-selection',
                     value='Part Search', #Default Page
                     children=[
                         dcc.Tab(label='Part Search', value='Part Search', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='Data Analyzer', value='Data Analyzer', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='Revision History', value='Revision History', style=tab_style,
                                 selected_style=tab_selected_style),
                     ],
                     style=tabs_styles,
                     ),

        ],
        className="row all-tabs",
    )
    return menu

app.layout = html.Div([
    html.H1("Photonic Tools"),
    tab_menu(),
    html.Div([
        dcc.Location(id="page_url",
                     refresh=False),
    ]
    ),

    html.Div([
        dcc.Location(id="url", refresh=False),
        html.Div(id="page_contents")

    ]
    ),
 ])

@app.callback(
    Output(component_id="page_contents", component_property="children"),
    [Input(component_id="tabs-selection", component_property="value"),
    Input(component_id="url", component_property="pathname")]
)
def display_page(Tabselection,pathname):
    if Tabselection == 'Data Analyzer':     #Default Page
        return DataAnalyzer_layout(app)

    elif Tabselection == 'Part Search':
        return PartSearch_layout(app)

    elif Tabselection == 'Revision History':
        return Analysis_Tool_History_layout(app)
    else:
        return html.Div("not yet")


