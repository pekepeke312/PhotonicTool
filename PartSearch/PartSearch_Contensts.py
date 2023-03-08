from dash import dcc
from dash import html
from dash.dependencies import Input, Output#, State

# from .PowerModuleCheckFunctions import Run_PMMaintenance
#
from .assets import (
    page_PS_DatabaseLink,
    page_PS_Maincontents,
    page_PS_HistoryLog,
)

from PartSearch.PartSearch_Functions import *



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
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}
##########################################################################

def PartSearch_tab_menu():
    menu = html.Div(
        [
            dcc.Tabs(id='PartSearch-tabs-selection',
                     value='Main Contents',
                     children=[
                         dcc.Tab(label='Part Search Contents', value='Main Contents', style=tab_style,
                                 selected_style=tab_selected_style),
                         dcc.Tab(label='Database Link', value='Database Link', style=tab_style,
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

def PartSearch_layout(app):
    return html.Div([
        #html.H2("Power Module Maintenance Tool"),
        PartSearch_tab_menu(),
        html.Div([
            dcc.Location(id="PartSearch_page_url",
                         refresh=False),
        ]
        ),

        html.Div([
            dcc.Location(id="PartSearch_url", refresh=False),
            html.Div(id="PartSearch_contents")
        ]
        ),
    ])


@app.callback(
    Output(component_id="PartSearch_contents", component_property="children"),
    [Input(component_id="PartSearch-tabs-selection", component_property="value"),
     Input(component_id="PartSearch_page_url", component_property="pathname")]
)
def display_page(Tabselection,pathname):
    global Running_PartSearch
    if Tabselection == 'Main Contents':     #Default Page
        Running_PartSearch = Run_PartSearch(DebugMode=False)
        return page_PS_Maincontents.create_layout(app)
    elif Tabselection == 'Database Link':
        return page_PS_DatabaseLink.create_layout(app)
    elif Tabselection == 'Revision History':
        return page_PS_HistoryLog.create_layout(app)
    else:
        return html.Div("not yet")