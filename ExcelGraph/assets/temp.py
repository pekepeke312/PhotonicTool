import xlwings as xw
import sys
path = "C:\\Users\\pekep\\OneDrive\\Project\\Python\\Functions\\"
sys.path.append(path)
from Functions import *

# if __name__ == '__main__':
#     from Functions import *
# else:
#     from Functions.Functions import *

@xw.sub  # only required if you want to import it or run it via UDF Server
def main():
    Graph = PlotlyGraphGenerator()

    wb = xw.Book.caller()
    sheet = wb.sheets[0]
    # address, x, y = CurrentLocation()
    # sheet["A2"].value = address
    # sheet["B2"].value = x
    # sheet['C2'].value = y

    if sheet["A1"].value == "Function File Location " + path:
        sheet["A1"].value = "Loaded correctly"

    else:
        sheet["A1"].value = "Function File Location " + path

    #xw.serve()
##############################

if __name__ == '__main__':
    # Expects the Excel file next to this source file, adjust accordingly.
    address = "C:\\Users\\pekep\\Desktop\\ExcelMacro\\book1.xlsm"
    xw.Book(address).set_mock_caller()
    main()