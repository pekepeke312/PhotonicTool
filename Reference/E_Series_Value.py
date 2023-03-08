from dash import dcc
from dash import html

import plotly.figure_factory as ff

VALUE_LIST = {
"E3" : [10,   22,  47],
"E6" : [10,   15,  22,  33,  47,  68],
"E12": [10,   12,  15,  18,  22,  27,  33,  39,  47,  56,  68,  82],
"E24": [10,   11,  12,  13,  15,  16,  18,  20,  22,  24,  27,  30,
        33,   36,  39,  43,  47,  51,  56,  62,  68,  75,  82,  91],
"E48": [10.0, 10.5, 11.0, 11.5, 12.1, 12.7, 13.3, 14.0, 14.7, 15.4, 16.2, 16.9,
        17.8, 18.7, 19.6, 20.5, 21.5, 22.6, 23.7, 24.9, 26.1, 27.4, 28.7, 30.1,
        31.6, 33.2, 34.8, 36.5, 38.3, 40.2, 42.2, 44.2, 46.4, 48.7, 51.1, 53.6,
        56.2, 59.0, 61.9, 64.9, 68.1, 71.5, 75.0, 78.7, 82.5, 86.6, 90.9, 95.3],
"E96": [10.0, 10.2, 10.5, 10.7, 11.0, 11.3, 11.5, 11.8, 12.1, 12.4, 12.7, 13.0,
        13.3, 13.7, 14.0, 14.3, 14.7, 15.0, 15.4, 15.8, 16.2, 16.5, 16.9, 17.4,
        17.8, 18.2, 18.7, 19.1, 19.6, 20.0, 20.5, 21.0, 21.5, 22.1, 22.6, 23.2,
        23.7, 24.3, 24.9, 25.5, 26.1, 26.7, 27.4, 28.0, 28.7, 29.4, 30.1, 30.9,
        31.6, 32.4, 33.2, 34.0, 34.8, 35.7, 36.5, 37.4, 38.3, 39.2, 40.2, 41.2,
        42.2, 43.2, 44.2, 45.3, 46.4, 47.5, 48.7, 49.9, 51.1, 52.3, 53.6, 54.9,
        56.2, 57.6, 59.0, 60.4, 61.9, 63.4, 64.9, 66.5, 68.1, 69.8, 71.5, 73.2,
        75.0, 76.8, 78.7, 80.6, 82.5, 84.5, 86.6, 88.7, 90.9, 93.1, 95.3, 97.6],
}
TOLERANCE_LIST = {
    "E3":0.4,
    "E6":0.2,
    "E12":0.1,
    "E24":0.05,
    "E48":0.02,
    "E96":0.01,
}

RATIO = 0

df = []
for SERIES in VALUE_LIST.keys():
    for N in VALUE_LIST[SERIES]:
        Temp_dict = dict(Task=SERIES,
                       Start=N,#str(round(N*(1-TOLERANCE_LIST[SERIES]*RATIO),1)),
                       Finish=N+0.1,#str(round(N*(1+TOLERANCE_LIST[SERIES]*RATIO),1)),
                       Resource=str(SERIES)#+":"+str(N)
                       )
        df.append(Temp_dict)


# df = [
#         #dict(Task="E6", Start=str(1*0.6),     Finish=str(1*1.4),     Resource = "E6"),
#         dict(Task="E6", Start=str(2.2 * 0.8), Finish=str(2.2 * 1.2), Resource = "2.2", name="TYP=2.2"),
#         dict(Task="E6", Start=str(4.7 * 0.8), Finish=str(4.7 * 1.2), Resource = "E6"),
#
#         dict(Task="E12", Start=str(2.7 * 0.8), Finish=str(2.7 * 1.2), Resource = "E12"),
# ]



fig = ff.create_gantt(df,
                      index_col = "Resource",
                      group_tasks=True,
                      )
fig.layout.xaxis.type = 'linear'

fig.data[0].line.width = 1
fig.show()