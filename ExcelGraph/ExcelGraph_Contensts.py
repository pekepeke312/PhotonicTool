from dash import html
from dash import dcc
from dash.dependencies import Input, Output

from .EG_Functions import PlotlyGraph

from .assets import (
    page_EG_1D_Histogram,
    page_EG_2D_Histogram,
    page_EG_Scatter_Graph,
    page_EG_HistoryLog
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

def ExcelGraph_tab_menu():
    menu = html.Div(
        [
            dcc.Tabs(id='ExcelGraph_tabs-selection',
                     value='Scatter Graph',
                     children=[
                         dcc.Tab(label='Scatter Graph', value='Scatter Graph', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='1D Histogram', value='1D Histogram', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='2D Histogram', value='2D Histogram', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='Excel Graph Revision History', value='Revision History', style=tab_style,
                                 selected_style=tab_selected_style),
                     ],
                     style=tabs_styles,
                     ),

        ],
        className="row all-tabs",
    )
    return menu

def ExcelGraph_layout(app):
    return html.Div([
        html.H5(["1. Select a Target Excel File"]),
        dcc.Upload(
            id="ExcelGraph_upload-data",
            children=html.Div(
                ["Drag and drop or click to select an Excel File."]
            ),
            style={
                "width": "98%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "2px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=True,
        ),
        html.H6(["File = "],
                id='EG_Loading_File_Name',
                ),
        html.Br([]),
        html.H5(["2. Select an Analyis Mode"]),
        ExcelGraph_tab_menu(),
        html.Div([
            dcc.Location(id="ExcelGraph_page_url",
                         refresh=False),
        ]
        ),

        html.Div([
            dcc.Location(id="ExcelGraph_url", refresh=False),
            html.Div(id="ExcelGraph_page_contents")

        ]
        ),
    ])

@app.callback(
    Output(component_id="ExcelGraph_page_contents", component_property="children"),
    [Input(component_id="ExcelGraph_tabs-selection", component_property="value"),
    Input(component_id="ExcelGraph_url", component_property="pathname")]
)
def ExcelGraph_page(ExcelGraph_Tabselection,pathname):
    if ExcelGraph_Tabselection == '1D Histogram':     #Default Page
        return page_EG_1D_Histogram.create_layout(app)
    elif ExcelGraph_Tabselection == '2D Histogram':
        return page_EG_2D_Histogram.create_layout(app)
    elif ExcelGraph_Tabselection == 'Scatter Graph':
        return page_EG_Scatter_Graph.create_layout(app)
    elif ExcelGraph_Tabselection == 'Revision History':
        return page_EG_HistoryLog.create_layout(app)
    else:
        return html.Div("not yet")


