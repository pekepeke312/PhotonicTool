from dash import html
from dash import dcc
from dash.dependencies import Input, Output

from .assets import (
    page_CS,
)

from server import app

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

def CheatSheet_tab_menu():
    menu = html.Div(
        [
            html.Div([
            dcc.Tabs(id='CheatSheet_FPGA_tabs_selection',
                     value='VHDL',
                     children=[
                         dcc.Tab(label='VHDL', value='VHDL', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='Verilog', value='Verilog', style=tab_style,
                                 selected_style=tab_selected_style),
                     ],
                     style=tabs_styles,
                     ),
            ]
            )
        ],
        className="row all-tabs",
    )
    return menu

def CheatSheet_FPGA_layout(app):
    return html.Div([
        # html.H5(["Select a Genre"]),
        CheatSheet_tab_menu(),
        html.Div([
            dcc.Location(id="CheatSheet_FPGA_page_url",
                         refresh=False),
        ]
        ),

        html.Div([
            dcc.Location(id="CheatSheet_FPGA_url", refresh=False),
            html.Div(id="CheatSheet_FPGA_page_contents")

        ]
        ),
    ])

@app.callback(
    Output(component_id="CheatSheet_FPGA_page_contents", component_property="children"),
    [Input(component_id="CheatSheet_FPGA_tabs_selection", component_property="value"),
    Input(component_id="CheatSheet_FPGA_url", component_property="pathname")]
)
def CheatSheet_page(CheatSheet_Tabselection,pathname):
    if CheatSheet_Tabselection == 'VHDL':     #Default Page
         return page_CS.create_layout(app, file=r"CheatSheet/assets/VHDL.pdf")
    elif CheatSheet_Tabselection == 'Verilog':
         return page_CS.create_layout(app, file=r"CheatSheet/assets/Verilog.pdf")
    else:
        return html.Div("not yet")


