from dash import html
from dash import dcc
from dash.dependencies import Input, Output

from .assets import (
    page_CS,
    CS_HistoryLog,
)

from CheatSheet import (
    CheatSheet_Python_Contents,
    CheatSheet_FPGA_Contents,
    CheatSheet_ELEC_Contents,
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
                #html.Div(["Operation Log:"]),
                dcc.Interval(
                    id='interval1',
                    interval=1 * 1000,  # in milliseconds
                    n_intervals=0,
                ),
                html.Div([
                    html.Iframe(id='console-out',
                                srcDoc='',
                                style=dict(height='50px',
                                           width="100%",
                                           overflow='auto')
                                )
                ], className='twelve',
                )
            ], className='row',
                style={"border": "1px black solid"},
            ),
            dcc.Tabs(id='CheatSheet_tabs-selection',
                     value='Git',
                     children=[
                         dcc.Tab(label='Git', value='Git', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='Electrical', value='Electrical', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='Python', value='Python', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='FPGA', value='FPGA', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='Latex', value='Latex', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='Linux', value='Linux', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='Windows10', value='Windows10', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='Cheat Sheet Revision History', value='HistoryLog', style=tab_style,
                                 selected_style=tab_selected_style),
                     ],
                     style=tabs_styles,
                     ),

        ],
        className="row all-tabs",
    )
    return menu

def CheatSheet_layout(app):
    return html.Div([
        # html.H5(["Select a Genre"]),
        CheatSheet_tab_menu(),
        html.Div([
            dcc.Location(id="CheatSheet_page_url",
                         refresh=False),
        ]
        ),

        html.Div([
            dcc.Location(id="CheatSheet_url", refresh=False),
            html.Div(id="CheatSheet_page_contents")

        ]
        ),
    ])

@app.callback(
    Output(component_id="CheatSheet_page_contents", component_property="children"),
    [Input(component_id="CheatSheet_tabs-selection", component_property="value"),
    Input(component_id="CheatSheet_url", component_property="pathname")]
)
def CheatSheet_page(CheatSheet_Tabselection,pathname):
    if CheatSheet_Tabselection == 'Git':     #Default Page
         return page_CS.create_layout(app, file=r"CheatSheet/assets/git.pdf")
    elif CheatSheet_Tabselection == 'Electrical':
         return CheatSheet_ELEC_Contents.CheatSheet_ELEC_layout(app)
    elif CheatSheet_Tabselection == 'Windows10':
         return page_CS.create_layout(app, file=r"CheatSheet/assets/Windows10.pdf")
    elif CheatSheet_Tabselection == 'FPGA':
         return CheatSheet_FPGA_Contents.CheatSheet_FPGA_layout(app)
    elif CheatSheet_Tabselection == 'Python':
         return CheatSheet_Python_Contents.CheatSheet_Python_layout(app)
    elif CheatSheet_Tabselection == 'Latex':
         return page_CS.create_layout(app, file=r"CheatSheet/assets/Latex.pdf")
    elif CheatSheet_Tabselection == 'Linux':
         return page_CS.create_layout(app, file=r"CheatSheet/assets/Linux.pdf")
    elif CheatSheet_Tabselection == 'HistoryLog':
         return CS_HistoryLog.create_layout(app)

    else:
        return html.Div("not yet")


