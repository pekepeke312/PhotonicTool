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
            dcc.Tabs(id='CheatSheet_Python_tabs_selection',
                     value='Python3',
                     children=[
                         dcc.Tab(label='Python3', value='Python3', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='Python2', value='Python2', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='Scikit', value='Scikit', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='Numpy', value='Numpy', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='Pandas', value='Pandas', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='plotly', value='plotly', style=tab_style,
                                 selected_style=tab_selected_style),

                         dcc.Tab(label='Matplotlib', value='Matplotlib', style=tab_style,
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

def CheatSheet_Python_layout(app):
    return html.Div([
        # html.H5(["Select a Genre"]),
        CheatSheet_tab_menu(),
        html.Div([
            dcc.Location(id="CheatSheet_Python_page_url",
                         refresh=False),
        ]
        ),

        html.Div([
            dcc.Location(id="CheatSheet_Python_url", refresh=False),
            html.Div(id="CheatSheet_Python_page_contents")

        ]
        ),
    ])

@app.callback(
    Output(component_id="CheatSheet_Python_page_contents", component_property="children"),
    [Input(component_id="CheatSheet_Python_tabs_selection", component_property="value"),
    Input(component_id="CheatSheet_Python_url", component_property="pathname")]
)
def CheatSheet_page(CheatSheet_Tabselection,pathname):
    if CheatSheet_Tabselection == 'Python3':     #Default Page
         return page_CS.create_layout(app, file=r"CheatSheet/assets/python3.pdf")
    elif CheatSheet_Tabselection == 'Python2':
         return page_CS.create_layout(app, file=r"CheatSheet/assets/python2.pdf")
    elif CheatSheet_Tabselection == 'Numpy':
         return page_CS.create_layout(app, file=r"CheatSheet/assets/Numpy.pdf")
    elif CheatSheet_Tabselection == 'Pandas':
         return page_CS.create_layout(app, file=r"CheatSheet/assets/Pandas.pdf")
    elif CheatSheet_Tabselection == 'Scikit':
         return page_CS.create_layout(app, file=r"CheatSheet/assets/Scikit.pdf")
    elif CheatSheet_Tabselection == 'plotly':
         return page_CS.create_layout(app, file=r"CheatSheet/assets/plotly.pdf")
    elif CheatSheet_Tabselection == 'Matplotlib':
         return page_CS.create_layout(app, file=r"CheatSheet/assets/Matplotlib.pdf")
    else:
        return html.Div("not yet")


