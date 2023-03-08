import dash
from dash import callback_context

from dash.dependencies import Input, Output, State
import codecs
from .assets import (
     page_PS_Maincontents,
     page_PS_HistoryLog,
     page_PS_DatabaseLink,
 )

from DataAnalyzer.Digikey_WebScraping import Digikey_WebScraping

from .PartSearchTool import *
from server import app

Target_Path = '0'

SheetName = ""
CURRENT_PAGE = ""
SORT_BY =""


Running_PartSearch = 0
def Run_PartSearch(DebugMode=False):
    global Running_PartSearch
    Running_PartSearch = PartSearchTool(DebugMode=DebugMode)
    return Running_PartSearch

@app.callback(
    Output(component_id="id_PartNumberFileAddress", component_property="figure"),
    [Input(component_id="PartSearch-tabs-selection", component_property="value"),
    ]
)
def DataBaseLinkViewer(Tabselection):
    global Running_PartSearch
    if Tabselection == 'Database Link':
        return Running_PartSearch.DataBaseTable
    else:
        return {}

@app.callback(
    Output(component_id="id_DD_SheetNames", component_property="options"),
    [Input(component_id="PartSearch-tabs-selection", component_property="value"),
    ]
)
def DD_ListValueUpdate(Tabselection):
    global Running_PartSearch
    if Tabselection == 'Main Contents':
        return Running_PartSearch.DD_SheetNames
    else:
        return {}

@app.callback(
    (Output(component_id="PS_table-paging-and-sorting",component_property="columns"),
     Output(component_id='PS_table-paging-and-sorting',component_property='data'),
     ),
    (Input(component_id="id_DD_SheetNames", component_property="value"),
     Input(component_id='PS_table-paging-and-sorting',component_property= "page_current"),
     Input(component_id='PS_table-paging-and-sorting',component_property= "page_size"),
     Input(component_id='PS_table-paging-and-sorting',component_property= 'sort_by'),
     ),
)
def DataUpdate(Target_PS_SheetName, page_current, page_size, sort_by):
    global Running_PartSearch, SheetName, CURRENT_PAGE, SORT_BY
    if Target_PS_SheetName != '' and Target_PS_SheetName != None:
        #Running_PartSearch = Run_PartSearch(DebugMode=False)
        CURRENT_PAGE = page_current
        SORT_BY = sort_by
        SheetName = Target_PS_SheetName
        # Running_PartSearch.LoadDatafromDababase(Target=PM_PN)
        #     Running_PartSearch.Plotly_Histogram_Generator(StatusFilter=PM_ST)
        if SheetName != 'All':
           Running_PartSearch.Plotly_Table_Generator(SheetFilter=SheetName)
        else:
            Running_PartSearch.Plotly_Table_Generator()

        Column =[
            {'name': i, 'id': i, 'deletable': True} for i in (Running_PartSearch.Searched_Result_Table_df.columns)
                ]
        if len(sort_by):
            dff = Running_PartSearch.Searched_Result_Table_df.sort_values(
                str(sort_by[0]['column_id']),
                ascending=sort_by[0]['direction'] == 'asc',
                inplace=False
            )
        else:
                # No sort is applied
            dff = Running_PartSearch.Searched_Result_Table_df

        Data = dff.iloc[
            page_current * page_size:(page_current + 1) * page_size
            ].to_dict('records')

        return [Column, Data]#, Running_PMMaintenance.SerialNumberList_for_DD]

    if page_current != CURRENT_PAGE or sort_by != SORT_BY:
        CURRENT_PAGE = page_current
        SORT_BY = sort_by
        SheetName = Target_PS_SheetName
        Running_PartSearch.Plotly_Table_Generator(SheetFilter=SheetName)
        Column =[
            {'name': i, 'id': i, 'deletable': True} for i in (Running_PartSearch.Searched_Result_Table_df.columns)
            ]
        if len(sort_by):
            dff = Running_PartSearch.Searched_Result_Table_df.sort_values(
                sort_by[0]['column_id'],
                ascending=sort_by[0]['direction'] == 'asc',
                inplace=False
            )
        else:
            dff = Running_PartSearch.Searched_Result_Table_df

        Data = dff.iloc[
            page_current * page_size:(page_current + 1) * page_size
            ].to_dict('records')
        return [Column, Data]

    if page_current != CURRENT_PAGE or sort_by != SORT_BY:
        CURRENT_PAGE = page_current
        SORT_BY = sort_by
        Column =[
            {'name': i, 'id': i, 'deletable': True} for i in (Running_PartSearch.Searched_Result_Table_df.columns)
                ]
        if len(sort_by):
            dff = Running_PartSearch.Searched_Result_Table_df.sort_values(
                sort_by[0]['column_id'],
                ascending=sort_by[0]['direction'] == 'asc',
                inplace=False
            )
        else:
            # No sort is applied
            dff = Running_PartSearch.Searched_Result_Table_df

        Data = dff.iloc[
            page_current * page_size:(page_current + 1) * page_size
            ].to_dict('records')
        return [Column, Data]

    else:
        return [dash.no_update, dash.no_update,dash.no_update,dash.no_update]

@app.callback(
    Output(component_id="PS_download_dataframe_csv", component_property="data"),
    Input(component_id="PS_btn_Export_Table", component_property="n_clicks"),
    State(component_id='PS_table-paging-and-sorting', component_property="derived_virtual_data"),
    prevent_initial_call=True,
)
def ExportTable(btn_click,Data):
    global Running_PartSearch
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if "btn_Export_Table" in changed_id and btn_click != 0:
        data = Running_PartSearch.Export_Searched_Table(Data)
        return data
    else:
        return ()

@app.callback(
    Output('Table_Selected_Out', 'children'),
    Input('PS_table-paging-and-sorting', 'active_cell'),
    State('PS_table-paging-and-sorting', "derived_virtual_data"),
)
def update_graphs(active_cell, Data):
    global Running_PartSearch
    if active_cell != None:
        cell_data = Data[active_cell['row']]['Manufacturer PN']

        if active_cell['column_id'] == 'Manufacturer PN':
            Scraping = Digikey_WebScraping(PartNumber=cell_data)
            Scraping.Scraping()

        return f"Opening Manufacurer PN: \"{cell_data}\" in different Chrome browser"
    return "Click a Manufacture PN to open Digi-Key website"


global file
@app.callback(
    Output('PS_console-out','srcDoc'),
    [Input('interval_PS','n_intervals')])
def update_output(n):
    TextLine = 14

    Toppath = str(pathlib.Path(__file__).parent.parent.resolve())
    path = Toppath + str('\\Top_Assets\\')

    #path = os.getcwd() + str('\\Top_Assets\\')
    path = r'{}'.format(path)

    global file
    try:
        file = open(path + 'Log.txt', 'r')
    except:
        pass

    data = ''
    try:
        lines = file.readlines()
    except:
        fd = codecs.open(path + 'Log.txt', 'r', encoding='utf-8')
        lines = fd.read()

    if lines.__len__() <= TextLine:
        last_lines = lines
    else:
        last_lines = lines[-1*TextLine:]
    for line in last_lines:
        data = data + line + '<BR>'
    file.close()
    return data

