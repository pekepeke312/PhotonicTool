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
            dcc.Tabs(id='CheatSheet_ELEC_tabs_selection',
                     value='Cable',
                     children=[
                         dcc.Tab(label='Cable', value='Cable', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='Altium', value='Altium', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='Opamp', value='Opamp', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='Color Code', value='Color Code', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='IC Package', value='IC_Package', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='Unit Conversion', value='EMC_Formula', style=tab_style,
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

def CheatSheet_ELEC_layout(app):
    return html.Div([
        # html.H5(["Select a Genre"]),
        CheatSheet_tab_menu(),
        html.Div([
            dcc.Location(id="CheatSheet_ELEC_page_url",
                         refresh=False),
        ]
        ),

        html.Div([
            dcc.Location(id="CheatSheet_ELEC_url", refresh=False),
            html.Div(id="CheatSheet_ELEC_page_contents")

        ]
        ),
    ])

@app.callback(
    Output(component_id="CheatSheet_ELEC_page_contents", component_property="children"),
    [Input(component_id="CheatSheet_ELEC_tabs_selection", component_property="value"),
    Input(component_id="CheatSheet_ELEC_url", component_property="pathname")]
)
def CheatSheet_page(CheatSheet_Tabselection,pathname):
    if CheatSheet_Tabselection == 'Altium':     #Default Page
         return page_CS.create_layout(app, file=r"CheatSheet/assets/Altium2.pdf")
    elif CheatSheet_Tabselection == 'Opamp':
         return page_CS.create_layout(app, file=r"CheatSheet/assets/Opamp.pdf")
    elif CheatSheet_Tabselection == 'Color Code':
         return page_CS.create_layout(app, file=r"CheatSheet/assets/ColorCode.pdf")
    elif CheatSheet_Tabselection == 'IC_Package':
         return page_CS.create_layout(app, file=r"CheatSheet/assets/IC_Package.pdf")
    elif CheatSheet_Tabselection == 'EMC_Formula':
         return page_CS.create_layout(app, file=r"CheatSheet/assets/EMC_Formula.pdf")
    elif CheatSheet_Tabselection == 'Cable':
         return page_CS.create_layout(app, file=r"CheatSheet/assets/Cable.pdf")
    else:
        return html.Div("not yet")


