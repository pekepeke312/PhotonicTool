import numpy as np
import pandas as pd
import os
# import math
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)
from TextWriter import TextWriter

ColourTable = {
    0: "blue",
    1: "orange",
    2: "green",
    3: "red",
    4: "MediumPurple",
    5: "gray",
    6: "gold"
}

SequenceColumn = {
    'Sequence Number': 1,
    'Mode': 3,
    'Direction': 2,
    'I2C Add': 4,
    'SPI CS': 5,
    'Sending Data': 6,
}
for GPIONumber in range(16):
    SequenceColumn['GPIO_' + str(GPIONumber)] = GPIONumber + 7

SIGNAL_NAME = ["I2C-SCL / GPIO-00",# "SPI-CS1 / GPIO-04",
               "I2C-SDA / GPIO-01",# "SPI-CS2 / GPIO-03",
               "SPI-SCLK",# "SPI-CS3 / GPIO-05",
               "SPI-MOSI",# "SPI-CS4 / GPIO-06",
               #"SPI-CS0 / GPIO-02",  "SPI-CS5 / GPIO-07",
               ]

GPIO_MAP = [2, 4, 3, 5, 6, 7, 8, 15]  # GPIO Pin Number mapping per CS number
SAMPLING_CLK = pow(10,7)

class Promira_Serial_Control:
    def __init__(self, FilePath):
        self.MakingDirectory()
        self.CurrentMode = "GPIO"
        self.FileLocation = FilePath
        self.Excel_File_Loader(FileName=self.FileLocation)
        self.SequenceRun()

    def MakingDirectory(self) -> None:
        path_desktop = os.environ['USERPROFILE'] + str('\\Desktop\\')
        XMLFileDir = path_desktop + "Promira_Batch_files"
        if os.path.isdir(XMLFileDir):
            pass
        else:
            os.mkdir(XMLFileDir)
    def GUI_Control(self, Sheet = "Sheet") -> None:

        self.PlotlyGraph[Sheet] = make_subplots(rows=4,
                                         cols=1,#2,
                                         shared_xaxes=True,
                                         vertical_spacing=0.1,
                                         subplot_titles=SIGNAL_NAME,
                                         )
        # self.PlotlyGraph[Sheet] = temp

        # self.LstTime = {}

        self.WaveData_Genarater(Sheet=Sheet)

        Time_wunit = {}
        Time_wunit[Sheet] = self.Add_Desimal_Unit(self.MasterWaveData[Sheet]['Time'])
        customdata_I2C = {}

        templist = []
        if len(self.MasterWaveData[Sheet]["I2C_SCL"]) != 0 and len(self.MasterWaveData[Sheet]["SPI_SCLK"]) != 0:
            for n in range(len(self.MasterWaveData[Sheet]["Time"])):
                templist.append([
                        Time_wunit[Sheet][n],
                        self.MasterWaveData[Sheet]["I2C_DataName"][n],
                        self.MasterWaveData[Sheet]["I2C_SCL"][n],
                        self.MasterWaveData[Sheet]["I2C_SDA"][n],
                        self.MasterWaveData[Sheet]["SPI_DataName"][n],
                        self.MasterWaveData[Sheet]["SPI_SCLK"][n],
                        self.MasterWaveData[Sheet]["SPI_MOSI"][n],
                ])
            customdata_I2C[Sheet] = templist

        if len(self.MasterWaveData[Sheet]["I2C_SCL"]) == 0 and len(self.MasterWaveData[Sheet]["SPI_SCLK"]) != 0:
            for n in range(len(self.MasterWaveData[Sheet]["Time"])):
                templist.append([
                        Time_wunit[Sheet][n],
                        0,
                        0,
                        0,
                        self.MasterWaveData[Sheet]["SPI_DataName"][n],
                        self.MasterWaveData[Sheet]["SPI_SCLK"][n],
                        self.MasterWaveData[Sheet]["SPI_MOSI"][n],
                ])
            customdata_I2C[Sheet] = templist

        if len(self.MasterWaveData[Sheet]["I2C_SCL"]) != 0 and len(self.MasterWaveData[Sheet]["SPI_SCLK"]) == 0:
            for n in range(len(self.MasterWaveData[Sheet]["Time"])):
                templist.append([
                        Time_wunit[Sheet][n],
                        self.MasterWaveData[Sheet]["I2C_DataName"][n],
                        self.MasterWaveData[Sheet]["I2C_SCL"][n],
                        self.MasterWaveData[Sheet]["I2C_SDA"][n],
                        0,
                        0,
                        0,
                ])
            customdata_I2C[Sheet] = templist

        self.PlotlyGraph[Sheet].add_trace(
            go.Scatter(
                visible=True,
                x=self.MasterWaveData[Sheet]["Time"],
                y=self.MasterWaveData[Sheet]["I2C_SCL"],
                text=[f'Time: {Time}s <br>{DataName} <br> I2C-SCL: {SCL}' for [Time, DataName, SCL, SDA, SPI_NAME, SCLK, MOSI] in customdata_I2C[Sheet]],
                hoverinfo='text',
                name='I2C-SCL',
                line=dict(color=ColourTable[0])
            ),
            row=1, col=1,
        ),

        self.PlotlyGraph[Sheet].add_trace(
            go.Scatter(
                visible=True,
                x=self.MasterWaveData[Sheet]["Time"],
                y=self.MasterWaveData[Sheet]["I2C_SDA"],
                text=[f'Time: {Time}s <br>{DataName} <br>I2C-SDA: {SDA}' for [Time, DataName, SCL, SDA, SPI_NAME,SCLK, MOSI] in customdata_I2C[Sheet]],
                hoverinfo='text',
                name='I2C-SDA',
                line=dict(color=ColourTable[1])
            ),
            row=2, col=1,
        ),

        self.PlotlyGraph[Sheet].add_trace(
            go.Scatter(
                visible=True,
                x=self.MasterWaveData[Sheet]["Time"],
                y=self.MasterWaveData[Sheet]["SPI_SCLK"],
                text=[f'Time: {Time}s <br>{SPI_NAME} <br> SPI-SCLK: {SCLK}' for [Time, DataName, SCL, SDA, SPI_NAME,SCLK, MOSI] in customdata_I2C[Sheet]],
                hoverinfo='text',
                name='SPI-SCLK',
                line=dict(color=ColourTable[2])
            ),
            row=3, col=1,
        ),

        self.PlotlyGraph[Sheet].add_trace(
            go.Scatter(
                visible=True,
                x=self.MasterWaveData[Sheet]["Time"],
                y=self.MasterWaveData[Sheet]["SPI_MOSI"],
                text=[f'Time: {Time}s <br>{SPI_NAME} <br> SPI-MOSI: {MOSI}' for [Time, DataName, SCL, SDA, SPI_NAME,SCLK, MOSI] in customdata_I2C[Sheet]],
                hoverinfo='text',
                name='SPI-MOSI',
                line=dict(color=ColourTable[3])
            ),
            row=4, col=1,
        ),

        self.PlotlyGraph[Sheet].update_layout(
            title=dict(
                text='Expected Waveform from Promira Serial with "' + Sheet +'"',
                xanchor='auto'
            ),
            title_font=dict(
                size=20
            ),
        )

        # self.PlotlyGraph["layout"]["sliders"] = [self.SliderSetting(RangeList=self.Add_Desimal_Unit(self.MasterWaveData['Time']))]

        self.PlotlyGraph[Sheet].show()
        # print(fr"Waveform Viewer is Not Implemented")
        # TextWriter(fr"Waveform Viewer is Not Implemented")

    def SPI_Add_X(self, Sheet, TickTime, Bit=0, AMP=0, Name="",SPI_MODE=0, CLKSLEEP=False):
        if not CLKSLEEP:
            if SPI_MODE == 0 or SPI_MODE ==3:
                self.WaveData[Sheet]["SPI_SCLK"].append(0.0)
                self.WaveData[Sheet]["SPI_SCLK"].append(AMP)
            elif SPI_MODE == 1 or SPI_MODE == 2:
                self.WaveData[Sheet]["SPI_SCLK"].append(AMP)
                self.WaveData[Sheet]["SPI_SCLK"].append(0.0)
        else:
            if SPI_MODE == 0 or SPI_MODE == 1:
                for _ in range(2): self.WaveData[Sheet]['SPI_SCLK'].append(0.0)
            elif SPI_MODE == 2 or SPI_MODE == 3:
                for _ in range(2): self.WaveData[Sheet]['SPI_SCLK'].append(AMP)

        if str(Bit) == '1':
            for _ in range(2): self.WaveData[Sheet]['SPI_MOSI'].append(AMP)
        elif str(Bit) == '0':
            for _ in range(2): self.WaveData[Sheet]['SPI_MOSI'].append(0.0)

        for _ in range(2): self.WaveData[Sheet]['SPI_Time'].append(self.WaveData[Sheet]['SPI_Time'][-1] + TickTime)
        for _ in range(2): self.WaveData[Sheet]['SPI_DataName'].append(Name)

    def I2C_Add_X(self, Sheet, TickTime, Bit=0, AMP=0, Name="", CLKSLEEP=False, Init=False):
        if Init == True:
            for _ in range(4): self.WaveData[Sheet]['I2C_DataName'].append(Name)
            for _ in range(4): self.WaveData[Sheet]['I2C_SCL'].append(AMP)
            for _ in range(4): self.WaveData[Sheet]['I2C_SDA'].append(AMP)
            for _ in range(4): self.WaveData[Sheet]['I2C_Time'].append(self.WaveData[Sheet]['I2C_Time'][-1] + TickTime)

        else:
            self.WaveData[Sheet]['I2C_SCL'].append(0.0)
            self.WaveData[Sheet]['I2C_SCL'].append(0.0 if CLKSLEEP else AMP)
            self.WaveData[Sheet]['I2C_SCL'].append(0.0 if CLKSLEEP else AMP)
            self.WaveData[Sheet]['I2C_SCL'].append(0.0)

            for _ in range(4):self.WaveData[Sheet]['I2C_DataName'].append(Name)

            if str(Bit) == '1':
                for _ in range(4):self.WaveData[Sheet]['I2C_SDA'].append(AMP)
            elif str(Bit) == '0':
                for _ in range(4):self.WaveData[Sheet]['I2C_SDA'].append(0.0)

            for _ in range(4): self.WaveData[Sheet]['I2C_Time'].append(self.WaveData[Sheet]['I2C_Time'][-1]+TickTime)

    def I2C_Waveform(self, SheetName="", SequenceNumber=1, SequenceData=""):
        DataRate = self.Parameter[SheetName]['I2C Data Rate [kHz]']
        TickTime_4 = 1/(4 * DataRate * 1000)
        Voltage = float(self.Parameter[SheetName]['VIO [V]'])

        self.WaveData[SheetName]['I2C_Time'].append(self.WaveData[SheetName]['LastTime'])
        self.WaveData[SheetName]['I2C_SCL'].append(Voltage)
        self.WaveData[SheetName]['I2C_SDA'].append(Voltage)
        self.WaveData[SheetName]['I2C_DataName'].append("")

        self.I2C_Add_X(Sheet= SheetName, TickTime=TickTime_4, AMP=Voltage, Name='Sq#' + str(SequenceNumber) + ":", Init=True)

        ###Making Address Bit Stream
        scale = 16  ## equals to hexadecimal
        ADDR = str(SequenceData['I2C Add']).replace(" ", "")
        if ADDR[:2] == '0b':
            ADDR = hex(int(ADDR[2:], 2))

        num_of_bits = 7
        # Add_bin = bin(int(str(SequenceData['I2C Add']), scale))[2:].zfill(num_of_bits)
        Add_bin = bin(int(str(ADDR), scale))[2:].zfill(num_of_bits)


        # scale = 16  ## equals to hexadecimal
        # num_of_bits = 7
        # Add_bin = bin(int(str(SequenceData['I2C Add']), scale))[2:].zfill(num_of_bits)

        self.I2C_Add_X(Sheet= SheetName, TickTime=TickTime_4, Bit=0, AMP=Voltage, Name='Sq#' + str(SequenceNumber) + ":", CLKSLEEP=True)

        for n, bit in enumerate(Add_bin):
            dataname = 'Sq#'+str(SequenceNumber)+":" + 'ADDR['+str(6-n)+']'
            self.I2C_Add_X(Sheet= SheetName, TickTime=TickTime_4, Bit=bit, AMP=Voltage, Name=dataname)

        WR_BIT = 0 if "Write" in SequenceData['Direction'] else 1
        self.I2C_Add_X(Sheet= SheetName, TickTime=TickTime_4, Bit=WR_BIT, AMP=Voltage, Name='Sq#'+str(SequenceNumber)+":" + "W/R")
        ACK=0
        self.I2C_Add_X(Sheet= SheetName, TickTime=TickTime_4, Bit=ACK, AMP=Voltage, Name='Sq#'+str(SequenceNumber)+":" + "ACK")

        self.I2C_Add_X(Sheet= SheetName, TickTime=TickTime_4, Bit=1, AMP=Voltage, Name='Sq#'+str(SequenceNumber)+":",CLKSLEEP=True)
        self.I2C_Add_X(Sheet= SheetName, TickTime=TickTime_4, Bit=0, AMP=Voltage, Name='Sq#'+str(SequenceNumber)+":",CLKSLEEP=True)

        ### Makin Data bit Stream
        scale = 16  ## equals to hexadecimal
        DATA = str(SequenceData['Sending Data']).replace(" ", "")
        if DATA[:2] == '0b':
            DATA = hex(int(DATA[2:], 2))

        num_of_bits = 8
        # Add_bin = bin(int(str(SequenceData['I2C Add']), scale))[2:].zfill(num_of_bits)

        unm_of_data_bits = len(DATA) * 4
        Data_bin = bin(int(str(DATA), scale))[2:].zfill(unm_of_data_bits)

        # unm_of_data_bits = len(SequenceData['Sending Data']) * 4
        # Data_bin = bin(int(str(SequenceData['Sending Data']), scale))[2:].zfill(unm_of_data_bits)

        Bit_Counter = 7
        for n, bit in enumerate(Data_bin):
            dataname = 'Sq#'+str(SequenceNumber)+":" + 'DATA['+str(Bit_Counter)+']'
            self.I2C_Add_X(Sheet= SheetName, TickTime=TickTime_4, Bit=bit, AMP=Voltage, Name=dataname)
            Bit_Counter -= 1
            if Bit_Counter < 0:
                Bit_Counter = 7
                self.I2C_Add_X(Sheet= SheetName, TickTime=TickTime_4, Bit=ACK, AMP=Voltage, Name='Sq#' + str(SequenceNumber) + ":" + "ACK")

        STOP = 1
        self.I2C_Add_X(Sheet= SheetName, TickTime=TickTime_4, Bit=STOP, AMP=Voltage, Name='Sq#' + str(SequenceNumber) + ":" + "STOP", CLKSLEEP=True)
        self.I2C_Add_X(Sheet= SheetName, TickTime=TickTime_4, AMP=Voltage, Name='Sq#' + str(SequenceNumber) + ":", Init=True)
        print("")

        # self.WaveData['I2C_Time'] = ['{:.10f}'.format(n) for n in self.WaveData['I2C_Time']]
        return self.WaveData[SheetName]['I2C_Time'][-1]

    def SPI_Waveform(self, SheetName="", SequenceNumber=1, SequenceData=""):
        DataRate = self.Parameter[SheetName]['SPI Data Rate [kHz]']
        TickTime_2 = 1/(2 * DataRate * 1000)
        Voltage = float(self.Parameter[SheetName]['VIO [V]'])

        CPHA = False if "sample/setup" in self.Parameter[SheetName]['SPI Phase'] else True
        CPOL = False if "rising/falling" in self.Parameter[SheetName]['SPI Polarity'] else True
        if CPHA and CPOL:
            SPI_MODE = 3
        elif not CPHA and CPOL:
            SPI_MODE = 2
        elif CPHA and not CPOL:
            SPI_MODE = 1
        elif not CPHA and not CPOL:
            SPI_MODE = 0

        BITORDER = True if 'msb' in self.Parameter[SheetName]['SPI Bit Order'] else False
        CS_POL = True if 'active_low' in self.Parameter[SheetName]['SPI CS Polarity'] else False

        self.WaveData[SheetName]['SPI_Time'].append(self.WaveData[SheetName]['LastTime'])
        self.WaveData[SheetName]['SPI_MOSI'].append(Voltage)
        self.WaveData[SheetName]['SPI_DataName'].append("")

        if SPI_MODE == 0 or SPI_MODE == 1:
            self.WaveData[SheetName]['SPI_SCLK'].append(0)
            # self.WaveData[SheetName]['SPI_SCLK'].append(0)
        elif SPI_MODE == 2 or SPI_MODE == 3:
            self.WaveData[SheetName]['SPI_SCLK'].append(Voltage)
            # self.WaveData[SheetName]['SPI_SCLK'].append(Voltage)

        ### Makin Data bit Stream
        scale = 16  ## equals to hexadecimal
        DATA = str(SequenceData['Sending Data']).replace(" ", "")
        if DATA[:2] == '0b':
            DATA = hex(int(DATA[2:], 2))

        num_of_bits = 8
        # Add_bin = bin(int(str(SequenceData['I2C Add']), scale))[2:].zfill(num_of_bits)

        unm_of_data_bits = len(DATA) * 4
        Data_bin = bin(int(str(DATA), scale))[2:].zfill(unm_of_data_bits)

        # unm_of_data_bits = len(SequenceData['Sending Data']) * 4
        # Data_bin = bin(int(str(SequenceData['Sending Data']), scale))[2:].zfill(unm_of_data_bits)

        ### Initial
        self.SPI_Add_X(Sheet= SheetName, TickTime=TickTime_2, AMP=Voltage, Name='Sq#' + str(SequenceNumber) + ":", CLKSLEEP=True)

        Bit_Counter = 7
        if not BITORDER:
            for n in reversed(range(len(Data_bin))):
                bit = Data_bin[n]
                dataname = 'Sq#' + str(SequenceNumber) + ":" + 'DATA[' + str(Bit_Counter) + ']'
                self.SPI_Add_X(Sheet= SheetName, TickTime=TickTime_2, Bit=bit, AMP=Voltage, Name=dataname)
                Bit_Counter -= 1
                if Bit_Counter < 0: Bit_Counter = 7
        else:
            for n in range(len(Data_bin)):
                bit = Data_bin[n]
                dataname = 'Sq#'+str(SequenceNumber)+":" + 'DATA['+str(Bit_Counter)+']'
                self.SPI_Add_X(Sheet= SheetName, TickTime=TickTime_2, Bit=bit, AMP=Voltage, Name=dataname)
                Bit_Counter -= 1
                if Bit_Counter < 0: Bit_Counter = 7

        ### Closing
        self.SPI_Add_X(Sheet= SheetName, TickTime=TickTime_2, AMP=Voltage, Name='Sq#' + str(SequenceNumber) + ":", CLKSLEEP=True)
        self.WaveData[SheetName]['SPI_Time'].append(self.WaveData[SheetName]['SPI_Time'][-1] + TickTime_2)
        self.WaveData[SheetName]['SPI_MOSI'].append(Voltage)
        self.WaveData[SheetName]['SPI_DataName'].append("")
        self.WaveData[SheetName]['SPI_SCLK'].append(self.WaveData[SheetName]['SPI_SCLK'][-1])

        return self.WaveData[SheetName]['SPI_Time'][-1]

    def WaveFormReSamling(self, Sheet):
        SamplingTick = 1/SAMPLING_CLK

        Master_TimeLine = np.linspace(start=0.0, stop=self.WaveData[Sheet]['LastTime'], num=int(self.WaveData[Sheet]['LastTime']//SamplingTick))
        self.MasterWaveData[Sheet] = dict(
            I2C_SCL=[],
            I2C_SDA=[],
            I2C_DataName=[],
            SPI_SCLK=[],
            SPI_MOSI=[],
            SPI_DataName=[],
            Time = Master_TimeLine,
        )

        ### I2C Part
        if self.WaveData[Sheet]["I2C_Time"] != []:
            Data_ticknumber = 1
            for m_ticknumber in range(len(Master_TimeLine)):
                m_time = Master_TimeLine[m_ticknumber]

                try:
                    Data_time = self.WaveData[Sheet]["I2C_Time"][Data_ticknumber]
                except:
                    pass

                if m_time <= Data_time:
                    self.MasterWaveData[Sheet]["I2C_SCL"].append(self.WaveData[Sheet]["I2C_SCL"][Data_ticknumber-1])
                    self.MasterWaveData[Sheet]["I2C_SDA"].append(self.WaveData[Sheet]["I2C_SDA"][Data_ticknumber-1])
                    self.MasterWaveData[Sheet]["I2C_DataName"].append(self.WaveData[Sheet]["I2C_DataName"][Data_ticknumber-1])
                else:
                    try:
                        self.MasterWaveData[Sheet]["I2C_SCL"].append(self.WaveData[Sheet]["I2C_SCL"][Data_ticknumber])
                        self.MasterWaveData[Sheet]["I2C_SDA"].append(self.WaveData[Sheet]["I2C_SDA"][Data_ticknumber])
                        self.MasterWaveData[Sheet]["I2C_DataName"].append(self.WaveData[Sheet]["I2C_DataName"][Data_ticknumber])
                    except:
                        self.MasterWaveData[Sheet]["I2C_SCL"].append(self.WaveData[Sheet]["I2C_SCL"][-1])
                        self.MasterWaveData[Sheet]["I2C_SDA"].append(self.WaveData[Sheet]["I2C_SDA"][-1])
                        self.MasterWaveData[Sheet]["I2C_DataName"].append(self.WaveData[Sheet]["I2C_DataName"][-1])
                    Data_ticknumber += 1

        ### SPI Part
        if self.WaveData[Sheet]["SPI_Time"] != []:
            Data_ticknumber = 1
            for m_ticknumber in range(len(Master_TimeLine)):
                m_time = Master_TimeLine[m_ticknumber]

                try:
                    Data_time = self.WaveData[Sheet]["SPI_Time"][Data_ticknumber]
                except:
                    pass

                if m_time <= Data_time:
                    try:
                        self.MasterWaveData[Sheet]["SPI_SCLK"].append(self.WaveData[Sheet]["SPI_SCLK"][Data_ticknumber - 1])
                    except:
                        print("")

                    self.MasterWaveData[Sheet]["SPI_MOSI"].append(self.WaveData[Sheet]["SPI_MOSI"][Data_ticknumber - 1])
                    self.MasterWaveData[Sheet]["SPI_DataName"].append(self.WaveData[Sheet]["SPI_DataName"][Data_ticknumber - 1])
                else:
                    try:
                        self.MasterWaveData[Sheet]["SPI_SCLK"].append(self.WaveData[Sheet]["SPI_SCLK"][Data_ticknumber])
                        self.MasterWaveData[Sheet]["SPI_MOSI"].append(self.WaveData[Sheet]["SPI_MOSI"][Data_ticknumber])
                        self.MasterWaveData[Sheet]["SPI_DataName"].append(self.WaveData[Sheet]["SPI_DataName"][Data_ticknumber])
                    except:
                        self.MasterWaveData[Sheet]["SPI_SCLK"].append(self.WaveData[Sheet]["SPI_SCLK"][-1])
                        self.MasterWaveData[Sheet]["SPI_MOSI"].append(self.WaveData[Sheet]["SPI_MOSI"][-1])
                        self.MasterWaveData[Sheet]["SPI_DataName"].append(self.WaveData[Sheet]["SPI_DataName"][-1])
                    Data_ticknumber += 1

        print("")

    def WaveData_Genarater(self, Sheet):
        # self.WaveData = {}

        self.WaveData[Sheet] = dict(
            I2C_SCL= [],
            I2C_SDA= [],
            I2C_Time= [],
            I2C_DataName= [],
            SPI_SCLK=[],
            SPI_MOSI=[],
            SPI_Time=[],
            SPI_DataName= [],
            LastTime = 0.0,
        )

        for Sequence in self.SequenceData[Sheet]:
            print(f"Making Seq#{Sequence} Wavefrom Data")
            TextWriter(f"Making Seq#{Sequence} Wavefrom Data")

            if self.SequenceData[Sheet][Sequence]['Mode'] == "I2C":
                self.WaveData[Sheet]['LastTime'] = self.I2C_Waveform(SheetName=Sheet, SequenceNumber=Sequence, SequenceData=self.SequenceData[Sheet][Sequence])
            elif self.SequenceData[Sheet][Sequence]['Mode'] == "SPI":
                self.WaveData[Sheet]['LastTime'] = self.SPI_Waveform(SheetName=Sheet, SequenceNumber=Sequence, SequenceData=self.SequenceData[Sheet][Sequence])

        print(f"Data Re-Sampling for Sheet: {Sheet}")
        TextWriter(f"Data Re-Sampling for Sheet: {Sheet}")

        self.WaveFormReSamling(Sheet=Sheet)

    def SliderSetting(self, Unit='s', RangeList=range(10)):
        return dict(
            steps=[dict(
                method='animate',
                args=[[f'{k}'],  # This should match with Frame name
                      dict(mode='immediate',
                           frame=dict(duration=500, redraw=False),  # Reaction Time
                           transition=dict(duration=0),
                           )
                      ],
                label=f'{k}{Unit}',

            ) for k in RangeList],
            transition=dict(duration=0, ),  # Moving speed
            x=0,  # slider starting position
            y=0,
            currentvalue=dict(font=dict(size=12),
                              prefix='Time: ',
                              visible=True,
                              xanchor='right',
                              ),
            len=1.0,  # slider length)
        )

    def Add_Desimal_Unit(self, Data):
        Digits = 6
        list = []
        for n in Data:
            n = float(n)
            if n >= pow(10, -15) and n < (pow(10, -12)):
                list.append(str(round(n / pow(10, -15), Digits)) + 'f')

            elif n >= pow(10, -12) and n < (pow(10, -9)):
                list.append(str(round(n / pow(10, -12), Digits)) + 'p')

            elif n >= pow(10, -9) and n < (pow(10, -6)):
                list.append(str(round(n / pow(10, -9), Digits)) + 'n')

            elif n >= pow(10, -6) and n < (pow(10, -3)):
                list.append(str(round(n / pow(10, -6), Digits)) + "\u03BC")

            elif n >= pow(10, -3) and n < (pow(10, 0)):
                list.append(str(round(n / pow(10, -3), Digits)) + 'm')

            elif n >= pow(10, 0) and n < (pow(10, 3)) or n == 0:
                list.append(str(round(n / pow(10, 0), Digits)) + '')

            elif n >= pow(10, 3) and n < (pow(10, 6)):
                list.append(str(round(n / pow(10, 3), Digits)) + 'k')

            elif n >= pow(10, 6) and n < (pow(10, 9)):
                list.append(str(round(n / pow(10, 6), Digits)) + 'M')

            elif n >= pow(10, 9) and n < (pow(10, 12)):
                list.append(str(round(n / pow(10, 9), Digits)) + 'G')

            elif n >= pow(10, 12) and n < (pow(10, 15)):
                list.append(str(round(n / pow(10, 12), Digits)) + 'T')
        return list


    def Excel_File_Loader(self, FileName=""):
        Raw_PD = pd.read_excel(FileName, index_col=None, sheet_name=None)
        self.SheetNames = Raw_PD.keys()

        #### Parameter Loading ####
        self.Parameter = {}
        Dict_temp = {}
        NameColumn = 1
        ParamColumn = 2

        for Sheet in self.SheetNames:
            if Sheet == 'List':
                break
            for RawNumber, Data in enumerate(Raw_PD[Sheet].values):
                if Data[0] == 'Sequence':
                    RawNumber_Parameter_End = RawNumber
                    RawNumber_Sequence_Start = RawNumber + 4

        for Sheet in self.SheetNames:
            if Sheet == 'List':
                break
            for ParamNumber in range(RawNumber_Parameter_End):
                Dict_temp[Raw_PD[Sheet].values[ParamNumber][NameColumn]] = Raw_PD[Sheet].values[ParamNumber][ParamColumn]

            self.Parameter[Sheet] = Dict_temp
            Dict_temp = {}


        #### Sequence Loading ####
        self.SequenceData = {}
        temp_dict_seq = {}
        temp_dict_persheet = {}
        for Sheet in self.SheetNames:
            if Sheet == 'List':
                break
            for ParamNumber in range(RawNumber_Sequence_Start,len(Raw_PD[Sheet].values)):
                if Raw_PD[Sheet].values[ParamNumber][SequenceColumn['Mode']] != 'SPI' and Raw_PD[Sheet].values[ParamNumber][SequenceColumn['Mode']] != 'I2C' and Raw_PD[Sheet].values[ParamNumber][SequenceColumn['Mode']] != 'GPIO':
                    break
                for key in SequenceColumn.keys():
                    temp_dict_seq[key] = Raw_PD[Sheet].values[ParamNumber][SequenceColumn[key]]
                temp_dict_persheet[temp_dict_seq['Sequence Number']] = temp_dict_seq
                temp_dict_seq = {}

            self.SequenceData[Sheet] = temp_dict_persheet
            temp_dict_persheet = {}

        print("")

    def XML_Data_Config(self, XML_Data, SheetName = "Sheet1", ModeInput = "GPIO"):
        # XML_Data = ['<adapter>',]

        ## Configure
        if ModeInput == "I2C":
            I2C = 1
            SPI = 0
            GPIO = 1
        elif ModeInput == "SPI":
            I2C = 0
            SPI = 1
            GPIO = 1
        elif ModeInput == "GPIO":
            I2C = 0
            SPI = 0
            GPIO =1

        VTGT = 0 if "OFF" in str(self.Parameter[SheetName]['VTGT [V]']) else str(self.Parameter[SheetName]['VTGT [V]'])
        VIO = 0 if "OFF" in str(self.Parameter[SheetName]['VIO [V]']) else str(self.Parameter[SheetName]['VIO [V]'])
        PULLUP = 1 if "ON" in self.Parameter[SheetName]['I2C Pull-Up'] else 0

        XML_Data.append(
            fr'  <configure i2c="{I2C}" spi="{SPI}" gpio="{GPIO}" tpower="{VTGT}" levelshift="{VIO}" pullups="{PULLUP}"/>'
        )

        #SPI Config
        if SPI == 1:
            SPI_POLARITY = self.Parameter[SheetName]['SPI Polarity']
            SPI_PHASE = self.Parameter[SheetName]['SPI Phase']
            SPI_BITORDER = self.Parameter[SheetName]['SPI Bit Order']
            SPI_CS = self.Parameter[SheetName]['SPI CS Polarity']
            XML_Data.append(
                fr'  <spi_config polarity="{SPI_POLARITY}" phase="{SPI_PHASE}" bitorder="{SPI_BITORDER}" ss="{SPI_CS}"/>'
            )

        #GPIO Config
        # if GPIO == 1:
        #     # GPIO_DIRECTION = 0 if "Input" in self.Parameter[sheetName]['GPIO Direction'] else 1
        #     GPIO_PULLUP = 1 if "ON" in self.Parameter[SheetName]['GPIO Internal Pull Up'] else 0
        #     XML_Data.append(
        #         fr'  <gpio_config pullups="{GPIO_PULLUP}"/>'
        #     )

        ## DataRate
        if SPI == 1:
            SPIDATARATE = self.Parameter[SheetName]['SPI Data Rate [kHz]']
            XML_Data.append(
                fr'  <spi_bitrate khz="{SPIDATARATE}"/>'
            )

        if I2C == 1:
            I2CDATARATE = self.Parameter[SheetName]['I2C Data Rate [kHz]']
            XML_Data.append(
                fr'  <i2c_bitrate khz="{I2CDATARATE}"/>'
            )
        # XML_Data.append(
        #     ""
        # )

        return XML_Data

    def XML_Data_Sequence(self, XML_Data, SheetName = "Sheet1"):
        for Sequence_Number in self.SequenceData[SheetName]:
            DIRECTION = self.SequenceData[SheetName][Sequence_Number]['Direction']

            ## Preparing Sleep Time
            SLEEPTIME = self.Parameter[SheetName]['Sleep Duration [ms]']

            if DIRECTION == 'Write':
                XML_Data = self.XML_Data_Config(XML_Data=XML_Data,SheetName=SheetName, ModeInput=self.SequenceData[SheetName][Sequence_Number]['Mode'])

                ### GPIO Mode
                if self.SequenceData[SheetName][Sequence_Number]['Mode'] == "GPIO":
                    # GPIO Direction
                    DIRECTION_BIT = ""
                    for GPIO_Number in reversed(range(16)):
                        Status = '0' if 'nan' in str(self.SequenceData[SheetName][Sequence_Number]['GPIO_' + str(GPIO_Number)]) \
                                     else '1'
                        DIRECTION_BIT+=Status

                    GPIO_DIRECTION = hex(int(DIRECTION_BIT, 2))
                    XML_Data.append(
                        fr'  <gpio_config direction="{GPIO_DIRECTION}"/>'
                    )

                    # GPIO Output
                    OUTPUT_BIT = ""
                    for bit in reversed(range(16)):
                        Status = '1' if 'High' in str(self.SequenceData[SheetName][Sequence_Number]['GPIO_' + str(bit)]) else '0'
                        OUTPUT_BIT+=Status
                    GPIO_OUTPUT = hex(int(OUTPUT_BIT, 2))
                    XML_Data.append(
                        fr'  <gpio_get/>"/>'
                    )
                    XML_Data.append(
                        fr'  <gpio_set value="{GPIO_OUTPUT}"/>'
                    )

                ### SPI Data Sending
                if self.SequenceData[SheetName][Sequence_Number]['Mode'] == "SPI":
                    try:
                        SS = int(self.SequenceData[SheetName][Sequence_Number]['SPI CS'][-1])
                    except:
                        SS = 0
                        text = "Error: At Sequence# " + str(Sequence_Number) + " SPI Chip Select is missing"
                        print(text)
                        TextWriter(text)

                    DATA = str(self.SequenceData[SheetName][Sequence_Number]['Sending Data']).replace(" ", "")
                    if DATA == "nan":
                        text = "Error: At Sequence# " + str(Sequence_Number) + " SPI Data is missing"
                        print(text)
                        TextWriter(text)
                        DATA = "00"

                    # GPIO Direction
                    DIRECTION_BIT = ""
                    for GPIO_Number in reversed(range(16)):
                        if GPIO_MAP[SS] == GPIO_Number:
                            Status = '0'
                        else:
                            Status = '0' if 'nan' in str(self.SequenceData[SheetName][Sequence_Number]['GPIO_' + str(GPIO_Number)]) \
                                     else '1'
                        # Status = '1' if (str(GPIO_MAP[SS]) != GPIO_Number) else '0'
                        DIRECTION_BIT+=Status

                    GPIO_DIRECTION = hex(int(DIRECTION_BIT, 2))
                    XML_Data.append(
                        fr'  <gpio_config direction="{GPIO_DIRECTION}"/>'
                    )

                    # GPIO Output
                    OUTPUT_BIT = ""
                    for bit in reversed(range(16)):
                        Status = '1' if 'High' in str(self.SequenceData[SheetName][Sequence_Number]['GPIO_' + str(bit)]) else '0'
                        OUTPUT_BIT+=Status
                    GPIO_OUTPUT = hex(int(OUTPUT_BIT, 2))
                    XML_Data.append(
                        fr'  <gpio_get/>"/>'
                    )
                    XML_Data.append(
                        fr'  <gpio_set value="{GPIO_OUTPUT}"/>'
                    )


                    # SPI Data
                    if DATA[:2] == '0b':
                        DATA = hex(int(DATA[2:],2))
                        COUNT = (len(DATA) - 2) // 2
                    else:
                        COUNT = (len(DATA)) // 2
                    RADIX = 16

                    if len(DATA) > 2:
                        DATA = ' '.join(DATA[i:i + 2] for i in range(0, len(DATA), 2))

                    XML_Data.append(
                        fr'  <spi_write ss="{SS}" count="{COUNT}" radix="{RADIX}"> {DATA} </spi_write>'
                    )
                    if SLEEPTIME != 0:
                        XML_Data.append(
                            fr'  <sleep ms="{SLEEPTIME}"/>'
                        )

                ### I2C Data Sending
                if self.SequenceData[SheetName][Sequence_Number]['Mode'] == "I2C":

                    # GPIO Direction
                    DIRECTION_BIT = ""
                    for GPIO_Number in reversed(range(16)):
                        if GPIO_Number < 2:
                            Status = '0'
                        else:
                            Status = '0' if 'nan' in str(self.SequenceData[SheetName][Sequence_Number]['GPIO_' + str(GPIO_Number)]) \
                                     else '1'
                        # Status = '1' if (str(GPIO_MAP[SS]) != GPIO_Number) else '0'
                        DIRECTION_BIT+=Status

                    GPIO_DIRECTION = hex(int(DIRECTION_BIT, 2))
                    XML_Data.append(
                        fr'  <gpio_config direction="{GPIO_DIRECTION}"/>'
                    )

                    # GPIO Output
                    OUTPUT_BIT = ""
                    for bit in reversed(range(16)):
                        Status = '1' if 'High' in str(self.SequenceData[SheetName][Sequence_Number]['GPIO_' + str(bit)]) else '0'
                        OUTPUT_BIT+=Status
                    GPIO_OUTPUT = hex(int(OUTPUT_BIT, 2))
                    XML_Data.append(
                        fr'  <gpio_get/>'
                    )
                    XML_Data.append(
                        fr'  <gpio_set value="{GPIO_OUTPUT}"/>'
                    )


                    # I2C Data
                    I2C_ADD = str(self.SequenceData[SheetName][Sequence_Number]['I2C Add'])
                    if I2C_ADD[:2] == '0b':
                        I2C_ADD = hex(int(I2C_ADD[2:], 2))
                    else:
                        I2C_ADD = '0x'+I2C_ADD


                    if I2C_ADD == "nan":
                        text = "Error: At Sequence# " + str(Sequence_Number) + " I2C Address is missing"
                        print(text)
                        TextWriter(text)
                        I2C_ADD = "00"

                    DATA = str(self.SequenceData[SheetName][Sequence_Number]['Sending Data']).replace(" ", "")

                    if DATA == "nan":
                        text = "Error: At Sequence# " + str(Sequence_Number) + " I2C Data is missing"
                        print(text)
                        TextWriter(text)
                        DATA = "00"


                    if DATA[:2] == '0b':
                        DATA = hex(int(DATA[2:],2))
                        COUNT = (len(DATA) - 2) // 2
                    else:
                        COUNT = (len(DATA)) // 2
                    RADIX = 16

                    if len(DATA) > 2:
                        DATA = ' '.join(DATA[i:i + 2] for i in range(0, len(DATA), 2))

                    XML_Data.append(
                        fr'  <i2c_write addr="{I2C_ADD}" count="{COUNT}" radix="{RADIX}"> {DATA} </i2c_write>'
                    )
                    if SLEEPTIME != 0:
                        XML_Data.append(
                            fr'  <sleep ms="{SLEEPTIME}"/>'
                        )

            if DIRECTION == 'Read':
                XML_Data = self.XML_Data_Config(XML_Data=XML_Data,SheetName=SheetName, ModeInput=self.SequenceData[SheetName][Sequence_Number]['Mode'])

                # GPIO Direction
                XML_Data.append(
                    fr'  <gpio_config direction="0x00"/>'
                )

                # GPIO Read
                XML_Data.append(
                    fr'  <gpio_get/>'
                )
                ### I2C Data Reading
                if self.SequenceData[SheetName][Sequence_Number]['Mode'] == "I2C":
                    # I2C Data
                    I2C_ADD = str(self.SequenceData[SheetName][Sequence_Number]['I2C Add'])
                    if I2C_ADD[:2] == '0b':
                        I2C_ADD = hex(int(I2C_ADD[2:], 2))
                    else:
                        I2C_ADD = '0x'+I2C_ADD

                    if I2C_ADD == "nan":
                        text = "Error: At Sequence# " + str(Sequence_Number) + " I2C Address is missing"
                        print(text)
                        TextWriter(text)
                        I2C_ADD = "00"

                    DATA = str(self.SequenceData[SheetName][Sequence_Number]['Sending Data']).replace(" ", "")
                    if DATA[:2] == '0b':
                        DATA = hex(int(DATA[2:],2))
                        COUNT = (len(DATA) - 2) // 2
                    else:
                        COUNT = (len(DATA)) // 2

                    XML_Data.append(
                        fr'  <i2c_read addr="{I2C_ADD}" count="{COUNT}"/>'
                    )
                    XML_Data.append(
                        fr'  <sleep ms="{SLEEPTIME}"/>'
                    )

        return XML_Data
    def XML_File_Writer(self, FileLocation, SheetName):
        # WritingData = self.XML_Data_Config(SheetName)
        WritingData = ['<adapter>']
        WritingData = self.GPIOInitial(WritingData, SheetName=SheetName)
        WritingData = self.XML_Data_Sequence(WritingData, SheetName=SheetName)
        WritingData.append('</adapter>')

        with open(FileLocation+'\\'+SheetName +'.XML', "w") as f:
            for row in WritingData:
                f.write(str(row) + "\n")

        print("")

    def GPIOInitial(self,XML_Data, SheetName = "Sheet1"):
        GPIO_PULLUP = 1 if "ON" in self.Parameter[SheetName]['GPIO Internal Pull Up'] else 0
        XML_Data.append(
            fr'  <gpio_config pullups="{GPIO_PULLUP}"/>'
        )
        return XML_Data

    def SequenceRun(self):
        path_desktop = os.environ['USERPROFILE'] + str('\\Desktop\\')
        self.PlotlyGraph = {}
        self.WaveData = {}
        self.MasterWaveData = {}
        for Sheet in self.SheetNames:
            if Sheet == 'List':
                break
            print(fr"Reading {Sheet} sheet")
            TextWriter(fr"Reading {Sheet} sheet")

            self.GUI_Control(Sheet= Sheet)

            if not os.path.exists(path_desktop + r'Promira_Batch_files'):
                os.mkdir(path_desktop + r'Promira_Batch_files')

            self.XML_File_Writer(FileLocation=path_desktop + r'Promira_Batch_files',
                                    SheetName=Sheet)
            print(fr"XML File, {Sheet}.XML was created")
            TextWriter(fr"XML File, {Sheet}.XML was created")

            print(fr"")
            TextWriter(fr"")

        print(fr"Process Completed")
        TextWriter(fr"Process Completed")

if __name__ == "__main__":
    Path = r"C:\Users\IsaoYoneda\OneDrive - Photonic Inc\Python\AnalysisTool\DataAnalyzer\assets\Promira_Template.xlsx"
    if os.path.exists(Path) == True:
        Promira = Promira_Serial_Control(FilePath=Path)
    else:
        Path = r"C:\Users\pekep\OneDrive\Project\Python\AnalysisTool\DataAnalyzer\assets\Promira_Template.xlsx"
        if os.path.exists(Path) == True:
            Promira = Promira_Serial_Control(FilePath=Path)
            # Promira.GUI_Control()
