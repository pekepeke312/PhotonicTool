import os
import openpyxl as op

import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

path_desktop = os.environ['USERPROFILE'] + str('\\Desktop\\')

if not os.path.exists(path_desktop + r'Promira_Batch_files'):
    os.makedirs(path_desktop + r'Promira_Batch_files')

workbook = op.load_workbook("DataAnalyzer\\assets\\Promira_Template.xlsx")
workbook.save(path_desktop + r'Promira_Batch_files\Promira_Template.xlsx')