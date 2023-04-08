# ===================================================================================
# Program Name: Spectrum Analyzer
# Function: Class Code of Spectrum Analyzer with Plotly
# @author: Isao Yoneda
# ====================================================================================

import pandas as pd
import numpy as np
import plotly.graph_objs as go
import time
#import scikit-rf
from scipy import fftpack
from scipy.fft import fft
from scipy.signal import blackman
from TextWriter import TextWriter


ColurTable = {
    0 : "red",
    1 : "blue",
    2 : "green",
    3 : "orange",
    4 : "MediumPurple",
    5 : "gray",
    6 : "gold"
}

class SpectrumAnalyzer:
	def __init__(self, Path,HeaderRow=0,UnitRow=1):
		# Arguments  ------------------------------------
		self.Path = Path
		# Internal Parameters ---------------------------
		self.HeaderRow = HeaderRow
		self.UnitRow = UnitRow

		print("Class:SpectrumAnalyzer was called")
		TextWriter("Class:SpectrumAnalyzer was called")
		# Methods ------------------------------------
		self.CSV_Read()
		self.PlotlyEnable()
		self.AreaSplit()
		self.TimeDomainParameters(row=1, col=2)
		self.TimeDomainWaveForm(row=1, col=1)
		self.FreqDomainWaveForm(row=2, col=1)
		self.StyleUpdate()
		self.Fig_Plotly.show()

	def __call__(self):
		print("This is call faunction.")
		return self.Path

	def CSV_Read(self):
		starttime = time.time()

		try:
			HeaderCheck =pd.read_csv(self.Path,
									 header=None,
									 sep='\t\s',
   									 nrows=25,
									)
			if ',Start,Increment' in str(HeaderCheck.values[0]):
				HeaderNames = str(HeaderCheck.values[0]).split(',')
				StartColumn = HeaderNames.index('Start')
				IncrementColumn = HeaderNames.index('Increment')
				Start_Time = float(str(HeaderCheck.values[1]).split(',')[StartColumn])
				Increment_Time = float(str(HeaderCheck.values[1]).split(',')[IncrementColumn].split("'")[0])
				self.Data_Label = HeaderNames[:StartColumn]
				self.TraceNumbers = len(self.Data_Label)-1

				self.Table = pd.read_csv(self.Path,
										 header=self.HeaderRow+1,
										 sep='\t\s|,',
										 )
				self.Table = self.Table.dropna(axis='columns', how='all')  # ver.2.1 drop any NaN data
				self.Data_Unit = ['Second']
				self.Time_Data = []
				for Column in range(len(self.Table)):
					self.Time_Data.append(float(Start_Time+Increment_Time * Column))

				for ChannelUnit in (HeaderCheck.iloc[1][0]).split(",")[1:self.TraceNumbers+1]:
					self.Data_Unit.append(ChannelUnit)

				self.Data_Plot = self.Table


			elif 'MSO64' in HeaderCheck.values[0][0]:
				for n in range(len(HeaderCheck)):
					if 'Labels,' in HeaderCheck.iloc[n][0]:
						self.HeaderRow = n+1
						break

				### Trace Numbers Finder ###
				Labels = HeaderCheck.iloc[self.HeaderRow][0].split(',')
				NewLabel=[]
				for Key in Labels:
					if Key != '':
						NewLabel.append(Key)
				self.TraceNumbers = len(NewLabel)-1

				# self.HeaderRow = 15
				self.Table = pd.read_csv(self.Path,
										 header=self.HeaderRow,
										 sep='\t\s|,',
										 )
				self.Table = self.Table.dropna(axis='columns',how='all')  # ver.2.1 drop any NaN data
				self.Data_Label = np.array(self.Table.columns)[1:]
				self.Data_Label = np.insert(self.Data_Label, 0, 'Second')
				self.Data_Unit=['Second']

				for n in range(len(HeaderCheck)):
					if 'Vertical Units' in HeaderCheck.iloc[n][0]:
						UnitRow = n
						break

				for n in range(self.TraceNumbers):
					self.Data_Unit.append(HeaderCheck.iloc[UnitRow][0][15+n*18])

				#DataStartRow = max(self.HeaderRow, self.UnitRow) + 1

				self.Data_Plot = self.Table.iloc[1:, :]
				self.Time_Data = np.array(self.Data_Plot.iloc[:, 0])

			elif 'SDS5104X' in HeaderCheck.values[7][0]:
				for n in range(len(HeaderCheck)):
					if 'Second' in HeaderCheck.iloc[n][0]:
						self.HeaderRow = n + 1
						break
				### Trace Numbers Finder ###
				self.Data_Label = HeaderCheck.iloc[10][0].split(',')
				NewLabel = []
				for Key in self.Data_Label:
					if Key != '':
						NewLabel.append(Key)
				self.TraceNumbers = len(self.Data_Label)-1
				self.Table = pd.read_csv(self.Path,
										 header=self.HeaderRow,
										 sep='\t\s|,',
										 )
				self.Table = self.Table.dropna(axis='columns', how='all')  # ver.2.1 drop any NaN data
				self.Data_Unit = ['Second']

				for n in range(len(HeaderCheck)):
					if 'Vertical Units' in HeaderCheck.iloc[n][0]:
						UnitRow = n
						break
				for n in range(self.TraceNumbers):
					self.Data_Unit.append(HeaderCheck.iloc[UnitRow][0][19 + n * 7])

				self.Data_Plot = self.Table.iloc[:, :]
				self.Time_Data = np.array(self.Data_Plot.iloc[:, 0])

			else:
				data_reader = pd.read_csv(self.Path,
										  chunksize=500,
										  header=None,
										  engine='python')
				self.Table = pd.concat((r for r in data_reader), ignore_index=True)
				self.Data_Label = np.array(self.Table.iloc[self.HeaderRow, :])
				self.Data_Unit = np.array(self.Table.iloc[self.UnitRow, :])

				DataStartRow = max(self.HeaderRow, self.UnitRow) + 1

				#self.Table = self.Table.dropna(how='any')  # ver.2.1 drop any NaN data

				self.Data_Plot = self.Table.iloc[DataStartRow:, :]
				self.Table = self.Table.dropna(how='any')  # ver.2.1 drop any NaN data
				self.TraceNumbers = len(self.Data_Label) - 1
				self.Time_Data = np.array(self.Data_Plot.iloc[:, 0])

		except:
			data_reader = pd.read_csv(self.Path,
									  chunksize=500,
									  header=None,
									  engine='python')
			self.Table = pd.concat((r for r in data_reader), ignore_index=True)
			self.Data_Label = np.array(self.Table.iloc[self.HeaderRow, :])
			self.Data_Unit = np.array(self.Table.iloc[self.UnitRow, :])

			DataStartRow = max(self.HeaderRow, self.UnitRow) + 1

			self.Data_Plot = self.Table.iloc[DataStartRow:, :]

			# DataStartRow = max(self.HeaderRow, self.UnitRow) + 1
			#
			self.Table =self.Table.dropna(how='any')	#ver.2.1 drop any NaN data
			#
			#
			# self.Data_Plot = self.Table.iloc[DataStartRow:, :]
			self.TraceNumbers = len(self.Data_Label) - 1
			self.Time_Data = np.array(self.Data_Plot.iloc[:,0])
		elapstedtime = time.time() - starttime
		print("CSV Read Completed in {:.3}s".format(elapstedtime))
		TextWriter("CSV Read Completed in {:.3}s".format(elapstedtime))

	def PlotlyEnable(self):
		starttime = time.time()
		## To make enable for Run mode
		import plotly.io as pio
		pio.renderers.default = "browser"
		##############################
		elapstedtime = time.time() - starttime
		print("PlotlyEnable Completed in {:.3}s".format(elapstedtime))
		TextWriter("PlotlyEnable Completed in {:.3}s".format(elapstedtime))

	def AreaSplit(self):
		starttime = time.time()
		from plotly.subplots import make_subplots
		self.Fig_Plotly = make_subplots(
			rows=2,
			cols=2,
			specs= [
				[{"type": "scatter"},{"type": "table"}],
				[{"type": "scatter", 'colspan': 2}, None]],
			subplot_titles=(
				"Time Domain Scale",
				"Time Domain Parameters",
				"Frequency Domain Scale"
			)
		)
		elapstedtime = time.time() - starttime
		print("AreaSplit Completed in {:.3}s".format(elapstedtime))
		TextWriter("AreaSplit Completed in {:.3}s".format(elapstedtime))

	def TimeDomainParameters(self, row, col):
			starttime = time.time()
			from decimal import Decimal

			HeaderList = ['Trace#']
			UnitList = ['Unit']
			DataPointList = ['DataPoint']
			SamplingRate = ['SPLRate']
			Peak2Peak = ['Peak-Peak']
			Peak = ['Peak']
			Minimum = ['Minimum']
			RMS = ['RMS']
			Average = ['Average']
			Columnwidth = [80]

			for n in range(self.TraceNumbers):
				templist = np.array(self.Data_Plot.iloc[:, n + 1], dtype=np.float32)

				Columnwidth.append(50)
				try:
					HeaderList.append(self.Data_Label[n + 1])
				except:
					pass
				UnitList.append(self.Data_Unit[n + 1])
				DataPointList.append(len(templist))
				SamplingRate.append(
					"{:.4}".format(
						Decimal(
							len(templist) / (float(self.Time_Data[-1]) - float(self.Time_Data[0]))
						)
					)
				)
				Peak2Peak.append(
					"{:.4}".format(
						Decimal(
							float(max(templist)) - float(min(templist))
						)
					)
				)
				Peak.append(
					"{:.4}".format(
						Decimal(
							float(max(templist))
						)
					)
				)
				Minimum.append(
					"{:.4}".format(
						Decimal(
							float(min(templist))
						)
					)
				)
				# Array = templist
				Array = templist.astype(np.float)
				RMS.append(
					"{:.4}".format(
						Decimal(
							np.sqrt(np.mean(Array ** 2))
						)
					)
				)
				Average.append(
					"{:.4}".format(
						Decimal(
							np.average(Array)
						)
					)
				)

			# --------------------------
			ParamTable = []
			ParamTable.append(UnitList)
			ParamTable.append(DataPointList)
			ParamTable.append(SamplingRate)
			ParamTable.append(Peak2Peak)
			ParamTable.append(Peak)
			ParamTable.append(Minimum)
			ParamTable.append(RMS)
			ParamTable.append(Average)

			# Row <-> Column -----------
			ParamTable_np = np.array(ParamTable)
			ParamTable = ParamTable_np.T
			# --------------------------

			self.Fig_Plotly_TimeTable = go.Figure()
			self.Fig_Plotly_TimeTable.add_trace(
				go.Table(
					columnwidth=Columnwidth,
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
			self.Fig_Plotly_TimeTable.update_layout(
				dict(
					title=dict(
						text="Time Domain Parameters of " + '\\'.join(self.Path.split('\\')[-1:]),
						xanchor='auto',
					)
				)
			)

			# saving into Table
			self.Fig_Plotly.add_trace(
				go.Table(
					columnwidth=Columnwidth,
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
					),

				),
				row=row, col=col
			)
			# return self.Fig_Plotly
			elapstedtime = time.time() - starttime
			print("TimeDomainParameters Completed in {:.3}s".format(elapstedtime))
			TextWriter("TimeDomainParameters Completed in {:.3}s".format(elapstedtime))

	def TimeDomainWaveForm(self,row,col):
		starttime = time.time()
		# Data load -----------------

		for n in range(self.TraceNumbers):
			Y_Data = np.array(self.Data_Plot.iloc[:, n + 1])

			CustomData = []

			for k in range(len(self.Time_Data)):
				try:
					CheckValue = float(self.Time_Data[k])
					T = self.Add_Desimal_Unit(Data=abs(CheckValue))
					T_PN = +1 if CheckValue > 0 else -1

					if self.Data_Unit[n + 1] == 'Volt' or self.Data_Unit[n + 1] == 'V':
						CustomData.append(
							[
								T[0] * T_PN,  # Raw data of Time
								T[1]+'s',  # Unit data of Time
								float(Y_Data[k]),# Raw data of Voltage (Tuple V)
								'V',	# Unit data of Voltage (Tuple V)
								#float(self.Fig_Plotly_TimeTable.data[0].cells.values[n + 1][3]),  # Peak-to-Peak
								#float(self.Fig_Plotly_TimeTable.data[0].cells.values[n + 1][6]),  # RMS
							]
						)
					elif self.Data_Unit[n + 1] == 'Ampere' or self.Data_Unit[n + 1] == 'A':
						CustomData.append(
							[
								T[0] * T_PN,  # Raw data of Time
								T[1]+'s',  # Unit data of Time
								float(Y_Data[k]),# Raw data of Voltage (Tuple V)
								'A',	# Unit data of Voltage (Tuple V)
								#float(self.Fig_Plotly_TimeTable.data[0].cells.values[n + 1][3]),  # Peak-to-Peak
								#float(self.Fig_Plotly_TimeTable.data[0].cells.values[n + 1][6]),  # RMS
							]
						)

				except:
					pass

			Vpp = float(self.Fig_Plotly_TimeTable.data[0].cells.values[n + 1][3]),  # Peak-to-Peak
			Vrms = float(self.Fig_Plotly_TimeTable.data[0].cells.values[n + 1][6]),  # RMS

			self.Fig_Plotly.add_trace(
				go.Scatter(
					x=self.Time_Data,
					y=Y_Data,
					name="TimeDomain Trace#" + str(n+1) + "["+str(self.Data_Unit[n+1])[0]+"]",
					text=[
						f'Trace#: {n+1}<br>Time: {t_h:0.4f}{T_Unit} <br>Amplitude: {volt:0.4f}{V_Unit} <br>Peak-Peak: {Vpp[0]}{V_Unit}<br>RMS: {Vrms[0]}{V_Unit}'
						for [t_h, T_Unit, volt, V_Unit] in CustomData],
					hoverinfo='text',
					legendgroup = str(n+1),
					line_color = ColurTable[n],
				),
				row=row,col=col
			)

			elapstedtime = time.time() - starttime
			print("Preparing Data of Trace#{} Completed in {:.3}s".format(n+1, elapstedtime))
			TextWriter("Preparing Data of Trace#{} Completed in {:.3}s".format(n+1, elapstedtime))
			starttime = time.time()

		self.Fig_Plotly.update_yaxes(title_text="Amplitude [V]or[A]", row=row, col=col)
		self.Fig_Plotly.update_xaxes(title_text="Time [s]", row=row, col=col)

		self.Fig_Plotly_TimeWave = go.Figure()
		for n in range(self.TraceNumbers):
			Y_Data = np.array(self.Data_Plot.iloc[:, n + 1])
			self.Fig_Plotly_TimeWave.add_trace(
				go.Scatter(
					x=self.Time_Data,
					y=Y_Data,
					name="Trace#" + str(n + 1) + "[" + str(self.Data_Unit[n + 1])[0] + "]",
					#legendgroup=str(n + 1),
					line_color=ColurTable[n],
				),
			)
		self.Fig_Plotly_TimeWave.update_layout(
			dict(
				legend=dict(
					orientation="h",
					yanchor="top",
					y=1.2,
					xanchor="left",
					x=0.01
				)
			)
		)
		#self.Fig_Plotly_TimeWave.update_yaxes(type='log')
		self.Fig_Plotly_TimeWave.update_yaxes(title_text="Amplitude [V]or[A]",
											  type=None,
											  autorange=False,
											  )
		self.Fig_Plotly_TimeWave.update_xaxes(title_text="Time [s]",
											  type=None,
											  autorange=False,
											  )
		#return self.Fig_Plotly
		elapstedtime = time.time() - starttime
		print("TimeDomainWaveForm Completed in {:.3}s".format(elapstedtime))
		TextWriter("TimeDomainWaveForm Completed in {:.3}s".format(elapstedtime))

	def calc_fft(self, data, samplerate):
		spectrum = fftpack.fft(data)  # 信号のフーリエ変換
		amp = np.sqrt((spectrum.real ** 2) + (spectrum.imag ** 2))  # 振幅成分
		amp = amp / (len(data) / 2)  # 振幅成分の正規化（辻褄合わせ）
		phase = np.arctan2(spectrum.imag, spectrum.real)  # 位相を計算
		phase = np.degrees(phase)  # 位相をラジアンから度に変換
		freq = np.linspace(0, samplerate, len(data))  # 周波数軸を作成
		return spectrum, amp, phase, freq

	def FreqDomainWaveForm(self,row,col):
		starttime = time.time()
		# FFT Calculation ------------
		Datapoint = len(self.Time_Data)
		Space = abs(float(self.Time_Data[-1]) - float(self.Time_Data[0]))/len(self.Time_Data)
		Freq_Data = np.linspace(0.0, 1.0 / (2.0 * Space), Datapoint // 2)
		FFT_Window = blackman(Datapoint)

		SampleRate = 1 / Space


		for n in range(self.TraceNumbers):
			Y_Data=np.array(self.Data_Plot.iloc[:, n + 1],dtype=float)
			spectrum, amp, phase, freq = self.calc_fft(Y_Data, SampleRate)
			#ywf = fft(Y_Data * FFT_Window)#*Space

			Voltage= amp[1:Datapoint//2]
			CustomData = []

			for k in range(len(freq[1:Datapoint//2])):
				try:
					F = self.Add_Desimal_Unit(Data=Freq_Data[k+1])
					V = self.Add_Desimal_Unit(Data=Voltage[k]),
					if self.Data_Unit[n+1] == 'Volt' or self.Data_Unit[n+1] == 'V':
						CustomData.append(
							[	#Freq_Data[k+1],
								F[0],	#Raw data of Frequency
								F[1],	#Unit data of Frequency
								V[0][0],#Raw data of Voltage (Tuple V)
								V[0][1] +'V',#Unit data of Voltage (Tuple V)
								10 * np.log10(1000 * Voltage[k] ** 2 / (2 * 50)),
								10 * np.log10(1000 * Voltage[k] ** 2 / (50)),
							]
						)
					elif self.Data_Unit[n+1] == 'Ampere' or self.Data_Unit[n+1] == 'A':
						CustomData.append(
							[	#Freq_Data[k+1],
								F[0],	#Raw data of Frequency
								F[1],	#Unit data of Frequency
								V[0][0],#Raw data of Voltage (Tuple V)
								V[0][1] +'A',#Unit data of Voltage (Tuple V)
								10 * np.log10(1000 * Voltage[k] ** 2 * (2 * 50)),
								10 * np.log10(1000 * Voltage[k] ** 2 * (50)),
							]
						)
				except:
					pass


			self.Fig_Plotly.add_trace(
				go.Scatter(
					x=Freq_Data[1:Datapoint//2],
					y = (10*np.log10(1000*Voltage**2/(2*50))),
					text=[f'Trace#: {n+1}<br>Freq: {Freq:0.2f}{F_Unit}Hz <br>Amplitude: {V:0.4f}{V_Unit} <br>Amplitude: {dBm_50:0.2f}dBm(Measured with 50ohm)<br>Amplitude: {dBm_Megohm:0.2f}dBm(Measured with 1Mohm) ' for [Freq,F_Unit, V,V_Unit, dBm_50, dBm_Megohm] in CustomData],
					hoverinfo='text',
					name = "FreqDomain Trace#" + str(n+1),
					legendgroup=str(n + 1),
					line_color=ColurTable[n],
				),
				row=row,col=col
			)

		self.Fig_Plotly.update_yaxes(title_text="Amplitude [dBm]",
									 #range = [-140,0],
									 row=row,col=col)
		self.Fig_Plotly.update_xaxes(title_text="Frequency [Hz]",
									 rangeslider_visible=True,
									 row=row,col=col)

		self.Fig_Plotly_FreqDomain = go.Figure()
		for n in range(self.TraceNumbers):
			Y_Data=np.array(self.Data_Plot.iloc[:, n + 1],dtype='float64')
			ywf = fft(Y_Data * FFT_Window)*Space


			self.Fig_Plotly_FreqDomain.add_trace(
				go.Scatter(
					x=Freq_Data[1:Datapoint//2],
					y=20*np.log10(1e6*np.abs(ywf[1:Datapoint//2]))-107.2,
					name = "Trace#" + str(n+1),
					#legendgroup=str(n + 1),
					line_color=ColurTable[n],
				),
			)

		self.Fig_Plotly_FreqDomain.update_layout(
			legend=dict(
				orientation="h",
				yanchor="top",
				y=1.2,
				xanchor="left",
				x=0.01
			)
		)
		self.Fig_Plotly_FreqDomain.update_yaxes(title_text="Amplitude [dBm]")
										#rangeslider_visible=True)
		self.Fig_Plotly_FreqDomain.update_xaxes(title_text="Frequency [Hz]",
									 	rangeslider_visible=True,
									 	)
		elapstedtime = time.time() - starttime
		print("FreqDomainWaveForm Completed in {:.3}s".format(elapstedtime))
		TextWriter("FreqDomainWaveForm Completed in {:.3}s".format(elapstedtime))

	def StyleUpdate(self):
		self.Fig_Plotly.update_layout(
			title= "Waveform Check Result of " + str(self.Path[self.Path.rfind("\\")+1:])
		)

	def Add_Desimal_Unit(self,Data):
		Digits = 6
		n = Data
		#list = []
		if n >= pow(10,-15) and n < (pow(10,-12)) :
			return [(round(n / pow(10,-15),Digits)), 'f']
				#list.append([(round(n / pow(10,-15),Digits)), 'f'])

		elif n >= pow(10,-12) and n < (pow(10,-9)):
			return [(round(n / pow(10, -12), Digits)), 'p']
				#list.append([(round(n / pow(10, -12),Digits)),'p'])

		elif n >= pow(10,-9) and n < (pow(10,-6)):
			return [(round(n / pow(10, -9), Digits)), 'n']
				#list.append([(round(n / pow(10, -9),Digits)),'n'])

		elif n >= pow(10, -6) and n < (pow(10, -3)):
			return [(round(n / pow(10, -6), Digits)), "\u03BC"]
				#list.append([(round(n / pow(10, -6),Digits)),"\u03BC"])

		elif n >= pow(10, -3) and n < (pow(10, 0)):
			return [(round(n / pow(10, -3), Digits)), 'm']
				#list.append([(round(n / pow(10, -3),Digits)),'m'])

		elif n >= pow(10, 3) and n < (pow(10, 6)):
			return [(round(n / pow(10, 3), Digits)), 'k']
				#list.append([(round(n / pow(10, 3),Digits)),'k'])

		elif n >= pow(10, 6) and n < (pow(10, 9)):
			return [(round(n / pow(10, 6), Digits)), 'M']
				#list.append([(round(n / pow(10, 6), Digits)),'M'])

		elif n >= pow(10, 9) and n < (pow(10, 12)):
			return [(round(n / pow(10, 9), Digits)), 'G']
				#list.append([(round(n / pow(10, 9), Digits)),'G'])

		elif n >= pow(10, 12) and n < (pow(10, 15)):
			return [(round(n / pow(10, 12), Digits)), 'T']
				#list.append([(round(n / pow(10, 12), Digits)),'T'])
		else:
			return [(round(n, Digits)), '']
			#list.append([(round(n, Digits)),''])
		#return list[0]

if __name__ == "__main__":
	#from Import_Files import *
	from Defines import *

	#path = "C:\\Users\\iyoneda\\Desktop\\scope_25.csv"
	path = "C:\\Users\\iyoneda\\Desktop\\31026.csv"
	SpectrumAnalyzer(path)