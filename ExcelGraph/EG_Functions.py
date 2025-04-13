import pandas as pd
import xlwings as xw
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy.stats import norm
import time

from server import app
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import pathlib
import os
import base64
import codecs
from textwriter import textwriter

ColourTable = {
    0: 'blue',
    1: 'orange',
    2: 'green',
    3: 'red',
    4: 'MediumPurple',
    5: 'gray',
    6: 'gold',
    7: 'black',
    8: 'aqua',
    9: 'chocolate',
    10: 'cyan',
    11: 'darkgreen',
    12: 'darkblue',
    13: 'darkcyan',
}

ColourTable_Dash = []
for n in range(len(ColourTable)):
    ColourTable_Dash.append(
        {
            'label': ColourTable[n],
            'value': ColourTable[n],
        }
    )

class PlotlyGraph:
    def __init__(self, x1="", x2="", x3="", x4="", x5="", x6="", x7="",
                 y1="", y2="", y3="", y4="", y5="", y6="", y7="",
                 x1Name="", x2Name="", x3Name="", x4Name="", x5Name="", x6Name="", x7Name="",
                 y1Name="", y2Name="", y3Name="", y4Name="", y5Name="", y6Name="", y7Name="",
                 x1Unit="", x2Unit="", x3Unit="", x4Unit="", x5Unit="", x6Unit="", x7Unit="",
                 y1Unit="", y2Unit="", y3Unit="", y4Unit="", y5Unit="", y6Unit="", y7Unit="",
                 y1Colour=ColourTable[0], y2Colour=ColourTable[1], y3Colour=ColourTable[2], y4Colour=ColourTable[3], y5Colour=ColourTable[4], y6Colour=ColourTable[5], y7Colour=ColourTable[11],
                 Mode="Histogram",
                 Title="", Title_Size=20, Title_Colour=ColourTable[7],
                 Scale_X="Linear", Scale_Y="Linear",
                 x1_LowerLimit="", x1_UpperLimit="",
                 x2_LowerLimit="", x2_UpperLimit="",
                 x1_LowerLimitColour=ColourTable[2], x1_UpperLimitColour=ColourTable[3],
                 x2_LowerLimitColour=ColourTable[0], x2_UpperLimitColour=ColourTable[1],
                 Vertical_Range_Lower="", Vertical_Range_Upper="",
                 Horizontal_Range_Lower="", Horizontal_Range_Upper=""):
        self.x_data = {0: x1, 1: x2, 2: x3, 3: x4, 4: x5, 5: x6, 6: x7}
        self.x1 = x1; self.x2 = x2; self.x3 = x3; self.x4 = x4; self.x5 = x5; self.x6 = x6; self.x7 = x7
        self.x1Name = x1Name; self.x2Name = x2Name; self.x3Name = x3Name; self.x4Name = x4Name; self.x5Name = x5Name; self.x6Name = x6Name; self.x7Name = x7Name
        self.x1Unit = x1Unit; self.x2Unit = x2Unit; self.x3Unit = x3Unit; self.x4Unit = x4Unit; self.x5Unit = x5Unit; self.x6Unit = x6Unit; self.x7Unit = x7Unit

        self.y_data = {0: y1, 1: y2, 2: y3, 3: y4, 4: y5, 5: y6, 6: y7}
        self.y1 = y1; self.y2 = y2; self.y3 = y3; self.y4 = y4; self.y5 = y5; self.y6 = y6; self.y7 = y7
        self.y1Name = y1Name; self.y2Name = y2Name; self.y3Name = y3Name; self.y4Name = y4Name; self.y5Name = y5Name; self.y6Name = y6Name; self.y7Name = y7Name
        self.y1Unit = y1Unit; self.y2Unit = y2Unit; self.y3Unit = y3Unit; self.y4Unit = y4Unit; self.y5Unit = y5Unit; self.y6Unit = y6Unit; self.y7Unit = y7Unit
        self.y1Colour = y1Colour; self.y2Colour = y2Colour; self.y3Colour = y3Colour; self.y4Colour = y4Colour; self.y5Colour = y5Colour; self.y6Colour = y6Colour; self.y7Colour = y7Colour

        self.Title = Title; self.Title_Size = Title_Size; self.Title_Colour = Title_Colour

        self.Scale_X = Scale_X; self.Scale_Y = Scale_Y

        self.LowerLimit ={}; self.UpperLimit={}
        self.LowerLimit[0] = x1_LowerLimit
        self.LowerLimit[1] = x2_LowerLimit
        self.UpperLimit[0] = x1_UpperLimit
        self.UpperLimit[1] = x2_UpperLimit

        self.Vertical_Range_Lower = Vertical_Range_Lower
        self.Vertical_Range_Upper = Vertical_Range_Upper

        self.Horizontal_Range_Upper = Horizontal_Range_Upper
        self.Horizontal_Range_Lower = Horizontal_Range_Lower

        self.LowerLimitColour = {0: x1_LowerLimitColour, 1: x2_LowerLimitColour}

        self.UpperLimitColour = {0: x1_UpperLimitColour, 1: x2_UpperLimitColour}

        self.DataCleaner()

        if Mode == "Histogram":
            self.CPKCalculator()
            self.Histogram = go.Figure()
            self.Table = go.Figure()
            self.HistogramGenerator()

        if Mode == "Histogram_2D":
            self.Histogram = go.Figure()
            self.Table = go.Figure()
            self.CPKCalculator_2D()
            self.HistogramGenerator_2D()

        if Mode == "Scatter":
            self.XY_Graph = go.Figure()
            self.ScatterGenerator()

    def DataCleaner(self):
        for n in range(len(self.y_data.keys())):    #Number of data x1 - x7
            temp_x = self.x_data[n]
            temp_y = self.y_data[n]
            for i in reversed(range(len(self.y_data[n]))):
                if type(self.x_data[n][i]) != float and type(self.x_data[n][i]) != int:
                    del temp_y[i]
                    del temp_x[i]
            self.x_data[n] = temp_x
            self.y_data[n] = temp_y

        if self.x1 != "": self.x1 = self.x_data[0]
        if self.x2 != "": self.x2 = self.x_data[1]
        if self.x3 != "": self.x3 = self.x_data[2]
        if self.x4 != "": self.x4 = self.x_data[3]
        if self.x5 != "": self.x5 = self.x_data[4]
        if self.x6 != "": self.x6 = self.x_data[5]
        if self.x7 != "": self.x7 = self.x_data[6]

        if self.y1 != "": self.y1 = self.y_data[0]
        if self.y2 != "": self.y2 = self.y_data[1]
        if self.y3 != "": self.y3 = self.y_data[2]
        if self.y4 != "": self.y4 = self.y_data[3]
        if self.y5 != "": self.y5 = self.y_data[4]
        if self.y6 != "": self.y6 = self.y_data[5]
        if self.y7 != "": self.y7 = self.y_data[6]

    def UnitConverter(self, Values_list, Unit):
        Digits = 6
        New_Valuelist = []
        New_Unitlist = []
        for Value in Values_list:
            absValue = abs(Value)
            if absValue >= pow(10, -15) and absValue < (pow(10, -12)):
                New_Valuelist.append(round(Value / pow(10, -15), Digits))
                New_Unitlist.append('f' + Unit)

            elif absValue >= pow(10, -12) and absValue < (pow(10, -9)):
                New_Valuelist.append(round(Value / pow(10, -12), Digits))
                New_Unitlist.append('p' + Unit)

            elif absValue >= pow(10, -9) and absValue < (pow(10, -6)):
                New_Valuelist.append(round(Value / pow(10, -9), Digits))
                New_Unitlist.append('n' + Unit)

            elif absValue >= pow(10, -6) and absValue < (pow(10, -3)):
                New_Valuelist.append(round(Value / pow(10, -6), Digits))
                New_Unitlist.append("\u03BC" + Unit)

            elif absValue >= pow(10, -3) and absValue < (pow(10, 0)):
                New_Valuelist.append(round(Value / pow(10, -3), Digits))
                New_Unitlist.append("m" + Unit)

            elif absValue >= pow(10, 0) and absValue < (pow(10, 3)):
                New_Valuelist.append(round(Value / pow(10, 0), Digits))
                New_Unitlist.append("" + Unit)

            elif absValue >= pow(10, 3) and absValue < (pow(10, 6)):
                New_Valuelist.append(round(Value / pow(10, 3), Digits))
                New_Unitlist.append("k" + Unit)

            elif absValue >= pow(10, 6) and absValue < (pow(10, 9)):
                New_Valuelist.append(round(Value / pow(10, 6), Digits))
                New_Unitlist.append("M" + Unit)

            elif absValue >= pow(10, 9) and absValue < (pow(10, 12)):
                New_Valuelist.append(round(Value / pow(10, 9), Digits))
                New_Unitlist.append("G" + Unit)

            elif absValue >= pow(10, 12) and absValue < (pow(10, 15)):
                New_Valuelist.append(round(Value / pow(10, 12), Digits))
                New_Unitlist.append("T" + Unit)

        return [New_Valuelist, New_Unitlist]

    def ScatterGenerator(self):
        starttime = time.time()
        if self.y1 != "":
            [x1, x1Units] = self.UnitConverter(self.x1, self.x1Unit)
            [y1, y1Units] = self.UnitConverter(self.y1, self.y1Unit)
            self.XY_Graph.add_trace(
                go.Scatter(
                    showlegend=True,
                    x=np.array(self.x1),
                    y=np.array(self.y1),
                    text=[f'{self.x1Name}: {Freq:0.4f} {x1Unit} <br>{self.y1Name}: {y1Value:0.4f} {y1Unit}' for [Freq, y1Value, x1Unit, y1Unit] in zip(x1, y1, x1Units, y1Units)],
                    hoverinfo="text",
                    name= self.y1Name,
                    line = dict(color=self.y1Colour),
                )
            )
        if self.y2 != "":
            [x2, x2Units] = self.UnitConverter(self.x2, self.x2Unit)
            [y2, y2Units] = self.UnitConverter(self.y2, self.y2Unit)
            self.XY_Graph.add_trace(
                go.Scatter(
                    showlegend=True,
                    x=np.array(self.x2),
                    y=np.array(self.y2),
                    text=[f'{self.x2Name}: {Freq:0.4f} {x2Unit} <br>{self.y2Name}: {y2Value:0.4f} {y2Unit}' for  [Freq, y2Value, x2Unit, y2Unit] in zip(x2, y2, x2Units, y2Units)],
                    hoverinfo="text",
                    name=self.y2Name,
                    line=dict(color=self.y2Colour),
                )
            )
        if self.y3 != "":
            [x3, x3Units] = self.UnitConverter(self.x3, self.x3Unit)
            [y3, y3Units] = self.UnitConverter(self.y3, self.y3Unit)
            self.XY_Graph.add_trace(
                go.Scatter(
                    showlegend=True,
                    x=np.array(self.x3),
                    y=np.array(self.y3),
                    text=[f'{self.x3Name}: {Freq:0.4f} {x3Unit} <br>{self.y3Name}: {y3Value:0.4f} {y3Unit}' for [Freq, y3Value, x3Unit, y3Unit] in zip(x3, y3, x3Units, y3Units)],
                    hoverinfo="text",
                    name=self.y3Name,
                    line=dict(color=self.y3Colour),
                )
            )
        if self.y4 != "":
            [x4, x4Units] = self.UnitConverter(self.x4, self.x4Unit)
            [y4, y4Units] = self.UnitConverter(self.y4, self.y4Unit)
            self.XY_Graph.add_trace(
                go.Scatter(
                    showlegend=True,
                    x=np.array(self.x4),
                    y=np.array(self.y4),
                    text=[f'{self.x4Name}: {Freq:0.4f} {x4Unit} <br>{self.y4Name}: {y4Value:0.4f} {y4Unit}' for
                          [Freq, y4Value, x4Unit, y4Unit] in zip(x4, y4, x4Units, y4Units)],
                    hoverinfo="text",
                    name=self.y4Name,
                    line=dict(color=self.y4Colour),
                    )
                )
        if self.y5 != "":
            [x5, x5Units] = self.UnitConverter(self.x5, self.x5Unit)
            [y5, y5Units] = self.UnitConverter(self.y5, self.y5Unit)
            self.XY_Graph.add_trace(
                go.Scatter(
                    showlegend=True,
                    x=np.array(self.x5),
                    y=np.array(self.y5),
                    text=[f'{self.x5Name}: {Freq:0.4f} {x5Unit} <br>{self.y5Name}: {y5Value:0.4f} {y5Unit}' for
                          [Freq, y5Value, x5Unit, y5Unit] in zip(x5, y5, x5Units, y5Units)],
                    hoverinfo="text",
                    name=self.y5Name,
                    line=dict(color=self.y5Colour),
                )
            )
        if self.y6 != "":
            [x6, x6Units] = self.UnitConverter(self.x6, self.x6Unit)
            [y6, y6Units] = self.UnitConverter(self.y6, self.y6Unit)
            self.XY_Graph.add_trace(
                go.Scatter(
                    showlegend=True,
                    x=np.array(self.x6),
                    y=np.array(self.y6),
                    text=[f'{self.x6Name}: {Freq:0.4f} {x6Unit} <br>{self.y6Name}: {y6Value:0.4f} {y6Unit}' for
                          [Freq, y6Value, x6Unit, y6Unit] in zip(x6, y6, x6Units, y6Units)],
                    hoverinfo="text",
                    name=self.y6Name,
                    line=dict(color=self.y6Colour),
                )
            )
        if self.y7 != "":
            [x7, x7Units] = self.UnitConverter(self.x7, self.x7Unit)
            [y7, y7Units] = self.UnitConverter(self.y7, self.y7Unit)
            self.XY_Graph.add_trace(
                go.Scatter(
                    showlegend=True,
                    x=np.array(self.x7),
                    y=np.array(self.y7),
                    text=[f'{self.x7Name}: {Freq:0.4f} {x7Unit} <br>{self.y7Name}: {y7Value:0.4f} {y7Unit}' for
                          [Freq, y7Value, x7Unit, y7Unit] in zip(x7, y7, x7Units, y7Units)],
                    hoverinfo="text",
                    name=self.y7Name,
                    line=dict(color=self.y7Colour),
                )
            )

        self.XY_Graph.update_layout(
            title={
                'text': self.Title,
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'color' :self.Title_Colour}})
        self.XY_Graph.update_layout(hovermode="x")
        #self.XY_Graph['layout']['yaxis'].update(range=[self.Vertical_Range_Lower, self.Vertical_Range_Upper], dtick=5)#, autorange=False)
        self.XY_Graph['layout']['xaxis'].update(range=[self.Horizontal_Range_Lower, self.Horizontal_Range_Upper])

        if self.Scale_X == "Linear":
            Scale_X = None
        elif self.Scale_X == "Log":
            Scale_X = "log"

        self.XY_Graph.update_xaxes(
                title_text="{} {}".format(self.x1Name,self.x1Unit),
                type=Scale_X,
                exponentformat="SI",
        )

        if self.Scale_Y == "Linear":
            Scale_Y = None
        elif self.Scale_Y == "Log":
            Scale_Y = "log"
        self.XY_Graph.update_yaxes(
            title_text="{}".format(self.y1Unit),
            type=Scale_Y,
            exponentformat="SI",
        )
        self.XY_Graph.update_layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=True
                ),
            )
        )
        self.Plotly_Result = self.XY_Graph
        #self.XY_Graph["layout"]["sliders"] = [self.SliderSetting(FrameData=self.x1)]
        elapstedtime = time.time() - starttime
        print("Scatter Graph Data was generated in {:.3}s".format(elapstedtime))
        textwriter("Scatter Graph Data was generated in {:.3}s".format(elapstedtime))

    def DataLengthCounter(self,data):
        Count = 0
        for n in range(len(data)):
            if type(data[n]) == list:
                Count +=1
        return Count

    def CPKCalculator(self):
        starttime = time.time()
        self.CP_Value = {}
        self.K_Value = {}
        self.CPK_Value ={}
        self.Rate_Below={}
        self.Rate_Above={}

        DataLenght = self.DataLengthCounter(self.x_data)
        for n in range(DataLenght):
            if (self.UpperLimit[n] != None) and (self.LowerLimit[n] != None):
                try:
                    self.CP_Value[n] = (self.UpperLimit[n] - self.LowerLimit[n]) / (6 * np.std(self.x_data[n]))
                    self.K_Value[n] = abs(((self.UpperLimit[n] + self.LowerLimit[n]) / 2) - np.mean(self.x_data[n])) / (
                                    (self.UpperLimit[n] - self.LowerLimit[n]) / 2)
                except:
                    self.CP_Value[n] = '-'
                    self.K_Value[n] ='-'

                try:
                    self.CPK_Value[n] = (1 - self.K_Value[n]) * self.CP_Value[n]
                except:
                    self.CPK_Value[n] ='-'

                try:
                    self.Rate_Below[n] = norm.cdf(self.LowerLimit[n], np.mean(self.x_data[n]), np.std(self.x_data[n]))
                except:
                    self.Rate_Below[n] = '-'

                try:
                    self.Rate_Above[n] = 1 - norm.cdf(self.UpperLimit[n], np.mean(self.x_data[n]), np.std(self.x_data[n]))
                except:
                    self.Rate_Above[n] = '-'

            elif (self.UpperLimit[n] != None):
                self.CP_Value[n] = '-'
                self.CPK_Value[n] = '-'
                try:
                    self.Rate_Above[n] = 1 - norm.cdf(self.UpperLimit[n], np.mean(self.x_data[n]), np.std(self.x_data[n]))
                except:
                    self.Rate_Above[n] = '-'
                self.Rate_Below[n] = '-'

            elif (self.LowerLimit[n] != None):
                try:
                    self.Rate_Below[n] = norm.cdf(self.LowerLimit[n], np.mean(self.x_data[n]), np.std(self.x_data[n]))
                except:
                    self.Rate_Below[n] = '-'
                self.CP_Value[n] = '-'
                self.CPK_Value[n] = '-'
                self.Rate_Above[n] = '-'

            else:
                self.CP_Value[n] = '-'
                self.CPK_Value[n] = '-'
                self.Rate_Below[n] = '-'
                self.Rate_Above[n] = '-'

        elapstedtime = time.time() - starttime
        print("CPK Data Table was generated in {:.3}s".format(elapstedtime))
        textwriter("CPK Data Table was generated in {:.3}s".format(elapstedtime))

    def CPKCalculator_2D(self):
        starttime = time.time()
        self.TableData = {}

        self.CP_Value = {}
        self.K_Value = {}
        self.CPK_Value ={}
        self.Rate_Below={}
        self.Rate_Above={}
        for n in range(2):
            if (self.UpperLimit[n] != None) and (self.LowerLimit[n] != None):
                try:
                    self.CP_Value[n] = (self.UpperLimit[n] - self.LowerLimit[n]) / (6 * np.std(self.x_data[n]))
                    self.K_Value[n] = abs(((self.UpperLimit[n] + self.LowerLimit[n]) / 2) - np.mean(self.x_data[n])) / (
                                    (self.UpperLimit[n] - self.LowerLimit[n]) / 2)
                except:
                    self.CP_Value[n] = '-'
                    self.K_Value[n] ='-'

                try:
                    self.CPK_Value[n] = (1 - self.K_Value[n]) * self.CP_Value[n]
                except:
                    self.CPK_Value[n] ='-'

                try:
                    self.Rate_Below[n] = norm.cdf(self.LowerLimit[n], np.mean(self.x_data[n]), np.std(self.x_data[n]))
                except:
                    self.Rate_Below[n] = '-'

                try:
                    self.Rate_Above[n] = 1 - norm.cdf(self.UpperLimit[n], np.mean(self.x_data[n]), np.std(self.x_data[n]))
                except:
                    self.Rate_Above[n] = '-'

            elif (self.UpperLimit[n] != None):
                self.CP_Value[n] = '-'
                self.CPK_Value[n] = '-'
                try:
                    self.Rate_Above[n] = 1 - norm.cdf(self.UpperLimit[n], np.mean(self.x_data[n]), np.std(self.x_data[n]))
                except:
                   self.Rate_Above[n] = '-'
                self.Rate_Below[n] = '-'

            elif (self.LowerLimit[n] != None):
                try:
                    self.Rate_Below[n] = norm.cdf(self.LowerLimit[n], np.mean(self.x_data[n]), np.std(self.x_data[n]))
                except:
                    self.Rate_Below[n] = '-'
                self.CP_Value[n] = '-'
                self.CPK_Value[n] = '-'
                self.Rate_Above[n] = '-'

            else:
                self.CP_Value[n] = '-'
                self.CPK_Value[n] = '-'
                self.Rate_Below[n] = '-'
                self.Rate_Above[n] = '-'
        self.TableData['CP_Value'] = self.CP_Value
        self.TableData['CPK_Value'] = self.CPK_Value
        self.TableData['Rate_Below'] = self.Rate_Below
        self.TableData['Rate_Above'] = self.Rate_Above

        elapstedtime = time.time() - starttime
        print("CPK Data Table was generated in {:.3}s".format(elapstedtime))
        textwriter("CPK Data Table was generated in {:.3}s".format(elapstedtime))

    def HistogramGenerator(self):
        starttime = time.time()
        try:
            DataRange = max(self.x1) - min(self.x1)
        except:
            DataRange = 0

        Range = (DataRange)/20

        if self.x1 != '':
            self.counts, self.bins = np.histogram(self.x1,
                                        bins=np.arange(
                                            (min(self.x1) - 0.5 * DataRange),
                                            (max(self.x1) + 0.5 * DataRange),
                                            Range)
                                        )

        mu = np.mean(self.x1)
        sigma = np.std(self.x1)

        #sigma_line = 100*((1/np.sqrt(2*np.pi*sigma*sigma))*np.exp(-1*((bins-mu)**2)/(2*sigma*sigma)))
        self.pdf_line = 100 * norm.pdf(x=self.bins, loc=mu, scale=sigma)
        self.cdf_line = 100 * norm.cdf(x=self.bins, loc=mu, scale=sigma)

        color = np.array(['rgb(10,10,255)'] * self.bins.shape[0])
        if self.LowerLimit[0] != '' and self.LowerLimit[0] != None:
            color[self.bins < self.LowerLimit[0]] = self.LowerLimitColour[0]

        if self.UpperLimit[0] != '' and self.UpperLimit[0] != None:
            color[self.bins > self.UpperLimit[0]] = self.UpperLimitColour[0]


        self.Histogram.add_trace(  # dammy for Frame
            go.Scatter(
                showlegend=False,
                x=np.array(self.bins[0]),
                y=np.array(self.pdf_line[0]),
                name='Viewing Data' + ': ' + 'pdf',
                mode="markers",
                marker=dict(size=15, ),
                xaxis='x1',
                yaxis='y2',
                line=dict(color=ColourTable[1]),
            ),
        )

        self.Histogram.add_trace(  # dammy for Frame
            go.Scatter(
                showlegend=False,
                x=np.array(self.bins[0]),
                y=np.array(self.cdf_line[0]),
                name='Viewing Data' + ': ' + 'cdf',
                mode="markers",
                marker=dict(size=15, ),
                xaxis='x1',
                yaxis='y2',
                line=dict(color=ColourTable[2]),
            ),
        )


        self.Histogram.add_trace(
            go.Bar(
                showlegend=False,
                x=self.bins,
                y=self.counts,
                marker=dict(color=color.tolist()),
                name = self.x1Name,
                xaxis='x1',
                yaxis='y1',
                marker_color=self.y1Colour,
            )
        )

        self.Histogram.add_trace(
            go.Scatter(
                showlegend=False,
                x=np.array(self.bins),
                y=np.array(self.pdf_line),
                xaxis='x1',
                yaxis='y2',
                name= 'line',
                line = dict(color=ColourTable[1]),
            )
        )

        self.Histogram.add_trace(
            go.Scatter(
                showlegend=False,
                x=np.array(self.bins),
                y=np.array(self.cdf_line),
                xaxis='x1',
                yaxis='y2',
                name= 'line',
                line = dict(color=ColourTable[2]),
            )
        )

        layout = go.Layout(xaxis=dict(title=self.x1Name),
                           yaxis=dict(title='Count',
                                      side='left',
                                      showgrid=False,
                                      range=[0, np.max(self.Histogram.data[0].y)],
                                      ),
                           yaxis2=dict(title='Probability density',
                                       side='right',
                                       overlaying='y',
                                       showgrid=False,
                                       range=[0, np.max(self.Histogram.data[3].y)],
                                       )
                           )
        self.Histogram.layout = layout

        self.Histogram["layout"]["sliders"] = [self.SliderSetting(self.bins)]
        #self.Histogram.show()

        self.TableGenerator()

        self.Plotly_Result = make_subplots(rows=1, cols=3,
                                      shared_xaxes=False,
                                      subplot_titles=("Histogram", "", "Parameters"),
                                      specs=[[{"type": "xy", "colspan": 2, "secondary_y": True}, {"type": "scatter"},
                                              {"type": "table"}],
                                             ]
                                      )

        # dummy trace
        for n in range(0, 2):
            self.Plotly_Result.add_trace(self.Histogram["data"][n], row=1, col=1, secondary_y=True)

        # count trace
        self.Plotly_Result.add_trace(self.Histogram["data"][2], row=1, col=1, )

        # sigma lines
        for n in range(3, 5):
            self.Plotly_Result.add_trace(self.Histogram["data"][n], row=1, col=1, secondary_y=True)

        self.Plotly_Result["data"][3]["line"]["dash"] = 'dash'
        self.Plotly_Result["data"][4]["line"]["dash"] = 'dot'
        self.Plotly_Result.layout.bargap = 0.1
        self.Plotly_Result.layout.yaxis.title.text = "Count"
        self.Plotly_Result.layout.yaxis2.showgrid = False
        self.Plotly_Result.layout.yaxis2.title.text = "Probability density [%]"

        self.Plotly_Result.add_trace(self.Table["data"][0], row=1, col=3, )

        #Label_array = np.array(self.bins).astype("|S5")
        Label_array = []
        for n in self.bins:
            Label_array.append('{:.3}'.format(n))

        # Plotly_Result["layout"]["sliders"] = [Graphs.SliderSetting(Graphs.bins)]
        self.Plotly_Result["layout"]["sliders"] = [self.SliderSetting(Label_array)]

        if self.y1Colour == '':
            self.y1Colour = ColourTable[0]

        self.Plotly_Result["frames"] = [
            go.Frame(
                data=[
                    ### Graph Plot #1 ###
                    go.Scatter(
                        visible=True,
                        x=[self.bins[n]],
                        y=[self.pdf_line[n]],
                        text=f'X: {self.bins[n]:0.3f}<br>Normal PDF: {self.pdf_line[n]:0.3f}%',
                        hoverinfo='text',
                        mode="markers",
                        marker=dict(size=15, ),
                        xaxis='x1',
                        yaxis='y2',
                        line=dict(color=ColourTable[1]),
                    ),
                    go.Scatter(
                        visible=True,
                        x=[self.bins[n]],
                        y=[self.cdf_line[n]],
                        text=f'X: {self.bins[n]:0.3f}<br>Normal CDF: {self.cdf_line[n]:0.3f}%',
                        hoverinfo='text',
                        mode="markers",
                        marker=dict(size=15, ),
                        xaxis='x1',
                        yaxis='y2',
                        line=dict(color=ColourTable[2]),
                    ),
                    go.Bar(
                        showlegend=False,
                        x=[bin for bin in self.bins],
                        y=[count for count in self.counts],
                        marker=dict(color="blue"),
                        name=self.x1Name,
                        xaxis='x1',
                        yaxis='y1',
                        marker_color=self.y1Colour,
                    ),

                ],
                name='{}'.format(Label_array[n])
            ) for n in range(len(self.bins))
        ]

        if self.Title_Size == '':
            self.Title_Size = 20
        ## Layout update
        self.Plotly_Result.update_layout(
            title=dict(
                text=self.Title,
                x=0.5,
                font= dict(color=self.Title_Colour)
            ),
            title_font=dict(
                size=int(self.Title_Size),
            ),
        )

        # ymax = 0
        # data_axis = 0
        # for n in range(len(Graphs.Histogram["data"])):
        #     if max(Graphs.Histogram.data[n].y) > ymax:
        #         ymax = max(Graphs.Histogram.data[n].y)
        #         data_axis = n

        if self.LowerLimit != None:
            self.Plotly_Result.add_shape(
                type='line',
                line=dict(color="red"),
                x0=self.LowerLimit,
                y0=0,
                x1=self.LowerLimit,
                y1=max(self.Histogram.data[2].y) + 0.07 * max(self.Histogram.data[2].y),
            )

            if self.LowerLimit[0] != '':
                self.Plotly_Result.add_annotation(
                    x=self.LowerLimit,
                    y=max(self.Histogram.data[2].y) + 0.1 * max(self.Histogram.data[2].y),
                    text="Lower Limit = {:,.2f}".format(self.LowerLimit[0]),
                    showarrow=False,
                    arrowhead=2,
                    font=dict(
                        color="red",
                        size=15
                    ),
                )

        if self.UpperLimit[0] != None:
            self.Plotly_Result.add_shape(
                type='line',
                line=dict(color="green"),
                x0=self.UpperLimit[0],
                y0=0,
                x1=self.UpperLimit[0],
                y1=max(self.Histogram.data[2].y) + 0.07 * max(self.Histogram.data[2].y),
            )

            if self.UpperLimit[0] != '':
                self.Plotly_Result.add_annotation(
                    x=self.UpperLimit[0],
                    y=max(self.Histogram.data[2].y) + 0.1 * max(self.Histogram.data[2].y),
                    text="Upper Limit = {:,.2f}".format(self.UpperLimit[0]),
                    showarrow=False,
                    arrowhead=2,
                    font=dict(
                        color="green",
                        size=15
                    ),
                )
        elapstedtime = time.time() - starttime
        print("Histogram Graph Data was generated in {:.3}s".format(elapstedtime))
        textwriter("Histogram Graph Data was generated in {:.3}s".format(elapstedtime))

    def CustomDataGenerator_2D(self,Bin1,Bin2,Data1,Data2,CDF1,CDF2,**kwargs):
        TempDict = {}
        Array_2D = []
        TempArray = []
        Data1_Count = []
        Data2_Count = []
        # for key, values in kwargs.items():
        # for n in range(len(Data1)):
        #     for m in range(len(Data2)):
        Data1Total = len(Data1)
        Data2Total = len(Data2)

        for n in range(len(Bin1)):
            custom1 = []
            for m in range(len(Bin2)):
                Data1_Count = sum(1 for x in Data1 if x < Bin1[n])
                Data2_Count = sum(1 for y in Data2 if y < Bin2[m])
                Cond_Data1_Count = sum(1 for x,y in zip(Data1, Data2) if ((x < Bin1[n]) and (y < Bin2[m])))
                custom1.append([self.x1Name,
                                self.x2Name,
                                self.x1Unit,
                                self.x2Unit,
                                Data1_Count,
                                CDF1[n],
                                Data2_Count,
                                CDF2[m],
                                Cond_Data1_Count,
                                100*Cond_Data1_Count/Data1Total,
                                ])
            TempArray.append(custom1)

        Array_2D.append(TempArray)
            # Array_2D = np.full((len(Data1[0]), len(Data2[0])), values).tolist()
            #Array_2D = [[values for i in range(len(Data1))] for j in range(len(Data2))]
        #TempDict[key] = Array_2D
        return np.array(Array_2D)#TempDict

    def HistogramGenerator_2D(self):
        starttime = time.time()
        DataRange = {}

        ### ------------------------
        self.Plotly_Result = make_subplots(rows=3, cols=2,
                                      shared_xaxes=False,
                                      subplot_titles=("Histogram", "Cumulative Probability", "Parameters"),
                                      specs=[[{"type":'xy',"rowspan":2},{"type":'surface',"rowspan":2}],
                                             [None,None],
                                             [{"type":"table","colspan":2},None],
                                            ],
                                      horizontal_spacing=0.05,
                                      vertical_spacing=0.05,
                                      )
        ### ------------------------

        try:
            DataRange[0] = max(self.x1) - min(self.x1)
        except:
            DataRange[0] = 0

        try:
            DataRange[1] = max(self.x2) - min(self.x2)
        except:
            DataRange[1] = 0

        Range = {}; counts = {}; bins = {}; mu = {}; sigma= {}
        pdf_line ={}; cdf_line ={}

        for n in range(self.DataLengthCounter(self.x_data)):
            Range[n] = (DataRange[n])/20

            counts[n], bins[n] = np.histogram(self.x_data[n],
                                        bins=np.arange(
                                            (min(self.x_data[n]) - 0.25 * DataRange[n]),
                                            (max(self.x_data[n]) + 0.25 * DataRange[n]),
                                            Range[n])
                                        )

            mu[n] = np.mean(self.x_data[n])
            sigma[n] = np.std(self.x_data[n])

            pdf_line[n] = 100 * norm.pdf(x=bins[n], loc=mu[n], scale=sigma[n])
            cdf_line[n] = 100 * norm.cdf(x=bins[n], loc=mu[n], scale=sigma[n])


            color = np.array(['rgb(10,10,255)'] * bins[n].shape[0])
            if self.LowerLimit[n] != '' and self.LowerLimit[n] != None:
                color[bins[n] < self.LowerLimit[n]] = self.LowerLimitColour[n]

            if self.UpperLimit[n] != '' and self.UpperLimit[n] != None:
                color[bins[n] > self.UpperLimit[n]] = self.UpperLimitColour[n]


        z_data = []
        for x in range(len(cdf_line[0])):
            for y in range(len(cdf_line[1])):
                z_data.append(cdf_line[0][x] * cdf_line[1][y] / 100)
        z_data_np = np.array(z_data)
        z_data_np = z_data_np.reshape(len(cdf_line[0]),len(cdf_line[1]))

        x_data = bins[0].tolist()
        y_data = bins[1].tolist()
        Customdata = self.CustomDataGenerator_2D(x_data,    # X Axis Range
                                                 y_data,    # Y Axis Range
                                                 self.x1,   # X Raw Data
                                                 self.x2,   # Y Raw Data
                                                 cdf_line[0],   # X CDF line Data
                                                 cdf_line[1],   # Y CDF Line Data
                                                 )

        self.CDF_Graph_3D = go.Figure()

        self.CDF_Graph_3D.add_trace(
            go.Surface(
                contours={
                    "x": {"show": True,
                          "start": (min(self.x_data[0]) - 0.5 * DataRange[0]),
                          "end": (max(self.x_data[0]) + 0.5 * DataRange[0]),
                          "size": DataRange[0],
                          "color": "white"
                          },
                    "y": {"show": True,
                          "start": (min(self.x_data[1]) - 0.5 * DataRange[1]),
                          "end": (max(self.x_data[1]) + 0.5 * DataRange[1]),
                          "size": DataRange[1],
                          "color": "white"
                          },
                    "z": {"show": True,
                          "start": 0,
                          "end": 100,
                          },
                },
                x=bins[0],
                y=bins[1],
                z=z_data_np,
                showscale=False,
                customdata = Customdata[0].tolist(),
                hovertemplate = "%{customdata[0]} (x): %{x} %{customdata[2]}<br>" + \
                                "%{customdata[1]} (y): %{y} %{customdata[3]}<br>" + \
                                "P(x)*P(y) (z): %{z:.3f} %<br>" + \
                                "P(x) : %{customdata[5]:.3f} %<br>" + \
                                "P(y) : %{customdata[7]:.3f} %<br>" + \
                                "---------------------------------<br>" + \
                                "P(x|y): %{customdata[9]:.3f} %<br>" + \
                                "Count(x): %{customdata[4]}<br>" + \
                                "Count(y): %{customdata[6]}<br>" +\
                                "Count(x&y): %{customdata[8]}<br>",
                name = ''
            )
        )

        xaxis_title = 'x: ' + str(self.x1Name)
        if self.x1Unit != '':
            xaxis_title += ' [' +str(self.x1Unit) +']'

        yaxis_title = 'y: ' + str(self.x2Name)
        if self.x2Unit != '':
            yaxis_title +=  ' [' +str(self.x2Unit) +']'

        self.CDF_Graph_3D.update_layout(
            scene = dict(
                xaxis = dict(title=xaxis_title,
                             nticks=10),    # Xaxis ticks
                yaxis = dict(title=yaxis_title,
                             nticks=10),    # Yaxis ticks
                zaxis = dict(title="Cumulative Probability [%]",
                             nticks=10),    # Zaxis ticks
            ),
            scene_camera = dict(
                eye=dict(x=-1.5, y=-1.5, z=0.7)   # Camera Position
            ),
        )

        x = self.x_data[0] #x_data
        y = self.x_data[1] #y_data

        self.TableGenerator_2D()

        self.Plotly_Result.add_trace(
            go.Histogram2dContour(
                x=x,
                y=y,
                colorscale='Plasma',
                reversescale=False,
                xaxis='x',
                yaxis='y',
                name='',
                colorbar=dict(len=0.45, y=0.59, x=0.5),
                customdata = Customdata[0].tolist(),
                hovertemplate = "%{customdata[0]} (x): %{x} %{customdata[2]}<br>" + \
                                "%{customdata[1]} (y): %{y} %{customdata[3]}<br>" + \
                                "Count (z): %{z} <br>"

        ),
            col=1,
            row=1,
        )

        self.Plotly_Result.add_trace(
            go.Scatter(
                hoverinfo='skip',
                showlegend=False,
                x=x,
                y=y,
                xaxis='x',
                yaxis='y',
                mode='markers',
                marker=dict(
                    symbol='x',
                    opacity=0.7,
                    color='white',
                    size=8,
                    line=dict(width=1),
                ),
                name=''
            ),
            col=1,
            row=1,
        )
        self.Plotly_Result.add_trace(
            go.Histogram(
                showlegend=False,
                xaxis='x2',
                y=y,
                marker=dict(
                    color=self.y1Colour,
                    #color='rgba(0,0,0,1)'
                ),
                name='',
                hovertemplate = '<i>Range</i>:' + '%{y}' + '<extra></extra><br>' +
                                '<i>Count<i>:' + '%{x}'
            ),
            col=1,
            row=1,
        )
        self.Plotly_Result.add_trace(
            go.Histogram(
                showlegend=False,
                x=x,
                yaxis='y2',
                marker=dict(
                    color=self.y2Colour,
                    #color='rgba(0,0,0,1)'
                ),
                name='',
                hovertemplate = '<i>Range</i>:' + '%{x}' + '<extra></extra><br>' +
                                '<i>Count<i>:' + '%{y}'

            ),
            col=1,
            row=1,
        )

        self.Plotly_Result['data'][2]['xaxis'] = 'x2'
        self.Plotly_Result['data'][2]['yaxis'] = 'y1'
        self.Plotly_Result['data'][3]['xaxis'] = 'x1'
        self.Plotly_Result['data'][3]['yaxis'] = 'y2'

        self.Plotly_Result.update_layout(
            autosize=True,
            xaxis=dict(
                zeroline=False,
                domain=[0, 0.4],
                showgrid=True
            ),
            yaxis=dict(
                zeroline=False,
                domain=[0.4, 0.8],
                showgrid=True
            ),

            xaxis2=dict(
                zeroline=False,
                domain=[0.405, 0.5],
                showgrid=True
            ),
            yaxis2=dict(
                zeroline=False,
                domain=[0.81, 0.95],
                showgrid=True
            ),
            bargap=0.1,
            hovermode='closest',
        )

        self.Plotly_Result.add_trace(self.CDF_Graph_3D['data'][0],row=1, col=2)
        self.Plotly_Result.update_layout(self.CDF_Graph_3D['layout'])#,row=1,col=3)
        self.Plotly_Result.add_trace(self.Fig_Plotly_TimeTable['data'][0],row=3,col=1)

        self.Plotly_Result.update_xaxes(title_text=xaxis_title, row=1, col=1)
        self.Plotly_Result.update_yaxes(title_text=yaxis_title, row=1, col=1)

        if self.Title_Size == '':
            self.Title_Size = 20
        self.Plotly_Result.update_layout(
            title=dict(
                text=self.Title,
                x=0.5,
                font= dict(color=self.Title_Colour)
            ),
            title_font=dict(
                size=self.Title_Size,
            ),
        )

        ##Plane Data
        # zero_pt = pd.Series([0])
        # y = zero_pt.append()

        ### Vertical Limit Line ########
        if self.LowerLimit[0] != '':
            self.Plotly_Result.add_shape(
                type='line',
                line=dict(color=self.LowerLimitColour[0]),
                #xref="x domain",
                yref="y domain",
                x0=self.LowerLimit[0],
                y0=0,
                x1=self.LowerLimit[0],
                y1=1.38,
            )
            self.Plotly_Result.add_annotation(
                yref="y domain",
                x=self.LowerLimit[0],
                y=1.47,
                text="Lower Limit = {:,.2f}".format(self.LowerLimit[0]),
                showarrow=False,
                arrowhead=2,
                font=dict(
                    color=self.LowerLimitColour[0],
                    size=15
                ),
            )

        if self.UpperLimit[0] != '':
            self.Plotly_Result.add_shape(
                    type='line',
                    line=dict(color=self.UpperLimitColour[0]),
                    # xref="x domain",
                    yref="y domain",
                    x0=self.UpperLimit[0],
                    y0=0,
                    x1=self.UpperLimit[0],
                    y1=1.38,
                )
            self.Plotly_Result.add_annotation(
                    yref="y domain",
                    x=self.UpperLimit[0],
                    y=1.47,
                    text="Upper Limit = {:,.2f}".format(self.UpperLimit[0]),
                    showarrow=False,
                    arrowhead=2,
                    font=dict(
                        color=self.UpperLimitColour[0],
                        size=15
                    ),
            )

            ### Horizontal  Limit Line ########
        if self.LowerLimit[1] != '':
            self.Plotly_Result.add_shape(
                    type='line',
                    line=dict(color=self.LowerLimitColour[1]),
                    xref="x domain",
                    #yref="y domain",
                    x0=0,
                    y0=self.LowerLimit[1],
                    x1=1.25,
                    y1=self.LowerLimit[1],
            )
            self.Plotly_Result.add_annotation(
                    xref="x domain",
                    # yref="y domain",
                    x=0.93,
                    y=self.LowerLimit[1]*1.01,
                    text="Lower Limit = {:,.2f}".format(self.LowerLimit[1]),
                    showarrow=False,
                    arrowhead=2,
                    font=dict(
                        color=self.LowerLimitColour[1],
                        size=15
                    ),
            )

        if self.UpperLimit[1] != '':
            self.Plotly_Result.add_shape(
                        type='line',
                        line=dict(color=self.UpperLimitColour[1]),
                        xref="x domain",
                        # yref="y domain",
                        x0=0,
                        y0=self.UpperLimit[1],
                        x1=1.25,
                        y1=self.UpperLimit[1],
            )
            self.Plotly_Result.add_annotation(
                        xref="x domain",
                        # yref="y domain",
                        x=0.93,
                        y=self.UpperLimit[1] * 1.01,
                        text="Upper Limit = {:,.2f}".format(self.UpperLimit[1]),
                        showarrow=False,
                        arrowhead=2,
                        font=dict(
                            color=self.UpperLimitColour[1],
                            size=15
                        ),
            )

            # if self.LowerLimit[0] != '':
            #     self.Plotly_Result.add_annotation(
            #         x=self.LowerLimit,
            #         y=max(self.Histogram.data[2].y) + 0.1 * max(self.Histogram.data[2].y),
            #         text="Lower Limit = {:,.2f}".format(self.LowerLimit[0]),
            #         showarrow=False,
            #         arrowhead=2,
            #         font=dict(
            #             color="red",
            #             size=15
            #         ),
            #     )

        #self.Plotly_Result.show()

        #print("Complete")
        elapstedtime = time.time() - starttime
        print("2D Histogram Data was generated in {:.3}s".format(elapstedtime))
        textwriter("2D Histogram Data was generated in {:.3}s".format(elapstedtime))

    def TableGenerator(self):
        TableContents_List = []

        TableContents = {}

        TableContents['Name'] = self.x1Name
        TableContents['Qty'] = len(self.x1)
        TableContents['Max'] = max(self.x1)
        TableContents['Average'] = round(np.average(self.x1),5)
        TableContents['Min'] = min(self.x1)
        try:
            TableContents['Sigma'] = round(np.std(self.x1), 5)
        except:
            TableContents['Sigma'] = '-'

        TableContents['LowerLimit'] = self.LowerLimit[0]
        TableContents['UpperLimit'] = self.UpperLimit[0]

        try:
            TableContents['CPK'] = round(self.CPK_Value,5)
        except:
            TableContents['CPK'] = '-'

        try:
            TableContents['Failure Rate:Lower [%]'] = round(self.Rate_Below[0] * 100, 3)
        except:
            TableContents['Failure Rate:Lower [%]'] = '-'

        try:
            TableContents['Failure Rate:Upper [%]'] = round(self.Rate_Above[0] * 100, 3)
        except:
            TableContents['Failure Rate:Upper [%]'] = '-'

        try:
            TableContents['Pass Rate [%]'] = round((1 -self.Rate_Below[0]-self.Rate_Above[0]) * 100, 3)
        except:
            try:
                TableContents['Pass Rate [%]'] = round((1  - self.Rate_Above[0]) * 100, 3)
            except:
                try:
                    TableContents['Pass Rate [%]'] = round((1 - self.Rate_Below[0]) * 100, 3)
                except:
                    TableContents['Pass Rate [%]'] = '-'

        TableContents_List.append(TableContents)
        TableMenu = ['Parameter', 'Values']
        Col1 = []
        Col2 = []

        for n in TableContents.keys():
            Col1.append(n)
            Col2.append(TableContents_List[0][n])

        self.Table.add_trace(
            go.Table(
                header=dict(values=TableMenu),
                cells=dict(values=[Col1, Col2]),
            ),
        )

    def TableGenerator_2D(self):
        self.CPKCalculator_2D()
        TableContents_List = []
        Count = self.DataLengthCounter(self.x_data)

        HeaderList = ['Items','Parameter #1 (x)', 'Parameter #2 (y)']
        NameList = ['Name']
        NameList.append(self.x1Name)
        NameList.append(self.x2Name)
        LowerLimitList = ['LowerLimit']
        LowerLimitList.append(self.LowerLimit[0])
        LowerLimitList.append(self.LowerLimit[1])

        UpperLimitList = ['UpperLimit']
        UpperLimitList.append(self.UpperLimit[0])
        UpperLimitList.append(self.UpperLimit[1])

        QtyList = ['Qty']
        QtyList.append(len(self.x_data[0]))
        QtyList.append(len(self.x_data[1]))

        MaxList = ['Max']
        MaxList.append(max(self.x_data[0]))
        MaxList.append(max(self.x_data[1]))

        AverageList = ['Average']
        AverageList.append(round(np.average(self.x_data[0]),5))
        AverageList.append(round(np.average(self.x_data[1]),5))

        MinList = ['Min']
        MinList.append(min(self.x_data[0]))
        MinList.append(min(self.x_data[1]))

        SigmaList = ['Sigma']
        for n in range(Count):
            try:
                SigmaList.append(round(np.std(self.x_data[n]), 5))
            except:
                SigmaList.append('-')

        CPKList = ['CPK']
        for n in range(Count):
            try:
                CPKList.append(round(self.CPK_Value[n],5))
            except:
                CPKList.append('-')

        FRLList = ['Failure Rate: Lower [%]']
        for n in range(Count):
            try:
                FRLList.append(round(self.Rate_Below[n] * 100, 3))
            except:
                FRLList.append('-')

        FRHList = ['Failure Rate: Upper [%]']
        for n in range(Count):
            try:
                FRHList.append(round(self.Rate_Above[n] * 100, 3))
            except:
                FRHList.append('-')

        PassRateList = ['Pass Rate [%]']
        for n in range(Count):
            try:
                PassRateList.append(round((1 - self.Rate_Below[n] - self.Rate_Above[n]) * 100, 3))
            except:
                try:
                    PassRateList.append(round((1 - self.Rate_Above[n]) * 100, 3))
                except:
                    try:
                        PassRateList.append(round((1 - self.Rate_Below[n]) * 100, 3))
                    except:
                        PassRateList.append('-')

        # --------------------------
        ParamTable = []
        ParamTable.append(NameList)
        ParamTable.append(QtyList)
        ParamTable.append(MaxList)
        ParamTable.append(AverageList)
        ParamTable.append(MinList)
        ParamTable.append(SigmaList)
        ParamTable.append(LowerLimitList)
        ParamTable.append(UpperLimitList)
        ParamTable.append(CPKList)
        ParamTable.append(FRLList)
        ParamTable.append(FRHList)
        ParamTable.append(PassRateList)

        # Row <-> Column -----------
        ParamTable_np = np.array(ParamTable)
        ParamTable = ParamTable_np.T
        # --------------------------

        self.Fig_Plotly_TimeTable = go.Figure()
        self.Fig_Plotly_TimeTable.add_trace(
            go.Table(
                columnwidth=20,
                header=dict(
                    values=HeaderList,
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='center'
                ),
                cells=dict(
                    values=ParamTable,
                    line_color='darkslategray',
                    fill_color='white',
                    align='center'
                )
            )
        )
        #self.Fig_Plotly_TimeTable.show()

    def SliderSetting(self,FrameData):
        try:
            return dict(
                steps=[dict(
                    method='animate',
                    args=[['{:.3}'.format(k)],  # This should match with Frame name
                          dict(mode='immediate',
                               frame=dict(duration=500, redraw=False),  # Reaction Time
                               transition=dict(duration=0),
                               )
                          ],
                    label='{:.3}'.format(k),

                ) for k in FrameData],
                transition=dict(duration=0, ),  # Moving speed
                x=0,  # slider starting position
                y=0,
                currentvalue=dict(font=dict(size=12),
                                  prefix='{}:'.format(self.xName),
                                  visible=True,
                                  xanchor='right',
                                  ),
                len=1.0,  # slider length)
            )
        except:
            return dict(
                steps=[dict(
                    method='animate',
                    args=[['{}'.format(k)],  # This should match with Frame name
                          dict(mode='immediate',
                               frame=dict(duration=500, redraw=False),  # Reaction Time
                               transition=dict(duration=0),
                               )
                          ],
                    label='{}'.format(k),# This should match with Frame name

                ) for k in FrameData],
                transition=dict(duration=0, ),  # Moving speed
                x=0,  # slider starting position
                y=0,
                currentvalue=dict(font=dict(size=12),
                                  prefix='{}:'.format(self.x1Name),
                                  visible=True,
                                  xanchor='right',
                                  ),
                len=1.0 # slider length)
            )

def CurrentLocation():
    wb = xw.Book.caller()
    cellRange = wb.app.selection
    address = cellRange.address
    rowNum = cellRange.options(ndim=2).row
    colNum = cellRange.column
    return [address,rowNum,colNum]

MODELIST = ('Histogram','Histogram_2D','Scatter','Debug')
AXISLIST = ('1st','2nd')


class ExcelGraph():
    def __init__(self,Path):
        self.Path = Path
        self.ExcelFile = xw.Book(Path)
        self.ExcelFile.set_mock_caller()

    def GetSelectedArea(self):
        self.ExcelFile = xw.Book(self.Path)
        self.ExcelFile.set_mock_caller()
        try:
            wb = self.ExcelFile.caller()
            self.cellRange = wb.app.selection
            return self.cellRange.address
        except:
            pass

    def xwRangeGet(self, Address, Exception):#, xw=None):
        self.ExcelFile = xw.Book(self.Path)
        self.ExcelFile.set_mock_caller()
        try:
            ReadResult = xw.Range(Address).value  ## Picking up from Excel case
            if "$" in Address:
                return ReadResult
            else:
                return str(Address)
        except:
            try:
                Exception = Exception.removeprefix('[')
                Exception = Exception.removesuffix(']')
                try:
                    Return = [float(i) for i in Exception.split(',')]
                    if len(Return) > 1:
                        return Return       ## Direct Number input with list format case
                    else:
                        return Return[0]    ## Direct Number input of only one number with list format case
                except:
                    try:
                        Return = [float(i) for i in Exception.split(' ')]
                        if len(Return) > 1:
                            return Return  ## Direct Number input with list format case with tab splice case
                        else:
                            return Return[0]  ## Direct Number input of only one number with list format case
                    except:
                        return float(Exception) ## Direct Number input case


            except:
                try:
                    if len(Exception) != 1:
                        return Exception    ## Direct String input case
                except:
                    return ""               ## Default blank case

    def GraphGenerate(self,Mode=MODELIST[0],
                      x1_Data_Address="",x2_Data_Address="",x3_Data_Address="",x4_Data_Address="",x5_Data_Address="",x6_Data_Address="",x7_Data_Address="",
                      x1_Name_Address="",x2_Name_Address="",x3_Name_Address="",x4_Name_Address="",x5_Name_Address="",x6_Name_Address="",x7_Name_Address="",
                      x1_Unit_Address="",x2_Unit_Address="",x3_Unit_Address="",x4_Unit_Address="",x5_Unit_Address="",x6_Unit_Address="",x7_Unit_Address="",
                      y1_Data_Address="", y2_Data_Address="", y3_Data_Address="",y4_Data_Address="",y5_Data_Address="",y6_Data_Address="",y7_Data_Address="",
                      y1_Name_Address="", y2_Name_Address="", y3_Name_Address="",y4_Name_Address="",y5_Name_Address="",y6_Name_Address="",y7_Name_Address="",
                      y1_Unit_Address="", y2_Unit_Address="", y3_Unit_Address="",y4_Unit_Address="",y5_Unit_Address="",y6_Unit_Address="",y7_Unit_Address="",
                      y1_Color="", y2_Color="", y3_Color="", y4_Color="",y5_Color="",y6_Color="", y7_Color="",
                      x1_UP_LIMIT_Address="",x2_UP_LIMIT_Address="",
                      x1_LOW_LIMIT_Address="",x2_LOW_LIMIT_Address="",
                      x_UP_VIEW_Address="", x_LOW_VIEW_Address="",
                      y_UP_VIEW_Address="", y_LOW_VIEW_Address="",
                      Title_Text_Address="",
                      Title_Size_Address="",
                      Title_Colour="",
                      Scale_X="Linear", Scale_Y = "Linear",
                      ):
        Data_x1 = self.xwRangeGet(x1_Data_Address, x1_Data_Address)
        Data_x2 = self.xwRangeGet(x2_Data_Address, x2_Data_Address)
        Data_x3 = self.xwRangeGet(x3_Data_Address, x3_Data_Address)
        Data_x4 = self.xwRangeGet(x4_Data_Address, x4_Data_Address)
        Data_x5 = self.xwRangeGet(x5_Data_Address, x5_Data_Address)
        Data_x6 = self.xwRangeGet(x6_Data_Address, x6_Data_Address)
        Data_x7 = self.xwRangeGet(x7_Data_Address, x7_Data_Address)

        Name_x1 = self.xwRangeGet(x1_Name_Address, x1_Name_Address)
        Name_x2 = self.xwRangeGet(x2_Name_Address, x2_Name_Address)
        Name_x3 = self.xwRangeGet(x3_Name_Address, x3_Name_Address)
        Name_x4 = self.xwRangeGet(x4_Name_Address, x4_Name_Address)
        Name_x5 = self.xwRangeGet(x5_Name_Address, x5_Name_Address)
        Name_x6 = self.xwRangeGet(x6_Name_Address, x6_Name_Address)
        Name_x7 = self.xwRangeGet(x7_Name_Address, x7_Name_Address)

        Unit_x1 = self.xwRangeGet(x1_Unit_Address, x1_Unit_Address)
        Unit_x2 = self.xwRangeGet(x2_Unit_Address, x2_Unit_Address)
        Unit_x3 = self.xwRangeGet(x3_Unit_Address, x3_Unit_Address)
        Unit_x4 = self.xwRangeGet(x4_Unit_Address, x4_Unit_Address)
        Unit_x5 = self.xwRangeGet(x5_Unit_Address, x5_Unit_Address)
        Unit_x6 = self.xwRangeGet(x6_Unit_Address, x6_Unit_Address)
        Unit_x7 = self.xwRangeGet(x7_Unit_Address, x7_Unit_Address)

        Data_y1 = self.xwRangeGet(y1_Data_Address, y1_Data_Address)
        Data_y2 = self.xwRangeGet(y2_Data_Address, y2_Data_Address)
        Data_y3 = self.xwRangeGet(y3_Data_Address, y3_Data_Address)
        Data_y4 = self.xwRangeGet(y4_Data_Address, y4_Data_Address)
        Data_y5 = self.xwRangeGet(y5_Data_Address, y5_Data_Address)
        Data_y6 = self.xwRangeGet(y6_Data_Address, y6_Data_Address)
        Data_y7 = self.xwRangeGet(y7_Data_Address, y7_Data_Address)

        Name_y1 = self.xwRangeGet(y1_Name_Address, y1_Name_Address)
        Name_y2 = self.xwRangeGet(y2_Name_Address, y2_Name_Address)
        Name_y3 = self.xwRangeGet(y3_Name_Address, y3_Name_Address)
        Name_y4 = self.xwRangeGet(y4_Name_Address, y4_Name_Address)
        Name_y5 = self.xwRangeGet(y5_Name_Address, y5_Name_Address)
        Name_y6 = self.xwRangeGet(y6_Name_Address, y6_Name_Address)
        Name_y7 = self.xwRangeGet(y7_Name_Address, y7_Name_Address)

        Unit_y1 = self.xwRangeGet(y1_Unit_Address, y1_Unit_Address)
        Unit_y2 = self.xwRangeGet(y2_Unit_Address, y2_Unit_Address)
        Unit_y3 = self.xwRangeGet(y3_Unit_Address, y3_Unit_Address)
        Unit_y4 = self.xwRangeGet(y4_Unit_Address, y4_Unit_Address)
        Unit_y5 = self.xwRangeGet(y5_Unit_Address, y5_Unit_Address)
        Unit_y6 = self.xwRangeGet(y6_Unit_Address, y6_Unit_Address)
        Unit_y7 = self.xwRangeGet(y7_Unit_Address, y7_Unit_Address)

        UP_Limit_x1 = self.xwRangeGet(x1_UP_LIMIT_Address, x1_UP_LIMIT_Address)
        LOW_Limit_x1 = self.xwRangeGet(x1_LOW_LIMIT_Address, x1_LOW_LIMIT_Address)
        UP_Limit_x2 = self.xwRangeGet(x2_UP_LIMIT_Address, x2_UP_LIMIT_Address)
        LOW_Limit_x2 = self.xwRangeGet(x2_LOW_LIMIT_Address, x2_LOW_LIMIT_Address)

        UP_View_x = self.xwRangeGet(x_UP_VIEW_Address, x_UP_VIEW_Address)
        LOW_View_x = self.xwRangeGet(x_LOW_VIEW_Address, x_LOW_VIEW_Address)
        UP_View_y = self.xwRangeGet(y_UP_VIEW_Address, y_UP_VIEW_Address)
        LOW_View_y = self.xwRangeGet(y_LOW_VIEW_Address, y_LOW_VIEW_Address)

        Title_Text = self.xwRangeGet(Title_Text_Address, Title_Text_Address)
        Title_Size = self.xwRangeGet(Title_Size_Address, Title_Size_Address)

        starttime = time.time()

        Graphs = PlotlyGraph(Mode=Mode,
                             x1=Data_x1,x2=Data_x2,x3=Data_x3,x4=Data_x4,x5=Data_x5,x6=Data_x6,x7=Data_x7,
                             y1=Data_y1, y2=Data_y2, y3=Data_y3, y4=Data_y4, y5=Data_y5, y6=Data_y6, y7=Data_y7,
                             x1Name=Name_x1,x2Name=Name_x2,x3Name=Name_x3,x4Name=Name_x4,x5Name=Name_x5,x6Name=Name_x6,x7Name=Name_x7,
                             y1Name=Name_y1,y2Name=Name_y2,y3Name=Name_y3,y4Name=Name_y4,y5Name=Name_y5,y6Name=Name_y6,y7Name=Name_y7,
                             x1Unit=Unit_x1,x2Unit=Unit_x2,x3Unit=Unit_x3,x4Unit=Unit_x4,x5Unit=Unit_x5,x6Unit=Unit_x6,x7Unit=Unit_x7,
                             y1Unit=Unit_y1,y2Unit=Unit_y2,y3Unit=Unit_y3,y4Unit=Unit_y4,y5Unit=Unit_y5,y6Unit=Unit_y6,y7Unit=Unit_y7,
                             y1Colour=y1_Color,y2Colour=y2_Color,y3Colour=y3_Color,y4Colour=y4_Color,y5Colour=y5_Color,y6Colour=y6_Color,y7Colour=y7_Color,
                             x1_UpperLimit=UP_Limit_x1,x2_UpperLimit=UP_Limit_x2,
                             x1_LowerLimit=LOW_Limit_x1,x2_LowerLimit=LOW_Limit_x2,
                             Vertical_Range_Lower=LOW_View_y,Vertical_Range_Upper=UP_View_y,
                             Horizontal_Range_Lower=LOW_View_x, Horizontal_Range_Upper=UP_View_x,
                             Title=Title_Text,
                             Title_Size=Title_Size,
                             Title_Colour=Title_Colour,
                             Scale_X=Scale_X, Scale_Y=Scale_Y,
                             )
        Graphs.Plotly_Result.show()

        elapstedtime = time.time() - starttime
        print("Function: GraphGenerate completed in {:.3}s".format(elapstedtime))
        textwriter("Function: GraphGenerate completed in {:.3}s".format(elapstedtime))

    # def EG_save_file(self,name, content):
    #     """Decode and store a file uploaded with Plotly Dash."""
    #     FileLocation = str(pathlib.Path(__file__).parent)
    #     FileLocation += '\\assets'
    #     data = content.encode("utf8").split(b";base64,")[1]
    #     with open(os.path.join(FileLocation, name), "wb") as fp:
    #         fp.write(base64.decodebytes(data))

def EG_save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    FileLocation = str(pathlib.Path(__file__).parent)
    FileLocation += '\\assets'
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(FileLocation, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

RunningExcelGraph = ""
def RunExcelGraph(Path):
    global RunningExcelGraph
    RunningExcelGraph = ExcelGraph(Path)
    return RunningExcelGraph

global file
@app.callback(
    Output('HT1D_console-out','srcDoc'),
    [Input('interval1','n_intervals')])
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

@app.callback(
    Output('HT2D_console-out','srcDoc'),
    [Input('interval1','n_intervals')])
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

@app.callback(
    Output('SC_console-out','srcDoc'),
    [Input('interval1','n_intervals')])
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

@app.callback(
    Output(component_id="EG_Loading_File_Name", component_property="children"),
    [Input(component_id="ExcelGraph_upload-data", component_property="filename"),
     Input(component_id="ExcelGraph_upload-data", component_property="contents")])
def ExcelFileOpenner(uploaded_filenames, uploaded_file_contents):
    global RunningExcelGraph
    """Save uploaded files and regenerate the file list."""
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        starttime = time.time()

        for name, data in zip(['temp.'+str(uploaded_filenames[0].split('.')[1])], uploaded_file_contents):
            try:
                EG_save_file(name, data)
            except:
                print("Close temp."+str(uploaded_filenames[0].split('.')[1]) + " to proceed process")

        Path = str(pathlib.Path(__file__).parent)
        Path += '\\assets\\'+ name

        RunningExcelGraph = RunExcelGraph(Path)

        elapstedtime = time.time() - starttime
        print("Excel File was loaded in {:.3}s".format(elapstedtime))
        textwriter("Excel File was loaded in {:.3}s".format(elapstedtime))

    if uploaded_filenames != None:
        return ["File = "+uploaded_filenames[0]]
    else:
        return ["File = "]

####################################################################################
BT_GRAPH_GENERATE = 0
@app.callback(
    Output(component_id="HT1D_BT_Graph_Generate_Status",component_property=  "value"),
    [Input(component_id="HT1D_BT_Graph_Generate",component_property=  "n_clicks"),
     State(component_id="HT1D_BT_X1_DATA_INPUT",component_property=  "value"),
     State(component_id="HT1D_BT_X1_NAME_INPUT",component_property=  "value"),
     State(component_id="HT1D_BT_X1_UNIT_INPUT", component_property="value"),
     State(component_id="HT1D_BT_X1_COLOUR", component_property="value"),
     State(component_id="HT1D_BT_X1_UP_LIMIT_INPUT", component_property="value"),
     State(component_id="HT1D_BT_X1_LOW_LIMIT_INPUT", component_property="value"),
     State(component_id="HT1D_BT_TITLE_TEXT_INPUT", component_property="value"),
     State(component_id="HT1D_BT_TITLE_SIZE_INPUT", component_property="value"),
     State(component_id="HT1D_BT_TITLE_COLOUR", component_property="value"),
     ]
)
def EG_Graph_Generate(BT_Graph_Generate_Clicked,
                      HT1D_DATA_X1,
                      HT1D_NAME_X1,
                      HT1D_UNIT_X1,
                      HT1D_COLOR_X1,
                      HT1D_UP_LIMIT_X1,
                      HT1D_LOW_LIMIT_X1,
                      HT1D_TITLE_TEXT,
                      HT1D_TITLE_SIZE,
                      HT1D_TITLE_COLOUR,
                      ):
    global RunningExcelGraph, BT_GRAPH_GENERATE

    if type(RunningExcelGraph) != str and BT_GRAPH_GENERATE != BT_Graph_Generate_Clicked:
        BT_GRAPH_GENERATE = BT_Graph_Generate_Clicked
        print("-- 1D Histogram Mode was called --")
        textwriter("-- 1D Histogram Mode was called --")
        RunningExcelGraph.GraphGenerate(Mode=MODELIST[0],# "Histogram",
                                        x1_Data_Address=HT1D_DATA_X1,
                                        x1_Name_Address=HT1D_NAME_X1,
                                        x1_Unit_Address=HT1D_UNIT_X1,
                                        y1_Color = HT1D_COLOR_X1,
                                        x1_UP_LIMIT_Address=HT1D_UP_LIMIT_X1,
                                        x1_LOW_LIMIT_Address=HT1D_LOW_LIMIT_X1,
                                        Title_Text_Address=HT1D_TITLE_TEXT,
                                        Title_Size_Address=HT1D_TITLE_SIZE,
                                        Title_Colour=HT1D_TITLE_COLOUR,
                                        )

    return ["Making Graph"]

####################################################################################
BT2D_GRAPH_GENERATE = 0
@app.callback(
    Output(component_id="HT2D_BT_Graph_Generate_Status",component_property=  "value"),
    [Input(component_id="HT2D_BT_Graph_Generate",component_property=  "n_clicks"),
     State(component_id="HT2D_BT_X1_DATA_INPUT",component_property=  "value"),
     State(component_id="HT2D_BT_X1_NAME_INPUT",component_property=  "value"),
     State(component_id="HT2D_BT_X1_UNIT_INPUT", component_property="value"),
     State(component_id="HT2D_BT_X1_COLOUR", component_property="value"),
     State(component_id="HT2D_BT_X2_DATA_INPUT", component_property="value"),
     State(component_id="HT2D_BT_X2_NAME_INPUT", component_property="value"),
     State(component_id="HT2D_BT_X2_UNIT_INPUT", component_property="value"),
     State(component_id="HT2D_BT_X2_COLOUR", component_property="value"),
     State(component_id="HT2D_BT_X1_UP_LIMIT_INPUT", component_property="value"),
     State(component_id="HT2D_BT_X1_LOW_LIMIT_INPUT", component_property="value"),
     State(component_id="HT2D_BT_X2_UP_LIMIT_INPUT", component_property="value"),
     State(component_id="HT2D_BT_X2_LOW_LIMIT_INPUT", component_property="value"),
     State(component_id="HT2D_BT_TITLE_TEXT_INPUT", component_property="value"),
     State(component_id="HT2D_BT_TITLE_SIZE_INPUT", component_property="value"),
     State(component_id="HT2D_BT_TITLE_COLOUR", component_property="value"),
     ]
)
def EG_Graph_Generate(BT2D_Graph_Generate_Clicked,
                      HT2D_DATA_X1,
                      HT2D_NAME_X1,
                      HT2D_UNIT_X1,
                      HT2D_COLOR_X1,
                      HT2D_DATA_X2,
                      HT2D_NAME_X2,
                      HT2D_UNIT_X2,
                      HT2D_COLOR_X2,
                      HT2D_UP_LIMIT_X1,
                      HT2D_LOW_LIMIT_X1,
                      HT2D_UP_LIMIT_X2,
                      HT2D_LOW_LIMIT_X2,
                      HT2D_TITLE_TEXT,
                      HT2D_TITLE_SIZE,
                      HT2D_TITLE_COLOUR,
                      ):
    global RunningExcelGraph, BT2D_GRAPH_GENERATE

    if type(RunningExcelGraph) != str and BT2D_GRAPH_GENERATE != BT2D_Graph_Generate_Clicked:
        BT2D_GRAPH_GENERATE = BT2D_Graph_Generate_Clicked
        print("-- 2D Histogram Mode was called --")
        textwriter("-- 2D Histogram Mode was called --")
        RunningExcelGraph.GraphGenerate(Mode=MODELIST[1], #"Histogram_2D",
                                        x1_Data_Address=HT2D_DATA_X1,
                                        x1_Name_Address=HT2D_NAME_X1,
                                        x1_Unit_Address=HT2D_UNIT_X1,
                                        y1_Color=HT2D_COLOR_X1,
                                        x2_Data_Address=HT2D_DATA_X2,
                                        x2_Name_Address=HT2D_NAME_X2,
                                        x2_Unit_Address=HT2D_UNIT_X2,
                                        y2_Color=HT2D_COLOR_X2,
                                        x1_UP_LIMIT_Address=HT2D_UP_LIMIT_X1,
                                        x1_LOW_LIMIT_Address=HT2D_LOW_LIMIT_X1,
                                        x2_UP_LIMIT_Address=HT2D_UP_LIMIT_X2,
                                        x2_LOW_LIMIT_Address=HT2D_LOW_LIMIT_X2,
                                        Title_Text_Address=HT2D_TITLE_TEXT,
                                        Title_Size_Address=HT2D_TITLE_SIZE,
                                        Title_Colour=HT2D_TITLE_COLOUR,
                                        )

    return ["Making Graph"]

####################################################################################
SC_GRAPH_GENERATE = 0
@app.callback(
    Output(component_id="SC_BT_Graph_Generate_Status",component_property=  "value"),
    [Input(component_id="SC_BT_Graph_Generate",component_property=  "n_clicks"),

     State(component_id="SC_BT_X1_DATA_INPUT", component_property="value"),
     State(component_id="SC_BT_X2_DATA_INPUT", component_property="value"),
     State(component_id="SC_BT_X3_DATA_INPUT", component_property="value"),
     State(component_id="SC_BT_X4_DATA_INPUT", component_property="value"),
     State(component_id="SC_BT_X5_DATA_INPUT", component_property="value"),
     State(component_id="SC_BT_X6_DATA_INPUT", component_property="value"),
     State(component_id="SC_BT_X7_DATA_INPUT", component_property="value"),

     State(component_id="SC_BT_X1_NAME_INPUT", component_property="value"),
     State(component_id="SC_BT_X2_NAME_INPUT", component_property="value"),
     State(component_id="SC_BT_X3_NAME_INPUT", component_property="value"),
     State(component_id="SC_BT_X4_NAME_INPUT", component_property="value"),
     State(component_id="SC_BT_X5_NAME_INPUT", component_property="value"),
     State(component_id="SC_BT_X6_NAME_INPUT", component_property="value"),
     State(component_id="SC_BT_X7_NAME_INPUT", component_property="value"),

     State(component_id="SC_BT_X1_UNIT_INPUT", component_property="value"),
     State(component_id="SC_BT_X2_UNIT_INPUT", component_property="value"),
     State(component_id="SC_BT_X3_UNIT_INPUT", component_property="value"),
     State(component_id="SC_BT_X4_UNIT_INPUT", component_property="value"),
     State(component_id="SC_BT_X5_UNIT_INPUT", component_property="value"),
     State(component_id="SC_BT_X6_UNIT_INPUT", component_property="value"),
     State(component_id="SC_BT_X7_UNIT_INPUT", component_property="value"),

     State(component_id="SC_BT_Y1_DATA_INPUT", component_property="value"),
     State(component_id="SC_BT_Y2_DATA_INPUT", component_property="value"),
     State(component_id="SC_BT_Y3_DATA_INPUT", component_property="value"),
     State(component_id="SC_BT_Y4_DATA_INPUT", component_property="value"),
     State(component_id="SC_BT_Y5_DATA_INPUT", component_property="value"),
     State(component_id="SC_BT_Y6_DATA_INPUT", component_property="value"),
     State(component_id="SC_BT_Y7_DATA_INPUT", component_property="value"),

     State(component_id="SC_BT_Y1_NAME_INPUT", component_property="value"),
     State(component_id="SC_BT_Y2_NAME_INPUT", component_property="value"),
     State(component_id="SC_BT_Y3_NAME_INPUT", component_property="value"),
     State(component_id="SC_BT_Y4_NAME_INPUT", component_property="value"),
     State(component_id="SC_BT_Y5_NAME_INPUT", component_property="value"),
     State(component_id="SC_BT_Y6_NAME_INPUT", component_property="value"),
     State(component_id="SC_BT_Y7_NAME_INPUT", component_property="value"),

     State(component_id="SC_BT_Y1_UNIT_INPUT", component_property="value"),
     State(component_id="SC_BT_Y2_UNIT_INPUT", component_property="value"),
     State(component_id="SC_BT_Y3_UNIT_INPUT", component_property="value"),
     State(component_id="SC_BT_Y4_UNIT_INPUT", component_property="value"),
     State(component_id="SC_BT_Y5_UNIT_INPUT", component_property="value"),
     State(component_id="SC_BT_Y6_UNIT_INPUT", component_property="value"),
     State(component_id="SC_BT_Y7_UNIT_INPUT", component_property="value"),

     State(component_id="SC_Y1_COLOUR", component_property="value"),
     State(component_id="SC_Y2_COLOUR", component_property="value"),
     State(component_id="SC_Y3_COLOUR", component_property="value"),
     State(component_id="SC_Y4_COLOUR", component_property="value"),
     State(component_id="SC_Y5_COLOUR", component_property="value"),
     State(component_id="SC_Y6_COLOUR", component_property="value"),
     State(component_id="SC_Y7_COLOUR", component_property="value"),

     State(component_id="SC_BT_X1_UP_VIEW_INPUT", component_property="value"),
     State(component_id="SC_BT_X1_LOW_VIEW_INPUT", component_property="value"),
     State(component_id="SC_BT_Y_UP_VIEW_INPUT", component_property="value"),
     State(component_id="SC_BT_Y_LOW_VIEW_INPUT", component_property="value"),

     State(component_id="SC_BT_TITLE_TEXT_INPUT", component_property="value"),
     State(component_id="SC_BT_TITLE_SIZE_INPUT", component_property="value"),
     State(component_id="SC_BT_TITLE_COLOUR", component_property="value"),

     State(component_id="SC_BT_Graph_Scale_Horizontal", component_property="value"),
     State(component_id="SC_BT_Graph_Scale_Vertical", component_property="value"),

     ]
)
def EG_Graph_Generate(SC_Graph_Generate_Clicked,
                      SC_DATA_X1, SC_DATA_X2, SC_DATA_X3, SC_DATA_X4, SC_DATA_X5, SC_DATA_X6, SC_DATA_X7,
                      SC_NAME_X1, SC_NAME_X2, SC_NAME_X3, SC_NAME_X4, SC_NAME_X5, SC_NAME_X6, SC_NAME_X7,
                      SC_UNIT_X1, SC_UNIT_X2, SC_UNIT_X3, SC_UNIT_X4, SC_UNIT_X5, SC_UNIT_X6, SC_UNIT_X7,
                      SC_DATA_Y1, SC_DATA_Y2, SC_DATA_Y3, SC_DATA_Y4, SC_DATA_Y5, SC_DATA_Y6, SC_DATA_Y7,
                      SC_NAME_Y1, SC_NAME_Y2, SC_NAME_Y3, SC_NAME_Y4, SC_NAME_Y5, SC_NAME_Y6, SC_NAME_Y7,
                      SC_UNIT_Y1, SC_UNIT_Y2, SC_UNIT_Y3, SC_UNIT_Y4, SC_UNIT_Y5, SC_UNIT_Y6, SC_UNIT_Y7,
                      SC_COLOUR_Y1, SC_COLOUR_Y2, SC_COLOUR_Y3, SC_COLOUR_Y4, SC_COLOUR_Y5, SC_COLOUR_Y6, SC_COLOUR_Y7,
                      SC_X_UP_VIEW, SC_X_LOW_VIEW, SC_Y_UP_VIEW, SC_Y_LOW_VIEW,
                      SC_TITLE_TEXT, SC_TITLE_SIZE, SC_TITLE_COLOUR,
                      SC_SCALE_X, SC_SCALE_Y,
                      ):
    global RunningExcelGraph, SC_GRAPH_GENERATE

    if type(RunningExcelGraph) != str and SC_GRAPH_GENERATE != SC_Graph_Generate_Clicked:
        SC_GRAPH_GENERATE = SC_Graph_Generate_Clicked
        print("-- Scatter Graph Mode was called --")
        textwriter("-- Scatter Graph Mode was called --")
        RunningExcelGraph.GraphGenerate(Mode=MODELIST[2], #"Scatter Graph",
            x1_Data_Address=SC_DATA_X1, x2_Data_Address=SC_DATA_X2, x3_Data_Address=SC_DATA_X3, x4_Data_Address=SC_DATA_X4,
                                        x5_Data_Address=SC_DATA_X5, x6_Data_Address=SC_DATA_X6, x7_Data_Address=SC_DATA_X7,
            x1_Name_Address=SC_NAME_X1, x2_Name_Address=SC_NAME_X2, x3_Name_Address=SC_NAME_X3, x4_Name_Address=SC_NAME_X4,
                                        x5_Name_Address=SC_NAME_X5, x6_Name_Address=SC_NAME_X6, x7_Name_Address=SC_NAME_X7,
            x1_Unit_Address=SC_UNIT_X1, x2_Unit_Address=SC_UNIT_X2, x3_Unit_Address=SC_UNIT_X3, x4_Unit_Address=SC_UNIT_X4,
                                        x5_Unit_Address=SC_UNIT_X5, x6_Unit_Address=SC_UNIT_X6, x7_Unit_Address=SC_UNIT_X7,

            y1_Data_Address=SC_DATA_Y1, y2_Data_Address=SC_DATA_Y2, y3_Data_Address=SC_DATA_Y3, y4_Data_Address=SC_DATA_Y4,
                                        y5_Data_Address=SC_DATA_Y5, y6_Data_Address=SC_DATA_Y6, y7_Data_Address=SC_DATA_Y7,
            y1_Name_Address=SC_NAME_Y1, y2_Name_Address=SC_NAME_Y2, y3_Name_Address=SC_NAME_Y3, y4_Name_Address=SC_NAME_Y4,
                                        y5_Name_Address=SC_NAME_Y5, y6_Name_Address=SC_NAME_Y6, y7_Name_Address=SC_NAME_Y7,
            y1_Unit_Address=SC_UNIT_Y1, y2_Unit_Address=SC_UNIT_Y2, y3_Unit_Address=SC_UNIT_Y3, y4_Unit_Address=SC_UNIT_Y4,
                                        y5_Unit_Address=SC_UNIT_Y5, y6_Unit_Address=SC_UNIT_Y6, y7_Unit_Address=SC_UNIT_Y7,
            y1_Color = SC_COLOUR_Y1, y2_Color = SC_COLOUR_Y2, y3_Color = SC_COLOUR_Y3, y4_Color = SC_COLOUR_Y4, y5_Color = SC_COLOUR_Y5,
                                        y6_Color=SC_COLOUR_Y6, y7_Color = SC_COLOUR_Y7,
            x_UP_VIEW_Address = SC_X_UP_VIEW, x_LOW_VIEW_Address = SC_X_LOW_VIEW,
            y_UP_VIEW_Address = SC_Y_UP_VIEW, y_LOW_VIEW_Address = SC_Y_LOW_VIEW,
            Title_Text_Address=SC_TITLE_TEXT, Title_Size_Address=SC_TITLE_SIZE, Title_Colour=SC_TITLE_COLOUR,
            Scale_X = SC_SCALE_X, Scale_Y = SC_SCALE_Y,
            )

    return ["Making Graph"]


####################################################################################
BT_X1_DATA_SET = 0
BT_X1_DATA_CLEAR = 0
@app.callback(
    Output(component_id="HT1D_BT_X1_DATA_INPUT",component_property=  "value"),
    [Input(component_id="HT1D_BT_X1_DATA_SET",component_property=  "n_clicks"),
     Input(component_id="HT1D_BT_X1_DATA_CLEAR",component_property=  "n_clicks")])
def update_output(BT_X1_SET_Clicked, BT_X1_CLEAR_Clicked):
    global RunningExcelGraph, BT_X1_DATA_SET, BT_X1_DATA_CLEAR

    if type(RunningExcelGraph) != str and BT_X1_DATA_SET != BT_X1_SET_Clicked:
        BT_X1_DATA_SET = BT_X1_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and BT_X1_DATA_CLEAR != BT_X1_CLEAR_Clicked:
        BT_X1_DATA_CLEAR = BT_X1_CLEAR_Clicked
        return [""]
####################################################################################

####################################################################################
BT_X1_NAME_SET = 0
BT_X1_NAME_CLEAR = 0
@app.callback(
    Output(component_id="HT1D_BT_X1_NAME_INPUT",component_property=  "value"),
    [Input(component_id="HT1D_BT_X1_NAME_SET",component_property=  "n_clicks"),
     Input(component_id="HT1D_BT_X1_NAME_CLEAR",component_property=  "n_clicks")])
def update_output(BT_X1_SET_Clicked, BT_X1_CLEAR_Clicked):
    global RunningExcelGraph, BT_X1_NAME_SET, BT_X1_NAME_CLEAR

    if type(RunningExcelGraph) != str and BT_X1_NAME_SET != BT_X1_SET_Clicked:
        BT_X1_NAME_SET = BT_X1_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and BT_X1_NAME_CLEAR != BT_X1_CLEAR_Clicked:
        BT_X1_NAME_CLEAR = BT_X1_CLEAR_Clicked
        return [""]
####################################################################################

####################################################################################
BT_X1_UNIT_SET = 0
BT_X1_UNIT_CLEAR = 0
@app.callback(
    Output(component_id="HT1D_BT_X1_UNIT_INPUT",component_property=  "value"),
    [Input(component_id="HT1D_BT_X1_UNIT_SET",component_property=  "n_clicks"),
     Input(component_id="HT1D_BT_X1_UNIT_CLEAR",component_property=  "n_clicks")])
def update_output(BT_X1_SET_Clicked, BT_X1_CLEAR_Clicked):
    global RunningExcelGraph, BT_X1_UNIT_SET, BT_X1_UNIT_CLEAR

    if type(RunningExcelGraph) != str and BT_X1_UNIT_SET != BT_X1_SET_Clicked:
        BT_X1_UNIT_SET = BT_X1_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and BT_X1_UNIT_CLEAR != BT_X1_CLEAR_Clicked:
        BT_X1_UNIT_CLEAR = BT_X1_CLEAR_Clicked
        return [""]
####################################################################################
####################################################################################
BT_X1_UP_LIMIT_SET = 0
BT_X1_UP_LIMIT_CLEAR = 0
@app.callback(
    Output(component_id="HT1D_BT_X1_UP_LIMIT_INPUT",component_property=  "value"),
    [Input(component_id="HT1D_BT_X1_UP_LIMIT_SET",component_property=  "n_clicks"),
     Input(component_id="HT1D_BT_X1_UP_LIMIT_CLEAR",component_property=  "n_clicks")])
def update_output(BT_X1_SET_Clicked, BT_X1_CLEAR_Clicked):
    global RunningExcelGraph, BT_X1_UP_LIMIT_SET, BT_X1_UP_LIMIT_CLEAR

    if type(RunningExcelGraph) != str and BT_X1_UP_LIMIT_SET != BT_X1_SET_Clicked:
        BT_X1_UP_LIMIT_SET = BT_X1_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and BT_X1_UP_LIMIT_CLEAR != BT_X1_CLEAR_Clicked:
        BT_X1_UP_LIMIT_CLEAR = BT_X1_CLEAR_Clicked
        return [""]
####################################################################################
####################################################################################
BT_X1_LOW_LIMIT_SET = 0
BT_X1_LOW_LIMIT_CLEAR = 0
@app.callback(
    Output(component_id="HT1D_BT_X1_LOW_LIMIT_INPUT",component_property=  "value"),
    [Input(component_id="HT1D_BT_X1_LOW_LIMIT_SET",component_property=  "n_clicks"),
     Input(component_id="HT1D_BT_X1_LOW_LIMIT_CLEAR",component_property=  "n_clicks")])
def update_output(BT_X1_SET_Clicked, BT_X1_CLEAR_Clicked):
    global RunningExcelGraph, BT_X1_LOW_LIMIT_SET, BT_X1_LOW_LIMIT_CLEAR

    if type(RunningExcelGraph) != str and BT_X1_LOW_LIMIT_SET != BT_X1_SET_Clicked:
        BT_X1_LOW_LIMIT_SET = BT_X1_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and BT_X1_LOW_LIMIT_CLEAR != BT_X1_CLEAR_Clicked:
        BT_X1_LOW_LIMIT_CLEAR = BT_X1_CLEAR_Clicked
        return [""]
####################################################################################

####################################################################################
BT_TITLE_TEXT_SET = 0
BT_TITLE_TEXT_CLEAR = 0
@app.callback(
    Output(component_id="HT1D_BT_TITLE_TEXT_INPUT",component_property=  "value"),
    [Input(component_id="HT1D_BT_TITLE_TEXT_SET",component_property=  "n_clicks"),
     Input(component_id="HT1D_BT_TITLE_TEXT_CLEAR",component_property=  "n_clicks")])
def update_output(BT_X1_SET_Clicked, BT_X1_CLEAR_Clicked):
    global RunningExcelGraph, BT_TITLE_TEXT_SET, BT_TITLE_TEXT_CLEAR

    if type(RunningExcelGraph) != str and BT_TITLE_TEXT_SET != BT_X1_SET_Clicked:
        BT_TITLE_TEXT_SET = BT_X1_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and BT_TITLE_TEXT_CLEAR != BT_X1_CLEAR_Clicked:
        BT_TITLE_TEXT_CLEAR = BT_X1_CLEAR_Clicked
        return [""]
####################################################################################

####################################################################################
BT_TITLE_SIZE_SET = 0
BT_TITLE_SIZE_CLEAR = 0
@app.callback(
    Output(component_id="HT1D_BT_TITLE_SIZE_INPUT",component_property=  "value"),
    [Input(component_id="HT1D_BT_TITLE_SIZE_SET",component_property=  "n_clicks"),
     Input(component_id="HT1D_BT_TITLE_SIZE_CLEAR",component_property=  "n_clicks")])
def update_output(BT_TITLE_SIZE_SET_Clicked, BT_TITLE_SIZE_CLEAR_Clicked):
    global RunningExcelGraph, BT_TITLE_SIZE_SET, BT_TITLE_SIZE_CLEAR

    if type(RunningExcelGraph) != str and BT_TITLE_SIZE_SET != BT_TITLE_SIZE_SET_Clicked:
        BT_TITLE_SIZE_SET = BT_TITLE_SIZE_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and BT_TITLE_SIZE_CLEAR != BT_TITLE_SIZE_CLEAR_Clicked:
        BT_TITLE_SIZE_CLEAR = BT_TITLE_SIZE_CLEAR_Clicked
        return 10
####################################################################################

##********************************************
## Call backs for 2D Histogram
##********************************************

## X1 Data
####################################################################################
BT2D_X1_DATA_SET = 0
BT2D_X1_DATA_CLEAR = 0
@app.callback(
    Output(component_id="HT2D_BT_X1_DATA_INPUT",component_property=  "value"),
    [Input(component_id="HT2D_BT_X1_DATA_SET",component_property=  "n_clicks"),
     Input(component_id="HT2D_BT_X1_DATA_CLEAR",component_property=  "n_clicks")])
def update_output(BT2D_X1_SET_Clicked, BT2D_X1_CLEAR_Clicked):
    global RunningExcelGraph, BT2D_X1_DATA_SET, BT2D_X1_DATA_CLEAR

    if type(RunningExcelGraph) != str and BT2D_X1_DATA_SET != BT2D_X1_SET_Clicked:
        BT2D_X1_DATA_SET = BT2D_X1_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and BT2D_X1_DATA_CLEAR != BT2D_X1_CLEAR_Clicked:
        BT2D_X1_DATA_CLEAR = BT2D_X1_CLEAR_Clicked
        return [""]
####################################################################################
####################################################################################
BT2D_X1_NAME_SET = 0
BT2D_X1_NAME_CLEAR = 0
@app.callback(
    Output(component_id="HT2D_BT_X1_NAME_INPUT",component_property=  "value"),
    [Input(component_id="HT2D_BT_X1_NAME_SET",component_property=  "n_clicks"),
     Input(component_id="HT2D_BT_X1_NAME_CLEAR",component_property=  "n_clicks")])
def update_output(BT2D_X1_NAME_SET_Clicked, BT2D_X1_NAME_CLEAR_Clicked):
    global RunningExcelGraph, BT2D_X1_NAME_SET, BT2D_X1_NAME_CLEAR

    if type(RunningExcelGraph) != str and BT2D_X1_NAME_SET != BT2D_X1_NAME_SET_Clicked:
        BT2D_X1_NAME_SET = BT2D_X1_NAME_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and BT2D_X1_NAME_CLEAR != BT2D_X1_NAME_CLEAR_Clicked:
        BT2D_X1_NAME_CLEAR = BT2D_X1_NAME_CLEAR_Clicked
        return [""]
####################################################################################
####################################################################################
BT2D_X1_UNIT_SET = 0
BT2D_X1_UNIT_CLEAR = 0
@app.callback(
    Output(component_id="HT2D_BT_X1_UNIT_INPUT",component_property=  "value"),
    [Input(component_id="HT2D_BT_X1_UNIT_SET",component_property=  "n_clicks"),
     Input(component_id="HT2D_BT_X1_UNIT_CLEAR",component_property=  "n_clicks")])
def update_output(BT2D_X1_UNIT_SET_Clicked, BT2D_X1_UNIT_CLEAR_Clicked):
    global RunningExcelGraph, BT2D_X1_UNIT_SET, BT2D_X1_UNIT_CLEAR

    if type(RunningExcelGraph) != str and BT2D_X1_UNIT_SET != BT2D_X1_UNIT_SET_Clicked:
        BT2D_X1_UNIT_SET = BT2D_X1_UNIT_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and BT2D_X1_UNIT_CLEAR != BT2D_X1_UNIT_CLEAR_Clicked:
        BT2D_X1_UNIT_CLEAR = BT2D_X1_UNIT_CLEAR_Clicked
        return [""]
####################################################################################

## X2 Data
####################################################################################
BT2D_X2_DATA_SET = 0
BT2D_X2_DATA_CLEAR = 0
@app.callback(
    Output(component_id="HT2D_BT_X2_DATA_INPUT",component_property=  "value"),
    [Input(component_id="HT2D_BT_X2_DATA_SET",component_property=  "n_clicks"),
     Input(component_id="HT2D_BT_X2_DATA_CLEAR",component_property=  "n_clicks")])
def update_output(BT2D_X2_SET_Clicked, BT2D_X2_CLEAR_Clicked):
    global RunningExcelGraph, BT2D_X2_DATA_SET, BT2D_X2_DATA_CLEAR

    if type(RunningExcelGraph) != str and BT2D_X2_DATA_SET != BT2D_X2_SET_Clicked:
        BT2D_X2_DATA_SET = BT2D_X2_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and BT2D_X2_DATA_CLEAR != BT2D_X2_CLEAR_Clicked:
        BT2D_X2_DATA_CLEAR = BT2D_X2_CLEAR_Clicked
        return [""]
####################################################################################
####################################################################################
BT2D_X2_NAME_SET = 0
BT2D_X2_NAME_CLEAR = 0
@app.callback(
    Output(component_id="HT2D_BT_X2_NAME_INPUT",component_property=  "value"),
    [Input(component_id="HT2D_BT_X2_NAME_SET",component_property=  "n_clicks"),
     Input(component_id="HT2D_BT_X2_NAME_CLEAR",component_property=  "n_clicks")])
def update_output(BT2D_X2_NAME_SET_Clicked, BT2D_X2_NAME_CLEAR_Clicked):
    global RunningExcelGraph, BT2D_X2_NAME_SET, BT2D_X2_NAME_CLEAR

    if type(RunningExcelGraph) != str and BT2D_X2_NAME_SET != BT2D_X2_NAME_SET_Clicked:
        BT2D_X2_NAME_SET = BT2D_X2_NAME_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and BT2D_X2_NAME_CLEAR != BT2D_X2_NAME_CLEAR_Clicked:
        BT2D_X2_NAME_CLEAR = BT2D_X2_NAME_CLEAR_Clicked
        return [""]
####################################################################################
####################################################################################
BT2D_X2_UNIT_SET = 0
BT2D_X2_UNIT_CLEAR = 0
@app.callback(
    Output(component_id="HT2D_BT_X2_UNIT_INPUT",component_property=  "value"),
    [Input(component_id="HT2D_BT_X2_UNIT_SET",component_property=  "n_clicks"),
     Input(component_id="HT2D_BT_X2_UNIT_CLEAR",component_property=  "n_clicks")])
def update_output(BT2D_X2_UNIT_SET_Clicked, BT2D_X2_UNIT_CLEAR_Clicked):
    global RunningExcelGraph, BT2D_X2_UNIT_SET, BT2D_X2_UNIT_CLEAR

    if type(RunningExcelGraph) != str and BT2D_X2_UNIT_SET != BT2D_X2_UNIT_SET_Clicked:
        BT2D_X2_UNIT_SET = BT2D_X2_UNIT_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and BT2D_X2_UNIT_CLEAR != BT2D_X2_UNIT_CLEAR_Clicked:
        BT2D_X2_UNIT_CLEAR = BT2D_X2_UNIT_CLEAR_Clicked
        return [""]
####################################################################################

####################################################################################
BT2D_X1_UP_LIMIT_SET = 0
BT2D_X1_UP_LIMIT_CLEAR = 0
@app.callback(
    Output(component_id="HT2D_BT_X1_UP_LIMIT_INPUT",component_property=  "value"),
    [Input(component_id="HT2D_BT_X1_UP_LIMIT_SET",component_property=  "n_clicks"),
     Input(component_id="HT2D_BT_X1_UP_LIMIT_CLEAR",component_property=  "n_clicks")])
def update_output(BT2D_X1_SET_Clicked, BT2D_X1_CLEAR_Clicked):
    global RunningExcelGraph, BT2D_X1_UP_LIMIT_SET, BT2D_X1_UP_LIMIT_CLEAR

    if type(RunningExcelGraph) != str and BT2D_X1_UP_LIMIT_SET != BT2D_X1_SET_Clicked:
        BT2D_X1_UP_LIMIT_SET = BT2D_X1_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and BT2D_X1_UP_LIMIT_CLEAR != BT2D_X1_CLEAR_Clicked:
        BT2D_X1_UP_LIMIT_CLEAR = BT2D_X1_CLEAR_Clicked
        return [""]
####################################################################################
####################################################################################
BT2D_X1_LOW_LIMIT_SET = 0
BT2D_X1_LOW_LIMIT_CLEAR = 0
@app.callback(
    Output(component_id="HT2D_BT_X1_LOW_LIMIT_INPUT",component_property=  "value"),
    [Input(component_id="HT2D_BT_X1_LOW_LIMIT_SET",component_property=  "n_clicks"),
     Input(component_id="HT2D_BT_X1_LOW_LIMIT_CLEAR",component_property=  "n_clicks")])
def update_output(BT2D_X1_SET_Clicked, BT2D_X1_CLEAR_Clicked):
    global RunningExcelGraph, BT2D_X1_LOW_LIMIT_SET, BT2D_X1_LOW_LIMIT_CLEAR

    if type(RunningExcelGraph) != str and BT2D_X1_LOW_LIMIT_SET != BT2D_X1_SET_Clicked:
        BT2D_X1_LOW_LIMIT_SET = BT2D_X1_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and BT2D_X1_LOW_LIMIT_CLEAR != BT2D_X1_CLEAR_Clicked:
        BT2D_X1_LOW_LIMIT_CLEAR = BT2D_X1_CLEAR_Clicked
        return [""]
####################################################################################
####################################################################################
BT2D_X2_UP_LIMIT_SET = 0
BT2D_X2_UP_LIMIT_CLEAR = 0
@app.callback(
    Output(component_id="HT2D_BT_X2_UP_LIMIT_INPUT",component_property=  "value"),
    [Input(component_id="HT2D_BT_X2_UP_LIMIT_SET",component_property=  "n_clicks"),
     Input(component_id="HT2D_BT_X2_UP_LIMIT_CLEAR",component_property=  "n_clicks")])
def update_output(BT2D_X2_SET_Clicked, BT2D_X2_CLEAR_Clicked):
    global RunningExcelGraph, BT2D_X2_UP_LIMIT_SET, BT2D_X2_UP_LIMIT_CLEAR

    if type(RunningExcelGraph) != str and BT2D_X2_UP_LIMIT_SET != BT2D_X2_SET_Clicked:
        BT2D_X2_UP_LIMIT_SET = BT2D_X2_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and BT2D_X2_UP_LIMIT_CLEAR != BT2D_X2_CLEAR_Clicked:
        BT2D_X2_UP_LIMIT_CLEAR = BT2D_X2_CLEAR_Clicked
        return [""]
####################################################################################
####################################################################################
BT2D_X2_LOW_LIMIT_SET = 0
BT2D_X2_LOW_LIMIT_CLEAR = 0
@app.callback(
    Output(component_id="HT2D_BT_X2_LOW_LIMIT_INPUT",component_property=  "value"),
    [Input(component_id="HT2D_BT_X2_LOW_LIMIT_SET",component_property=  "n_clicks"),
     Input(component_id="HT2D_BT_X2_LOW_LIMIT_CLEAR",component_property=  "n_clicks")])
def update_output(BT2D_X2_SET_Clicked, BT2D_X2_CLEAR_Clicked):
    global RunningExcelGraph, BT2D_X2_LOW_LIMIT_SET, BT2D_X2_LOW_LIMIT_CLEAR

    if type(RunningExcelGraph) != str and BT2D_X2_LOW_LIMIT_SET != BT2D_X2_SET_Clicked:
        BT2D_X2_LOW_LIMIT_SET = BT2D_X2_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and BT2D_X2_LOW_LIMIT_CLEAR != BT2D_X2_CLEAR_Clicked:
        BT2D_X2_LOW_LIMIT_CLEAR = BT2D_X2_CLEAR_Clicked
        return [""]
####################################################################################


####################################################################################
BT2D_TITLE_TEXT_SET = 0
BT2D_TITLE_TEXT_CLEAR = 0
@app.callback(
    Output(component_id="HT2D_BT_TITLE_TEXT_INPUT",component_property=  "value"),
    [Input(component_id="HT2D_BT_TITLE_TEXT_SET",component_property=  "n_clicks"),
     Input(component_id="HT2D_BT_TITLE_TEXT_CLEAR",component_property=  "n_clicks")])
def update_output(BT2D_X1_SET_Clicked, BT2D_X1_CLEAR_Clicked):
    global RunningExcelGraph, BT2D_TITLE_TEXT_SET, BT2D_TITLE_TEXT_CLEAR

    if type(RunningExcelGraph) != str and BT2D_TITLE_TEXT_SET != BT2D_X1_SET_Clicked:
        BT2D_TITLE_TEXT_SET = BT2D_X1_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and BT2D_TITLE_TEXT_CLEAR != BT2D_X1_CLEAR_Clicked:
        BT2D_TITLE_TEXT_CLEAR = BT2D_X1_CLEAR_Clicked
        return [""]
####################################################################################

####################################################################################
BT2D_TITLE_SIZE_SET = 0
BT2D_TITLE_SIZE_CLEAR = 0
@app.callback(
    Output(component_id="HT2D_BT_TITLE_SIZE_INPUT",component_property=  "value"),
    [Input(component_id="HT2D_BT_TITLE_SIZE_SET",component_property=  "n_clicks"),
     Input(component_id="HT2D_BT_TITLE_SIZE_CLEAR",component_property=  "n_clicks")])
def update_output(BT2D_TITLE_SIZE_SET_Clicked, BT2D_TITLE_SIZE_CLEAR_Clicked):
    global RunningExcelGraph, BT2D_TITLE_SIZE_SET, BT2D_TITLE_SIZE_CLEAR

    if type(RunningExcelGraph) != str and BT2D_TITLE_SIZE_SET != BT2D_TITLE_SIZE_SET_Clicked:
        BT2D_TITLE_SIZE_SET = BT2D_TITLE_SIZE_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and BT2D_TITLE_SIZE_CLEAR != BT2D_TITLE_SIZE_CLEAR_Clicked:
        BT2D_TITLE_SIZE_CLEAR = BT2D_TITLE_SIZE_CLEAR_Clicked
        return 10
####################################################################################

##********************************************
## Call backs for 2D Scatter Graph
##********************************************
## X1 Data
####################################################################################
SC_X1_DATA_SET = 0
SC_X1_DATA_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X1_DATA_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X1_DATA_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X1_DATA_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X1_SET_Clicked, SC_X1_CLEAR_Clicked):
    global RunningExcelGraph, SC_X1_DATA_SET, SC_X1_DATA_CLEAR

    if type(RunningExcelGraph) != str and SC_X1_DATA_SET != SC_X1_SET_Clicked:
        SC_X1_DATA_SET = SC_X1_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X1_DATA_CLEAR != SC_X1_CLEAR_Clicked:
        SC_X1_DATA_CLEAR = SC_X1_CLEAR_Clicked
        return [""]
####################################################################################
## X2 Data
####################################################################################
SC_X2_DATA_SET = 0
SC_X2_DATA_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X2_DATA_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X2_DATA_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X2_DATA_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X2_SET_Clicked, SC_X2_CLEAR_Clicked):
    global RunningExcelGraph, SC_X2_DATA_SET, SC_X2_DATA_CLEAR

    if type(RunningExcelGraph) != str and SC_X2_DATA_SET != SC_X2_SET_Clicked:
        SC_X2_DATA_SET = SC_X2_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X2_DATA_CLEAR != SC_X2_CLEAR_Clicked:
        SC_X2_DATA_CLEAR = SC_X2_CLEAR_Clicked
        return [""]
####################################################################################
## X3 Data
####################################################################################
SC_X3_DATA_SET = 0
SC_X3_DATA_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X3_DATA_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X3_DATA_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X3_DATA_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X3_SET_Clicked, SC_X3_CLEAR_Clicked):
    global RunningExcelGraph, SC_X3_DATA_SET, SC_X3_DATA_CLEAR

    if type(RunningExcelGraph) != str and SC_X3_DATA_SET != SC_X3_SET_Clicked:
        SC_X3_DATA_SET = SC_X3_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X3_DATA_CLEAR != SC_X3_CLEAR_Clicked:
        SC_X3_DATA_CLEAR = SC_X3_CLEAR_Clicked
        return [""]
####################################################################################
## X4 Data
####################################################################################
SC_X4_DATA_SET = 0
SC_X4_DATA_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X4_DATA_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X4_DATA_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X4_DATA_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X4_SET_Clicked, SC_X4_CLEAR_Clicked):
    global RunningExcelGraph, SC_X4_DATA_SET, SC_X4_DATA_CLEAR

    if type(RunningExcelGraph) != str and SC_X4_DATA_SET != SC_X4_SET_Clicked:
        SC_X4_DATA_SET = SC_X4_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X4_DATA_CLEAR != SC_X4_CLEAR_Clicked:
        SC_X4_DATA_CLEAR = SC_X4_CLEAR_Clicked
        return [""]
####################################################################################
## X5 Data
####################################################################################
SC_X5_DATA_SET = 0
SC_X5_DATA_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X5_DATA_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X5_DATA_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X5_DATA_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X5_SET_Clicked, SC_X5_CLEAR_Clicked):
    global RunningExcelGraph, SC_X5_DATA_SET, SC_X5_DATA_CLEAR

    if type(RunningExcelGraph) != str and SC_X5_DATA_SET != SC_X5_SET_Clicked:
        SC_X5_DATA_SET = SC_X5_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X5_DATA_CLEAR != SC_X5_CLEAR_Clicked:
        SC_X5_DATA_CLEAR = SC_X5_CLEAR_Clicked
        return [""]
####################################################################################
## X6 Data
####################################################################################
SC_X6_DATA_SET = 0
SC_X6_DATA_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X6_DATA_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X6_DATA_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X6_DATA_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X6_SET_Clicked, SC_X6_CLEAR_Clicked):
    global RunningExcelGraph, SC_X6_DATA_SET, SC_X6_DATA_CLEAR

    if type(RunningExcelGraph) != str and SC_X6_DATA_SET != SC_X6_SET_Clicked:
        SC_X6_DATA_SET = SC_X6_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X6_DATA_CLEAR != SC_X6_CLEAR_Clicked:
        SC_X6_DATA_CLEAR = SC_X6_CLEAR_Clicked
        return [""]
####################################################################################
## X7 Data
####################################################################################
SC_X7_DATA_SET = 0
SC_X7_DATA_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X7_DATA_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X7_DATA_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X7_DATA_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X7_SET_Clicked, SC_X7_CLEAR_Clicked):
    global RunningExcelGraph, SC_X7_DATA_SET, SC_X7_DATA_CLEAR

    if type(RunningExcelGraph) != str and SC_X7_DATA_SET != SC_X7_SET_Clicked:
        SC_X7_DATA_SET = SC_X7_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X7_DATA_CLEAR != SC_X7_CLEAR_Clicked:
        SC_X7_DATA_CLEAR = SC_X7_CLEAR_Clicked
        return [""]
####################################################################################

## Y1 Data
####################################################################################
SC_Y1_DATA_SET = 0
SC_Y1_DATA_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y1_DATA_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y1_DATA_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y1_DATA_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y1_SET_Clicked, SC_Y1_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y1_DATA_SET, SC_Y1_DATA_CLEAR

    if type(RunningExcelGraph) != str and SC_Y1_DATA_SET != SC_Y1_SET_Clicked:
        SC_Y1_DATA_SET = SC_Y1_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y1_DATA_CLEAR != SC_Y1_CLEAR_Clicked:
        SC_Y1_DATA_CLEAR = SC_Y1_CLEAR_Clicked
        return [""]
####################################################################################
## Y2 Data
####################################################################################
SC_Y2_DATA_SET = 0
SC_Y2_DATA_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y2_DATA_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y2_DATA_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y2_DATA_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y2_SET_Clicked, SC_Y2_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y2_DATA_SET, SC_Y2_DATA_CLEAR

    if type(RunningExcelGraph) != str and SC_Y2_DATA_SET != SC_Y2_SET_Clicked:
        SC_Y2_DATA_SET = SC_Y2_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y2_DATA_CLEAR != SC_Y2_CLEAR_Clicked:
        SC_Y2_DATA_CLEAR = SC_Y2_CLEAR_Clicked
        return [""]
####################################################################################
## Y3 Data
####################################################################################
SC_Y3_DATA_SET = 0
SC_Y3_DATA_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y3_DATA_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y3_DATA_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y3_DATA_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y3_SET_Clicked, SC_Y3_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y3_DATA_SET, SC_Y3_DATA_CLEAR

    if type(RunningExcelGraph) != str and SC_Y3_DATA_SET != SC_Y3_SET_Clicked:
        SC_Y3_DATA_SET = SC_Y3_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y3_DATA_CLEAR != SC_Y3_CLEAR_Clicked:
        SC_Y3_DATA_CLEAR = SC_Y3_CLEAR_Clicked
        return [""]
####################################################################################
## Y4 Data
####################################################################################
SC_Y4_DATA_SET = 0
SC_Y4_DATA_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y4_DATA_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y4_DATA_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y4_DATA_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y4_SET_Clicked, SC_Y4_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y4_DATA_SET, SC_Y4_DATA_CLEAR

    if type(RunningExcelGraph) != str and SC_Y4_DATA_SET != SC_Y4_SET_Clicked:
        SC_Y4_DATA_SET = SC_Y4_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y4_DATA_CLEAR != SC_Y4_CLEAR_Clicked:
        SC_Y4_DATA_CLEAR = SC_Y4_CLEAR_Clicked
        return [""]
####################################################################################
## Y5 Data
####################################################################################
SC_Y5_DATA_SET = 0
SC_Y5_DATA_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y5_DATA_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y5_DATA_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y5_DATA_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y5_SET_Clicked, SC_Y5_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y5_DATA_SET, SC_Y5_DATA_CLEAR

    if type(RunningExcelGraph) != str and SC_Y5_DATA_SET != SC_Y5_SET_Clicked:
        SC_Y5_DATA_SET = SC_Y5_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y5_DATA_CLEAR != SC_Y5_CLEAR_Clicked:
        SC_Y5_DATA_CLEAR = SC_Y5_CLEAR_Clicked
        return [""]
####################################################################################
## Y6 Data
####################################################################################
SC_Y6_DATA_SET = 0
SC_Y6_DATA_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y6_DATA_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y6_DATA_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y6_DATA_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y6_SET_Clicked, SC_Y6_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y6_DATA_SET, SC_Y6_DATA_CLEAR

    if type(RunningExcelGraph) != str and SC_Y6_DATA_SET != SC_Y6_SET_Clicked:
        SC_Y6_DATA_SET = SC_Y6_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y6_DATA_CLEAR != SC_Y6_CLEAR_Clicked:
        SC_Y3_DATA_CLEAR = SC_Y6_CLEAR_Clicked
        return [""]
####################################################################################
## Y7 Data
####################################################################################
SC_Y7_DATA_SET = 0
SC_Y7_DATA_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y7_DATA_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y7_DATA_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y7_DATA_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y7_SET_Clicked, SC_Y7_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y7_DATA_SET, SC_Y7_DATA_CLEAR

    if type(RunningExcelGraph) != str and SC_Y7_DATA_SET != SC_Y7_SET_Clicked:
        SC_Y7_DATA_SET = SC_Y7_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y7_DATA_CLEAR != SC_Y7_CLEAR_Clicked:
        SC_Y7_DATA_CLEAR = SC_Y7_CLEAR_Clicked
        return [""]
####################################################################################
# x1 Name
####################################################################################
SC_X1_NAME_SET = 0
SC_X1_NAME_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X1_NAME_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X1_NAME_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X1_NAME_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X1_NAME_SET_Clicked, SC_X1_NAME_CLEAR_Clicked):
    global RunningExcelGraph, SC_X1_NAME_SET, SC_X1_NAME_CLEAR

    if type(RunningExcelGraph) != str and SC_X1_NAME_SET != SC_X1_NAME_SET_Clicked:
        SC_X1_NAME_SET = SC_X1_NAME_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X1_NAME_CLEAR != SC_X1_NAME_CLEAR_Clicked:
        SC_X1_NAME_CLEAR = SC_X1_NAME_CLEAR_Clicked
        return [""]
####################################################################################
# x2 Name
####################################################################################
SC_X2_NAME_SET = 0
SC_X2_NAME_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X2_NAME_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X2_NAME_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X2_NAME_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X2_NAME_SET_Clicked, SC_X2_NAME_CLEAR_Clicked):
    global RunningExcelGraph, SC_X2_NAME_SET, SC_X2_NAME_CLEAR

    if type(RunningExcelGraph) != str and SC_X2_NAME_SET != SC_X2_NAME_SET_Clicked:
        SC_X2_NAME_SET = SC_X2_NAME_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X2_NAME_CLEAR != SC_X2_NAME_CLEAR_Clicked:
        SC_X2_NAME_CLEAR = SC_X2_NAME_CLEAR_Clicked
        return [""]
####################################################################################
# x3 Name
####################################################################################
SC_X3_NAME_SET = 0
SC_X3_NAME_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X3_NAME_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X3_NAME_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X3_NAME_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X3_NAME_SET_Clicked, SC_X3_NAME_CLEAR_Clicked):
    global RunningExcelGraph, SC_X3_NAME_SET, SC_X3_NAME_CLEAR

    if type(RunningExcelGraph) != str and SC_X3_NAME_SET != SC_X3_NAME_SET_Clicked:
        SC_X3_NAME_SET = SC_X3_NAME_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X3_NAME_CLEAR != SC_X3_NAME_CLEAR_Clicked:
        SC_X3_NAME_CLEAR = SC_X3_NAME_CLEAR_Clicked
        return [""]
####################################################################################
# x4 Name
####################################################################################
SC_X4_NAME_SET = 0
SC_X4_NAME_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X4_NAME_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X4_NAME_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X4_NAME_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X4_NAME_SET_Clicked, SC_X4_NAME_CLEAR_Clicked):
    global RunningExcelGraph, SC_X4_NAME_SET, SC_X4_NAME_CLEAR

    if type(RunningExcelGraph) != str and SC_X4_NAME_SET != SC_X4_NAME_SET_Clicked:
        SC_X4_NAME_SET = SC_X4_NAME_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X4_NAME_CLEAR != SC_X4_NAME_CLEAR_Clicked:
        SC_X4_NAME_CLEAR = SC_X4_NAME_CLEAR_Clicked
        return [""]
####################################################################################
# x5 Name
####################################################################################
SC_X5_NAME_SET = 0
SC_X5_NAME_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X5_NAME_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X5_NAME_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X5_NAME_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X5_NAME_SET_Clicked, SC_X5_NAME_CLEAR_Clicked):
    global RunningExcelGraph, SC_X5_NAME_SET, SC_X5_NAME_CLEAR

    if type(RunningExcelGraph) != str and SC_X5_NAME_SET != SC_X5_NAME_SET_Clicked:
        SC_X5_NAME_SET = SC_X5_NAME_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X5_NAME_CLEAR != SC_X5_NAME_CLEAR_Clicked:
        SC_X5_NAME_CLEAR = SC_X5_NAME_CLEAR_Clicked
        return [""]
####################################################################################
# x6 Name
####################################################################################
SC_X6_NAME_SET = 0
SC_X6_NAME_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X6_NAME_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X6_NAME_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X6_NAME_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X6_NAME_SET_Clicked, SC_X6_NAME_CLEAR_Clicked):
    global RunningExcelGraph, SC_X6_NAME_SET, SC_X6_NAME_CLEAR

    if type(RunningExcelGraph) != str and SC_X6_NAME_SET != SC_X6_NAME_SET_Clicked:
        SC_X6_NAME_SET = SC_X6_NAME_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X6_NAME_CLEAR != SC_X6_NAME_CLEAR_Clicked:
        SC_X6_NAME_CLEAR = SC_X6_NAME_CLEAR_Clicked
        return [""]
####################################################################################
# x7 Name
####################################################################################
SC_X7_NAME_SET = 0
SC_X7_NAME_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X7_NAME_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X7_NAME_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X7_NAME_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X7_NAME_SET_Clicked, SC_X7_NAME_CLEAR_Clicked):
    global RunningExcelGraph, SC_X7_NAME_SET, SC_X7_NAME_CLEAR

    if type(RunningExcelGraph) != str and SC_X7_NAME_SET != SC_X7_NAME_SET_Clicked:
        SC_X7_NAME_SET = SC_X7_NAME_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X7_NAME_CLEAR != SC_X7_NAME_CLEAR_Clicked:
        SC_X7_NAME_CLEAR = SC_X7_NAME_CLEAR_Clicked
        return [""]
####################################################################################
# y1 Name
####################################################################################
SC_Y1_NAME_SET = 0
SC_Y1_NAME_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y1_NAME_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y1_NAME_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y1_NAME_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y1_NAME_SET_Clicked, SC_Y1_NAME_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y1_NAME_SET, SC_Y1_NAME_CLEAR

    if type(RunningExcelGraph) != str and SC_Y1_NAME_SET != SC_Y1_NAME_SET_Clicked:
        SC_Y1_NAME_SET = SC_Y1_NAME_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y1_NAME_CLEAR != SC_Y1_NAME_CLEAR_Clicked:
        SC_Y1_NAME_CLEAR = SC_Y1_NAME_CLEAR_Clicked
        return [""]
####################################################################################
# y2 Name
####################################################################################
SC_Y2_NAME_SET = 0
SC_Y2_NAME_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y2_NAME_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y2_NAME_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y2_NAME_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y2_NAME_SET_Clicked, SC_Y2_NAME_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y2_NAME_SET, SC_Y2_NAME_CLEAR

    if type(RunningExcelGraph) != str and SC_Y2_NAME_SET != SC_Y2_NAME_SET_Clicked:
        SC_Y2_NAME_SET = SC_Y2_NAME_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y2_NAME_CLEAR != SC_Y2_NAME_CLEAR_Clicked:
        SC_Y2_NAME_CLEAR = SC_Y2_NAME_CLEAR_Clicked
        return [""]
####################################################################################
# y3 Name
####################################################################################
SC_Y3_NAME_SET = 0
SC_Y3_NAME_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y3_NAME_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y3_NAME_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y3_NAME_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y3_NAME_SET_Clicked, SC_Y3_NAME_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y3_NAME_SET, SC_Y3_NAME_CLEAR

    if type(RunningExcelGraph) != str and SC_Y3_NAME_SET != SC_Y3_NAME_SET_Clicked:
        SC_Y3_NAME_SET = SC_Y3_NAME_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y3_NAME_CLEAR != SC_Y3_NAME_CLEAR_Clicked:
        SC_Y3_NAME_CLEAR = SC_Y3_NAME_CLEAR_Clicked
        return [""]
####################################################################################
# y4 Name
####################################################################################
SC_Y4_NAME_SET = 0
SC_Y4_NAME_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y4_NAME_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y4_NAME_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y4_NAME_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y4_NAME_SET_Clicked, SC_Y4_NAME_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y4_NAME_SET, SC_Y4_NAME_CLEAR

    if type(RunningExcelGraph) != str and SC_Y4_NAME_SET != SC_Y4_NAME_SET_Clicked:
        SC_Y4_NAME_SET = SC_Y4_NAME_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y4_NAME_CLEAR != SC_Y4_NAME_CLEAR_Clicked:
        SC_Y4_NAME_CLEAR = SC_Y4_NAME_CLEAR_Clicked
        return [""]


####################################################################################
# y5 Name
####################################################################################
SC_Y5_NAME_SET = 0
SC_Y5_NAME_CLEAR = 0

@app.callback(
    Output(component_id="SC_BT_Y5_NAME_INPUT", component_property="value"),
    [Input(component_id="SC_BT_Y5_NAME_SET", component_property="n_clicks"),
     Input(component_id="SC_BT_Y5_NAME_CLEAR", component_property="n_clicks")])
def update_output(SC_Y5_NAME_SET_Clicked, SC_Y5_NAME_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y5_NAME_SET, SC_Y5_NAME_CLEAR

    if type(RunningExcelGraph) != str and SC_Y5_NAME_SET != SC_Y5_NAME_SET_Clicked:
        SC_Y5_NAME_SET = SC_Y5_NAME_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y5_NAME_CLEAR != SC_Y5_NAME_CLEAR_Clicked:
        SC_Y5_NAME_CLEAR = SC_Y5_NAME_CLEAR_Clicked
        return [""]
####################################################################################
# y6 Name
####################################################################################
SC_Y6_NAME_SET = 0
SC_Y6_NAME_CLEAR = 0

@app.callback(
    Output(component_id="SC_BT_Y6_NAME_INPUT", component_property="value"),
    [Input(component_id="SC_BT_Y6_NAME_SET", component_property="n_clicks"),
     Input(component_id="SC_BT_Y6_NAME_CLEAR", component_property="n_clicks")])
def update_output(SC_Y6_NAME_SET_Clicked, SC_Y6_NAME_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y6_NAME_SET, SC_Y6_NAME_CLEAR

    if type(RunningExcelGraph) != str and SC_Y6_NAME_SET != SC_Y6_NAME_SET_Clicked:
        SC_Y6_NAME_SET = SC_Y6_NAME_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y6_NAME_CLEAR != SC_Y6_NAME_CLEAR_Clicked:
        SC_Y6_NAME_CLEAR = SC_Y6_NAME_CLEAR_Clicked
        return [""]
####################################################################################
# y7 Name
####################################################################################
SC_Y7_NAME_SET = 0
SC_Y7_NAME_CLEAR = 0

@app.callback(
    Output(component_id="SC_BT_Y7_NAME_INPUT", component_property="value"),
    [Input(component_id="SC_BT_Y7_NAME_SET", component_property="n_clicks"),
     Input(component_id="SC_BT_Y7_NAME_CLEAR", component_property="n_clicks")])
def update_output(SC_Y7_NAME_SET_Clicked, SC_Y7_NAME_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y7_NAME_SET, SC_Y7_NAME_CLEAR

    if type(RunningExcelGraph) != str and SC_Y7_NAME_SET != SC_Y7_NAME_SET_Clicked:
        SC_Y7_NAME_SET = SC_Y7_NAME_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y7_NAME_CLEAR != SC_Y7_NAME_CLEAR_Clicked:
        SC_Y7_NAME_CLEAR = SC_Y7_NAME_CLEAR_Clicked
        return [""]
####################################################################################

# X1 UNIT
####################################################################################
SC_X1_UNIT_SET = 0
SC_X1_UNIT_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X1_UNIT_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X1_UNIT_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X1_UNIT_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X1_SET_Clicked, SC_X1_CLEAR_Clicked):
    global RunningExcelGraph, SC_X1_UNIT_SET, SC_X1_UNIT_CLEAR

    if type(RunningExcelGraph) != str and SC_X1_UNIT_SET != SC_X1_SET_Clicked:
        SC_X1_UNIT_SET = SC_X1_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X1_UNIT_CLEAR != SC_X1_CLEAR_Clicked:
        SC_X1_UNIT_CLEAR = SC_X1_CLEAR_Clicked
        return [""]
####################################################################################

# X2 UNIT
####################################################################################
SC_X2_UNIT_SET = 0
SC_X2_UNIT_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X2_UNIT_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X2_UNIT_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X2_UNIT_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X2_SET_Clicked, SC_X2_CLEAR_Clicked):
    global RunningExcelGraph, SC_X2_UNIT_SET, SC_X2_UNIT_CLEAR

    if type(RunningExcelGraph) != str and SC_X2_UNIT_SET != SC_X2_SET_Clicked:
        SC_X2_UNIT_SET = SC_X2_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X2_UNIT_CLEAR != SC_X2_CLEAR_Clicked:
        SC_X2_UNIT_CLEAR = SC_X2_CLEAR_Clicked
        return [""]
####################################################################################

# X3 UNIT
####################################################################################
SC_X3_UNIT_SET = 0
SC_X3_UNIT_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X3_UNIT_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X3_UNIT_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X3_UNIT_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X3_SET_Clicked, SC_X3_CLEAR_Clicked):
    global RunningExcelGraph, SC_X3_UNIT_SET, SC_X3_UNIT_CLEAR

    if type(RunningExcelGraph) != str and SC_X3_UNIT_SET != SC_X3_SET_Clicked:
        SC_X3_UNIT_SET = SC_X3_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X3_UNIT_CLEAR != SC_X3_CLEAR_Clicked:
        SC_X3_UNIT_CLEAR = SC_X3_CLEAR_Clicked
        return [""]
####################################################################################

# X4 UNIT
####################################################################################
SC_X4_UNIT_SET = 0
SC_X4_UNIT_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X4_UNIT_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X4_UNIT_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X4_UNIT_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X4_SET_Clicked, SC_X4_CLEAR_Clicked):
    global RunningExcelGraph, SC_X4_UNIT_SET, SC_X4_UNIT_CLEAR

    if type(RunningExcelGraph) != str and SC_X4_UNIT_SET != SC_X4_SET_Clicked:
        SC_X4_UNIT_SET = SC_X4_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X4_UNIT_CLEAR != SC_X4_CLEAR_Clicked:
        SC_X4_UNIT_CLEAR = SC_X4_CLEAR_Clicked
        return [""]
####################################################################################

# X5 UNIT
####################################################################################
SC_X5_UNIT_SET = 0
SC_X5_UNIT_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X5_UNIT_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X5_UNIT_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X5_UNIT_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X5_SET_Clicked, SC_X5_CLEAR_Clicked):
    global RunningExcelGraph, SC_X5_UNIT_SET, SC_X5_UNIT_CLEAR

    if type(RunningExcelGraph) != str and SC_X5_UNIT_SET != SC_X5_SET_Clicked:
        SC_X5_UNIT_SET = SC_X5_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X5_UNIT_CLEAR != SC_X5_CLEAR_Clicked:
        SC_X5_UNIT_CLEAR = SC_X5_CLEAR_Clicked
        return [""]
####################################################################################

# X6 UNIT
####################################################################################
SC_X6_UNIT_SET = 0
SC_X6_UNIT_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X6_UNIT_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X6_UNIT_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X6_UNIT_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X6_SET_Clicked, SC_X6_CLEAR_Clicked):
    global RunningExcelGraph, SC_X6_UNIT_SET, SC_X6_UNIT_CLEAR

    if type(RunningExcelGraph) != str and SC_X6_UNIT_SET != SC_X6_SET_Clicked:
        SC_X6_UNIT_SET = SC_X6_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X6_UNIT_CLEAR != SC_X6_CLEAR_Clicked:
        SC_X6_UNIT_CLEAR = SC_X6_CLEAR_Clicked
        return [""]
####################################################################################

# X7 UNIT
####################################################################################
SC_X7_UNIT_SET = 0
SC_X7_UNIT_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X7_UNIT_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X7_UNIT_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X7_UNIT_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X7_SET_Clicked, SC_X7_CLEAR_Clicked):
    global RunningExcelGraph, SC_X7_UNIT_SET, SC_X7_UNIT_CLEAR

    if type(RunningExcelGraph) != str and SC_X7_UNIT_SET != SC_X7_SET_Clicked:
        SC_X7_UNIT_SET = SC_X7_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X7_UNIT_CLEAR != SC_X7_CLEAR_Clicked:
        SC_X7_UNIT_CLEAR = SC_X7_CLEAR_Clicked
        return [""]
####################################################################################

# Y1 UNIT
####################################################################################
SC_Y1_UNIT_SET = 0
SC_Y1_UNIT_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y1_UNIT_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y1_UNIT_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y1_UNIT_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y1_SET_Clicked, SC_Y1_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y1_UNIT_SET, SC_Y1_UNIT_CLEAR

    if type(RunningExcelGraph) != str and SC_Y1_UNIT_SET != SC_Y1_SET_Clicked:
        SC_Y1_UNIT_SET = SC_Y1_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y1_UNIT_CLEAR != SC_Y1_CLEAR_Clicked:
        SC_Y1_UNIT_CLEAR = SC_Y1_CLEAR_Clicked
        return [""]
####################################################################################
# Y2 UNIT
####################################################################################
SC_Y2_UNIT_SET = 0
SC_Y2_UNIT_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y2_UNIT_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y2_UNIT_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y2_UNIT_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y2_SET_Clicked, SC_Y2_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y2_UNIT_SET, SC_Y2_UNIT_CLEAR

    if type(RunningExcelGraph) != str and SC_Y2_UNIT_SET != SC_Y2_SET_Clicked:
        SC_Y2_UNIT_SET = SC_Y2_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y2_UNIT_CLEAR != SC_Y2_CLEAR_Clicked:
        SC_Y2_UNIT_CLEAR = SC_Y2_CLEAR_Clicked
        return [""]
####################################################################################

# Y3 UNIT
####################################################################################
SC_Y3_UNIT_SET = 0
SC_Y3_UNIT_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y3_UNIT_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y3_UNIT_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y3_UNIT_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y3_SET_Clicked, SC_Y3_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y3_UNIT_SET, SC_Y3_UNIT_CLEAR

    if type(RunningExcelGraph) != str and SC_Y3_UNIT_SET != SC_Y3_SET_Clicked:
        SC_Y3_UNIT_SET = SC_Y3_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y3_UNIT_CLEAR != SC_Y3_CLEAR_Clicked:
        SC_Y3_UNIT_CLEAR = SC_Y3_CLEAR_Clicked
        return [""]
####################################################################################

# Y4 UNIT
####################################################################################
SC_Y4_UNIT_SET = 0
SC_Y4_UNIT_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y4_UNIT_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y4_UNIT_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y4_UNIT_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y4_SET_Clicked, SC_Y4_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y4_UNIT_SET, SC_Y4_UNIT_CLEAR

    if type(RunningExcelGraph) != str and SC_Y4_UNIT_SET != SC_Y4_SET_Clicked:
        SC_Y4_UNIT_SET = SC_Y4_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y4_UNIT_CLEAR != SC_Y4_CLEAR_Clicked:
        SC_Y4_UNIT_CLEAR = SC_Y4_CLEAR_Clicked
        return [""]
####################################################################################

# Y5 UNIT
####################################################################################
SC_Y5_UNIT_SET = 0
SC_Y5_UNIT_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y5_UNIT_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y5_UNIT_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y5_UNIT_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y5_SET_Clicked, SC_Y5_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y5_UNIT_SET, SC_Y5_UNIT_CLEAR

    if type(RunningExcelGraph) != str and SC_Y5_UNIT_SET != SC_Y5_SET_Clicked:
        SC_Y5_UNIT_SET = SC_Y5_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y5_UNIT_CLEAR != SC_Y5_CLEAR_Clicked:
        SC_Y5_UNIT_CLEAR = SC_Y5_CLEAR_Clicked
        return [""]
####################################################################################

# Y6 UNIT
####################################################################################
SC_Y6_UNIT_SET = 0
SC_Y6_UNIT_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y6_UNIT_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y6_UNIT_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y6_UNIT_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y6_SET_Clicked, SC_Y6_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y6_UNIT_SET, SC_Y6_UNIT_CLEAR

    if type(RunningExcelGraph) != str and SC_Y6_UNIT_SET != SC_Y6_SET_Clicked:
        SC_Y6_UNIT_SET = SC_Y6_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y6_UNIT_CLEAR != SC_Y6_CLEAR_Clicked:
        SC_Y6_UNIT_CLEAR = SC_Y6_CLEAR_Clicked
        return [""]
####################################################################################

# Y7 UNIT
####################################################################################
SC_Y7_UNIT_SET = 0
SC_Y7_UNIT_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y7_UNIT_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y7_UNIT_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y7_UNIT_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y7_SET_Clicked, SC_Y7_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y7_UNIT_SET, SC_Y7_UNIT_CLEAR

    if type(RunningExcelGraph) != str and SC_Y7_UNIT_SET != SC_Y7_SET_Clicked:
        SC_Y7_UNIT_SET = SC_Y7_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y7_UNIT_CLEAR != SC_Y7_CLEAR_Clicked:
        SC_Y7_UNIT_CLEAR = SC_Y7_CLEAR_Clicked
        return [""]
####################################################################################

# TITLE
####################################################################################
SC_TITLE_TEXT_SET = 0
SC_TITLE_TEXT_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_TITLE_TEXT_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_TITLE_TEXT_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_TITLE_TEXT_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X1_SET_Clicked, SC_X1_CLEAR_Clicked):
    global RunningExcelGraph, SC_TITLE_TEXT_SET, SC_TITLE_TEXT_CLEAR

    if type(RunningExcelGraph) != str and SC_TITLE_TEXT_SET != SC_X1_SET_Clicked:
        SC_TITLE_TEXT_SET = SC_X1_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_TITLE_TEXT_CLEAR != SC_X1_CLEAR_Clicked:
        SC_TITLE_TEXT_CLEAR = SC_X1_CLEAR_Clicked
        return [""]
####################################################################################

####################################################################################
SC_TITLE_SIZE_SET = 0
SC_TITLE_SIZE_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_TITLE_SIZE_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_TITLE_SIZE_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_TITLE_SIZE_CLEAR",component_property=  "n_clicks")])
def update_output(SC_TITLE_SIZE_SET_Clicked, SC_TITLE_SIZE_CLEAR_Clicked):
    global RunningExcelGraph, SC_TITLE_SIZE_SET, SC_TITLE_SIZE_CLEAR

    if type(RunningExcelGraph) != str and SC_TITLE_SIZE_SET != SC_TITLE_SIZE_SET_Clicked:
        SC_TITLE_SIZE_SET = SC_TITLE_SIZE_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_TITLE_SIZE_CLEAR != SC_TITLE_SIZE_CLEAR_Clicked:
        SC_TITLE_SIZE_CLEAR = SC_TITLE_SIZE_CLEAR_Clicked
        return 10
####################################################################################


# VIEW RANGE X UP
####################################################################################
SC_X_UP_VIEW_SET = 0
SC_X_UP_VIEW_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X_UP_VIEW_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X_UP_VIEW_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X_UP_VIEW_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X_UP_SET_Clicked, SC_X_UP_CLEAR_Clicked):
    global RunningExcelGraph, SC_X_UP_VIEW_SET, SC_X_UP_VIEW_CLEAR

    if type(RunningExcelGraph) != str and SC_X_UP_VIEW_SET != SC_X_UP_SET_Clicked:
        SC_X_UP_VIEW_SET = SC_X_UP_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X_UP_VIEW_CLEAR != SC_X_UP_CLEAR_Clicked:
        SC_X_UP_VIEW_CLEAR = SC_X_UP_CLEAR_Clicked
        return [""]
####################################################################################

# VIEW RANGE X LOW
####################################################################################
SC_X_LOW_VIEW_SET = 0
SC_X_LOW_VIEW_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_X_LOW_VIEW_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_X_LOW_VIEW_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_X_LOW_VIEW_CLEAR",component_property=  "n_clicks")])
def update_output(SC_X_LOW_SET_Clicked, SC_X_LOW_CLEAR_Clicked):
    global RunningExcelGraph, SC_X_LOW_VIEW_SET, SC_X_LOW_VIEW_CLEAR

    if type(RunningExcelGraph) != str and SC_X_LOW_VIEW_SET != SC_X_LOW_SET_Clicked:
        SC_X_LOW_VIEW_SET = SC_X_LOW_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_X_LOW_VIEW_CLEAR != SC_X_LOW_CLEAR_Clicked:
        SC_X_LOW_VIEW_CLEAR = SC_X_LOW_CLEAR_Clicked
        return [""]
####################################################################################

# VIEW RANGE Y UP
####################################################################################
SC_Y_UP_VIEW_SET = 0
SC_Y_UP_VIEW_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y_UP_VIEW_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y_UP_VIEW_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y_UP_VIEW_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y_UP_SET_Clicked, SC_Y_UP_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y_UP_VIEW_SET, SC_Y_UP_VIEW_CLEAR

    if type(RunningExcelGraph) != str and SC_Y_UP_VIEW_SET != SC_Y_UP_SET_Clicked:
        SC_Y_UP_VIEW_SET = SC_Y_UP_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y_UP_VIEW_CLEAR != SC_Y_UP_CLEAR_Clicked:
        SC_Y_UP_VIEW_CLEAR = SC_Y_UP_CLEAR_Clicked
        return [""]
####################################################################################

# VIEW RANGE Y LOW
####################################################################################
SC_Y_LOW_VIEW_SET = 0
SC_Y_LOW_VIEW_CLEAR = 0
@app.callback(
    Output(component_id="SC_BT_Y_LOW_VIEW_INPUT",component_property=  "value"),
    [Input(component_id="SC_BT_Y_LOW_VIEW_SET",component_property=  "n_clicks"),
     Input(component_id="SC_BT_Y_LOW_VIEW_CLEAR",component_property=  "n_clicks")])
def update_output(SC_Y_LOW_SET_Clicked, SC_Y_LOW_CLEAR_Clicked):
    global RunningExcelGraph, SC_Y_LOW_VIEW_SET, SC_Y_LOW_VIEW_CLEAR

    if type(RunningExcelGraph) != str and SC_Y_LOW_VIEW_SET != SC_Y_LOW_SET_Clicked:
        SC_Y_LOW_VIEW_SET = SC_Y_LOW_SET_Clicked
        GotInfo = RunningExcelGraph.GetSelectedArea()
        return GotInfo

    elif type(RunningExcelGraph) != str and SC_Y_LOW_VIEW_CLEAR != SC_Y_LOW_CLEAR_Clicked:
        SC_Y_LOW_VIEW_CLEAR = SC_Y_LOW_CLEAR_Clicked
        return [""]
####################################################################################
####################################################################################
if __name__ == "__main__":
    Input_Data = [0.1,0.1,0.2,0.2,0.2,0.2,0.2,0.2,0.1,0.1,0.5,0.1]

    #Plotly_Scatter(x1_Data=Axis_Data,x1_Name="X",y1_Data=Vertical_Data,y1_Name='Y',Vertical_ViewRange_Lower=-120,Vertical_ViewRange_Upper=5)
    #xw.serve()
    SampleGraph = PlotlyGraphGenerator()
