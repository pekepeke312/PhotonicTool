import time
from typing import Union
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import skrf as rf
import plotly.io as pio
from TextWriter import TextWriter

import warnings
warnings.simplefilter(action='ignore', category=RuntimeWarning)

ColourTable = {
			0: "blue",
			1: "orange",
			2: "green",
			3: "red",
			4: "MediumPurple",
			5: "gray",
			6: "gold"
		}

class smith:
	def __init__(self, path=''):
		self.Path = path
		self.PlotlyEnable()
		self.S2PReader(self.Path)
		self.Fig_2D = go.Figure()
		self.Fig_3D = go.Figure()
		self.RF_Check_2D()

	def PlotlyEnable(self):
		# To make enable for Run mode
		pio.renderers.default = "browser"

	def UVtoG(self, UVList):
		if len([UVList]) > 1:
			list = []
			for n in UVList:
				[U, V] = n
				base = pow(U,2) - 2*U + pow(V,2) +1
				re = -1* (pow(U,2) + pow(V,2) - 1) / base
				imag = (2*V)/base
				list.append(np.complex32(re+imag*1.0j))
			return list
		else:
			[U, V] = UVList
			base = pow(U, 2) - 2 * U + pow(V, 2) + 1
			re = -1* (pow(U, 2) + pow(V, 2) - 1) / base
			imag = (2 * V) / base
			return complex(re + imag * 1.0j)

	def GtoUV(self,Impedance:[complex]):
		### numpy file format case ###
		try:
			if len(Impedance) >1:
				list = []
				for n in Impedance:
					re = n.real
					img = n.imag
					base = pow((1 + re), 2) + pow(img, 2)
					U = (pow(re, 2) + pow(img, 2) - 1) / base
					V = (2 * img) / base
					list.append([U, V])
				return list
			### single complex format case ###
			else:
				re = Impedance.real
				img = Impedance.imag
				base = pow((1 + re), 2) + pow(img, 2)
				U = (pow(re, 2) + pow(img, 2) - 1) / base
				V = (2 * img) / base
				return [U, V]

		except:
			if len([Impedance]) > 1:
				list = []
				for n in Impedance:
					Re = n.real
					Img = n.imag
					Base = pow((1 + Re), 2) + pow(Img, 2)
					U = (pow(Re, 2) + pow(Img, 2) - 1) / Base
					V = (2 * Img) / Base
					list.append([U, V])
				return list
			### single complex format case ###
			else:
				Re = Impedance.real
				Img = Impedance.imag
				Base = pow((1 + Re), 2) + pow(Img, 2)
				U = (pow(Re, 2) + pow(Img, 2) - 1) / Base
				V = (2 * Img) / Base
				return [U, V]

	def ZtoG(self, Zs:[complex], Zl:[complex]):
		if len([Zs]) > 1:
			list = []
			for n in Zs:
				list.append((n-Zl)/(n+Zl))
			return list
		else:
			return (Zs-Zl)/(Zs+Zl)

	def GtoV(self, Gumma: [Union[int, float]]):
		if len([Gumma]) > 1:
			list = []
			for n in Gumma:
				list.append((1+n)/(1-n))
			return list

		return (1+Gumma)/(1-Gumma)

	def ZtoZn(self,Z:[complex],Zo: [Union[int,float,complex]]):
		if len([Z]) > 1:
			list = []
			for n in Z:
				list.append(n/Zo)
			return list
		else:
			return Z/Zo

	def StoZ(self, Data):
		return (1 + Data) / (1 - Data)

	def AddCircle_2D(self, Radius=0, Center:[complex]="", Resolution=100, color="black", name=""):
		#re=Center.real
		#img=Center.imag
		r = Radius
		if name == "":
			name = 'R=' + str(r) + ' Center=' + str(Center)


		[U,V] = self.GtoUV(Center)

		circle_UV=[]
		circle_XY=[]

		for n in np.linspace(0,2*np.pi,Resolution):
			U_C = r*np.cos(n)+U
			V_C = r*np.sin(n)+V
			circle_UV.append([U_C,V_C])
			temp_XY = self.UVtoG([U_C,V_C])
			circle_XY.append([temp_XY.real, temp_XY.imag])

		self.Fig_2D.add_trace(
			go.Scatter(
				x=[U for [U, V] in circle_UV],
				y=[V for [U, V] in circle_UV],
				text=[f'Re: {Re:0.4f} <br>Img: {Img:0.4f}j' for [Re, Img] in circle_XY],
				hoverinfo='text',
				showlegend=True,
				line=dict(color=color),
				name=name
			),
		),

	def S2PReader(self,path=""):
		starttime = time.time()
		self.S2PFileName = path
		self.ring_slot = rf.Network(path)
		self.Freq = self.ring_slot.frequency.f
		self.Freq_Units = self.Add_Desimal_Unit(self.Freq)
		self.S11 = self.ring_slot.s[: ,0, 0]
		self.S12 = self.ring_slot.s[:, 0, 1]
		self.S21 = self.ring_slot.s[:, 1, 0]
		self.S22 = self.ring_slot.s[:, 1, 1]

		self.S11_z = self.StoZ(self.S11)
		self.S22_z = self.StoZ(self.S22)
		elapstedtime = time.time() - starttime
		print("S2P file Read Completed in {:.3}s".format(elapstedtime))
		TextWriter("S2P file Read Completed in {:.3}s".format(elapstedtime))

	def SparaTable(self, ViewPlot=False):
		starttime = time.time()
		#self.ring_slot.plot_s_db()
		self.SparaTable = go.Figure()
		customdata =[]

		S11_VSWR = self.ring_slot.s_vswr[:, 0, 0].tolist()
		S22_VSWR = self.ring_slot.s_vswr[:, 1, 1].tolist()

		S11_dB = self.ring_slot.s_db[:, 0, 0].tolist() #for Frame Data
		S12_dB = self.ring_slot.s_db[:, 0, 1].tolist() #for Frame Data
		S21_dB = self.ring_slot.s_db[:, 1, 0].tolist() #for Frame Data
		S22_dB = self.ring_slot.s_db[:, 1, 1].tolist() #for Frame Data

		for n in range(len(self.Freq_Units)):
			customdata.append([self.Freq[n],
							   self.Freq_Units[n],
							   S11_dB[n],
							   S12_dB[n],
							   S21_dB[n],
							   S22_dB[n],
							   S11_VSWR[n],
							   S22_VSWR[n],
							   ]) #for Data

		# S11_VSWR = self.ring_slot.s_vswr[:, 0, 0].tolist()
		# S22_VSWR = self.ring_slot.s_vswr[:, 1, 1].tolist()
		#
		# S11_dB = self.ring_slot.s_db[:, 0, 0].tolist() #for Frame Data
		# S12_dB = self.ring_slot.s_db[:, 0, 1].tolist() #for Frame Data
		# S21_dB = self.ring_slot.s_db[:, 1, 0].tolist() #for Frame Data
		# S22_dB = self.ring_slot.s_db[:, 1, 1].tolist() #for Frame Data

		order = ['S11','S12','S21','S22']

		for n in range(len(order)):
			self.SparaTable.add_trace(
				go.Scatter(
					visible = False,
					x=[0],
					y=[0],
					name=order[n],
					mode="markers",
					line=dict(color=ColourTable[n]),
			),
		),

		self.SparaTable.add_trace(
			go.Scatter(
				visible = True,
                x=[Freq for [Freq,FreqUnit, S11,S12, S21, S22,S11VS, S22VS] in customdata],
                y=[S11 for [Freq, FreqUnit, S11,S12, S21, S22,S11VS, S22VS] in customdata],
                text=[f'Freq: {FreqUnit}Hz <br>S11: {S11:0.4f}dB<br>VSWR: {S11VS:0.4f}' for [Freq,FreqUnit, S11, S12, S21, S22, S11VS, S22VS] in customdata],
				hoverinfo='text',
				name='S11',
				line=dict(color=ColourTable[0]),
				# exponentformat = "SI",
			),
        ),

		self.SparaTable.add_trace(
			go.Scatter(
				visible=True,
				x=[Freq for [Freq, FreqUnit,S11, S12, S21, S22,S11VS, S22VS] in customdata],
				y=[S12 for [Freq, FreqUnit,S11, S12, S21, S22,S11VS, S22VS] in customdata],
				text=[f'Freq: {FreqUnit}Hz <br>S12: {S12:0.4f}dB' for [Freq, FreqUnit,S11, S12, S21, S22,S11VS, S22VS] in customdata],
				hoverinfo='text',
				name='S12',
				line=dict(color=ColourTable[1])
			),
		),

		self.SparaTable.add_trace(
			go.Scatter(
				visible=True,
				x=[Freq for [Freq, FreqUnit,S11, S12, S21, S22,S11VS, S22VS] in customdata],
				y=[S21 for [Freq, FreqUnit,S11, S12, S21, S22,S11VS, S22VS] in customdata],
				text=[f'Freq: {FreqUnit}Hz <br>S21: {S21:0.4f}dB' for [Freq, FreqUnit,S11, S12, S21, S22,S11VS, S22VS] in customdata],
				hoverinfo='text',
				name='S21',
				line=dict(color=ColourTable[2])
			),
		),

		self.SparaTable.add_trace(
			go.Scatter(
				visible=True,
				x=[Freq for [Freq, FreqUnit,S11, S12, S21, S22,S11VS, S22VS] in customdata],
				y=[S22 for [Freq, FreqUnit,S11, S12, S21, S22,S11VS, S22VS] in customdata],
				text=[f'Freq: {FreqUnit}Hz <br>S22: {S22:0.4f}dB<br>VSWR: {S22VS:0.4f}' for [Freq, FreqUnit, S11, S12, S21, S22,S11VS, S22VS] in customdata],
				hoverinfo='text',
				name='S22',
				line=dict(color=ColourTable[3])
			),
		),

		self.SparaTable["frames"] = [
			go.Frame(
				data=[
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[S11_dB[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>S11: {S11_dB[n]:0.4f}dB <br>VSWR: {S11_VSWR[n]:0.4f}',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15,),
						xaxis='x',
						yaxis='y',
						line=dict(color=ColourTable[0]),
					),
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[S12_dB[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>S12: {S12_dB[n]:0.4f}dB',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15,),
						xaxis='x',
						yaxis='y',
						line=dict(color=ColourTable[1]),
					),
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[S21_dB[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>S21: {S21_dB[n]:0.4f}dB',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15,),
						xaxis='x',
						yaxis='y',
						line=dict(color=ColourTable[2]),
					),
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[S22_dB[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>S22: {S22_dB[n]:0.4f}dB<br>VSWR: {S22_VSWR[n]:0.4f}',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15,),
						xaxis='x',
						yaxis='y',
						line=dict(color=ColourTable[3]),
					),
					],
					name=self.Freq_Units[n]
				) for n in range(len(self.Freq_Units))
			]

		#self.SparaTable.update_xaxes(range=[min(self.Freq),max(self.Freq)])
		if ViewPlot:
			#### Slider Setting
			self.SparaTable["layout"]["sliders"] = [self.SliderSetting()]
			print("Slider Data Ready")
			TextWriter("Slider Data Ready")

			####
			# fill in most of layout template
			self.SparaTable["layout"]["updatemenus"] = [self.ButtonSetting()]
			print('Animation Button Ready')
			TextWriter('Animation Button Ready')

			self.SparaTable.show()

		elapstedtime = time.time() - starttime
		print("Sparameter Table Preparation Completed in {:.3}s".format(elapstedtime))
		TextWriter("Sparameter Table Preparation Completed in {:.3}s".format(elapstedtime))

	def StabilityTable(self, ViewPlot=False):
		starttime = time.time()
		self.StabilityTable = go.Figure()
		customdata = []
		self.Kfactor =[]
		self.Mufactor = []

		for n in range(len(self.Freq_Units)):
			Delta = self.S11[n] * self.S22[n] - self.S12[n] * self.S21[n]
			self.Kfactor.append((1 - pow(abs(self.S11[n]),2) - pow(abs(self.S22[n]),2) + pow(abs(Delta),2)) / (2 * abs(self.S21[n] * self.S12[n])))
			self.Mufactor.append((1 - pow(abs(self.S11[n]),2) )/ (abs(self.S22[n] - np.conj(self.S11[n]) * Delta) + abs(self.S21[n] * self.S12[n])))

			customdata.append([self.Freq[n],
							   self.Freq_Units[n],
							   self.Kfactor[n],
							   self.Mufactor[n],
							   ])  # for Data


		order = ['K-Factor', 'MU-Factor']
		for n in range(len(order)):
			self.StabilityTable.add_trace(
				go.Scatter(
					visible=False,
					x=[0],
					y=[0],
					name=order[n],
					mode="markers",
					line=dict(color=ColourTable[n]),
				),
			),

		self.StabilityTable.add_trace(
			go.Scatter(
				visible=True,
				x=[Freq for [Freq, FreqUnit, K, MU] in customdata],
				y=[K for [Freq, FreqUnit, K, MU] in customdata],
				text=[f'Freq: {FreqUnit}Hz <br>K-Factor: {K:0.4f}' for [Freq, FreqUnit, K, MU] in customdata],
				hoverinfo='text',
				name='K-Factor',
				line=dict(color=ColourTable[0])
			),
		),

		self.StabilityTable.add_trace(
			go.Scatter(
				visible=True,
				x=[Freq for [Freq, FreqUnit, K, MU] in customdata],
				y=[MU for [Freq, FreqUnit, K, MU] in customdata],
				text=[f'Freq: {FreqUnit}Hz <br>MU-Factor: {MU:0.4f}' for [Freq, FreqUnit, K, MU] in customdata],
				hoverinfo='text',
				name='MU-Factor',
				line=dict(color=ColourTable[1])
			),
		),

		self.StabilityTable["frames"] = [
			go.Frame(
				data=[
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[self.Kfactor[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>K-Factor: {self.Kfactor[n]:0.4f}',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x',
						yaxis='y',
						line=dict(color=ColourTable[0]),
					),
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[self.Mufactor[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>MU-Factor: {self.Mufactor[n]:0.4f}',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x',
						yaxis='y',
						line=dict(color=ColourTable[1]),
					),
				],
				name=self.Freq_Units[n]
			) for n in range(len(self.Freq_Units))
		]

		self.StabilityTable.update_yaxes(
			range = [0,5]
		)

		# self.SparaTable.update_xaxes(range=[min(self.Freq),max(self.Freq)])
		if ViewPlot:
			#### Slider Setting
			self.StabilityTable["layout"]["sliders"] = [self.SliderSetting()]
			print("Slider Data Ready")
			TextWriter("Slider Data Ready")

			####
			# fill in most of layout template
			self.StabilityTable["layout"]["updatemenus"] = [self.ButtonSetting()]
			print('Animation Button Ready')
			TextWriter('Animation Button Ready')

			self.StabilityTable.show()

		elapstedtime = time.time() - starttime
		print("Stability Factor Calculation Completed in {:.3}s".format(elapstedtime))
		TextWriter("Stability Factor Calculation Completed in {:.3}s".format(elapstedtime))

	def GainTable(self, ViewPlot=True):
		starttime = time.time()
		self.GainTable = go.Figure()
		customdata = []
		self.Gt = []
		self.Gp = []
		self.Ga = []

		for n in range(len(self.Freq_Units)):
			self.Gt.append(10 * np.log10(pow(abs(self.S21[n]),2)))
			self.Ga.append(10 * np.log10(pow(abs(self.S21[n]),2) / (1-pow(abs(self.S22[n]),2))))
			self.Gp.append(10 * np.log10(pow(abs(self.S21[n]),2) / (1 - pow(abs(self.S11[n]),2))))

			customdata.append([self.Freq[n],
							   self.Freq_Units[n],
							   self.Gt[n],
							   self.Ga[n],
							   self.Gp[n]
							   ])  # for Data

		order = ['Gt:Transducer Power Gain', 'Ga:Available Power Gain','Gp:Operating Power Gain']
		for n in range(len(order)):
			self.GainTable.add_trace(
				go.Scatter(
					visible=False,
					x=[0],
					y=[0],
					name=order[n],
					mode="markers",
					line=dict(color=ColourTable[n]),
				),
			),

		self.GainTable.add_trace(
			go.Scatter(
				visible=True,
				x=[Freq for [Freq, FreqUnit, Gt, Ga,Gp] in customdata],
				y=[Gt for [Freq, FreqUnit, Gt, Ga,Gp] in customdata],
				text=[f'Freq: {FreqUnit}Hz <br>Gt: {Gt:0.4f}dB' for [Freq, FreqUnit, Gt, Ga,Gp] in customdata],
				hoverinfo='text',
				name='Gt:Transducer Power Gain',
				line=dict(color=ColourTable[0])
			),
		),

		self.GainTable.add_trace(
			go.Scatter(
				visible=True,
				x=[Freq for [Freq, FreqUnit, Gt, Ga,Gp] in customdata],
				y=[Ga for [Freq, FreqUnit, Gt, Ga,Gp] in customdata],
				text=[f'Freq: {FreqUnit}Hz <br>Ga: {Ga:0.4f}dB' for [Freq, FreqUnit, Gt, Ga,Gp] in customdata],
				hoverinfo='text',
				name='Ga:Available Power Gain',
				line=dict(color=ColourTable[1])
			),
		),

		self.GainTable.add_trace(
			go.Scatter(
				visible=True,
				x=[Freq for [Freq, FreqUnit, Gt, Ga,Gp] in customdata],
				y=[Gp for [Freq, FreqUnit, Gt, Ga,Gp] in customdata],
				text=[f'Freq: {FreqUnit}Hz <br>Gp: {Gp:0.4f}dB' for [Freq, FreqUnit, Gt, Ga,Gp] in customdata],
				hoverinfo='text',
				name='Gp:Operating Power Gain',
				line=dict(color=ColourTable[2])
			),
		),

		self.GainTable["frames"] = [
			go.Frame(
				data=[
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[self.Gt[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>Gt: {self.Gt[n]:0.4f}dB',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x',
						yaxis='y',
						line=dict(color=ColourTable[0]),
					),
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[self.Ga[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>Ga: {self.Ga[n]:0.4f}dB',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x',
						yaxis='y',
						line=dict(color=ColourTable[1]),
					),
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[self.Gp[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>Gp: {self.Gp[n]:0.4f}dB',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x',
						yaxis='y',
						line=dict(color=ColourTable[2]),
					),
				],
				name=self.Freq_Units[n]
			) for n in range(len(self.Freq_Units))
		]

		# self.SparaTable.update_xaxes(range=[min(self.Freq),max(self.Freq)])
		if ViewPlot:
			#### Slider Setting
			self.GainTable["layout"]["sliders"] = [self.SliderSetting()]
			print("Slider Data Ready")
			TextWriter("Slider Data Ready")

			####
			# fill in most of layout template
			self.GainTable["layout"]["updatemenus"] = [self.ButtonSetting()]
			print('Animation Button Ready')
			TextWriter('Animation Button Ready')

			self.GainTable.show()

		elapstedtime = time.time() - starttime
		print("Ideal Gain Data Calculation Completed in {:.3}s".format(elapstedtime))
		TextWriter("Ideal Gain Data Calculation Completed in {:.3}s".format(elapstedtime))

	def SmithPlate(self):
		Constantlist1 = [0,0.2,0.5,1,2,5]
		Constantlist2 = [1,-1,2,-2,5,-5,0.5,-0.5,0.2,-0.2,0]
		Constantlist3 = [1,-1,2,-2,5,-5,0.5,-0.5,0.2,-0.2]
		Circle_U = []
		Circle_V = []
		Imp_U = []
		Imp_V= []
		Adm_U = []
		Adm_V =[]

		## Constant r circle
		for r in Constantlist1:
			for img in np.linspace(-100, 100, 3000, endpoint=False):
				[U,V] = self.GtoUV(r + 1j*img)
				Circle_U.append(U)
				Circle_V.append(V)

		## Constant Imaginary line, Impedance
		for img in Constantlist2:
			for r in np.linspace(100, 0, 500, endpoint=False):
				[U,V] = self.GtoUV(r+1j*img)
				Imp_U.append(U)
				Imp_V.append(V)
			for r in np.linspace(0, 100, 500, endpoint=False):
				[U,V] = self.GtoUV(r+1j*img)
				Imp_U.append(U)
				Imp_V.append(V)

		## Constant Imaginary line, Admittance
		for img in Constantlist3:
			for r in np.linspace(100, 0, 500, endpoint=False):
				[U,V] = self.GtoUV(1/(r+1j*img))
				Adm_U.append(U)
				Adm_V.append(V)
			for r in np.linspace(0, 100, 500, endpoint=False):
				[U,V] = self.GtoUV(1/(r+1j*img))
				Adm_U.append(U)
				Adm_V.append(V)
		return [[Circle_U,Circle_V],[Imp_U,Imp_V],[Adm_U,Adm_V]]

	def Add_Desimal_Unit(self,Data):
		Digits = 6
		list = []
		for n in Data:
			if n >= pow(10,-15) and n < (pow(10,-12)) :
				list.append(str(round(n / pow(10,-15),Digits)) + 'f')

			elif n >= pow(10,-12) and n < (pow(10,-9)):
				list.append(str(round(n / pow(10, -12),Digits)) + 'p')

			elif n >= pow(10,-9) and n < (pow(10,-6)):
				list.append(str(round(n / pow(10, -9),Digits)) + 'n')

			elif n >= pow(10, -6) and n < (pow(10, -3)):
				list.append(str(round(n / pow(10, -6),Digits)) + "\u03BC")

			elif n >= pow(10, -3) and n < (pow(10, 0)):
				list.append(str(round(n / pow(10, -3),Digits)) + 'm')

			elif n >= pow(10, 0) and n < (pow(10, 3)) or n == 0:
				list.append(str(round(n / pow(10, 0), Digits)) + '')

			elif n >= pow(10, 3) and n < (pow(10, 6)):
				list.append(str(round(n / pow(10, 3),Digits)) + 'k')

			elif n >= pow(10, 6) and n < (pow(10, 9)):
				list.append(str(round(n / pow(10, 6), Digits)) + 'M')

			elif n >= pow(10, 9) and n < (pow(10, 12)):
				list.append(str(round(n / pow(10, 9), Digits)) + 'G')

			elif n >= pow(10, 12) and n < (pow(10, 15)):
				list.append(str(round(n / pow(10, 12), Digits)) + 'T')
		return list

	def PlotlyGraph(self,Size_x=1,Size_y=1,plot=True):
		starttime = time.time()
		[[CU,CV],[IU,IV],[AU,AV]] = self.SmithPlate()

		#if Mode == '2D':
		#self.Fig_2D = go.Figure()
		self.Fig_2D.add_trace(
			go.Scatter(
					x = CU,
					y = CV,
					hoverinfo = 'skip',
					showlegend = False,
					line=dict(width=0.75,
							  color= 'black'),
            ),
		),

		self.Fig_2D.add_trace(
				go.Scatter(
					x=IU,
					y=IV,
					hoverinfo='skip',
					showlegend = False,
					line=dict(width=0.75,
							  dash='dash',
							  color="orange"),
				),
			),

		self.Fig_2D.add_trace(
				go.Scatter(
					x=AU,
					y=AV,
					hoverinfo='skip',
					showlegend = False,
					line=dict(width=0.75,
							  dash='dash',
							  color= "gold"),
				),
			),

		self.Fig_2D.add_trace(
				go.Scatter(
					x=[-1.02,-1,-0.66, 0, 0.62, 0.95, 1.03,-1,
					   -0.66,0,0.62, 0.95,
					   -0.66,-0.33,0,0.33,0.67],
					y=[-0.02,0.38,0.81, 1.02, 0.81,0.38,-0.02,
					   -0.42,-0.87,-1.07, -0.85,-0.42,
					   -0.02,-0.02,-0.02,-0.02,-0.02],
					text=["0", "+0.2j", "+0.5j", "+1j","+2j","+5j","\u221e",
						  "-0.2j","-0.5j","-1j","-2j","-5j",
						  "0.2","0.5","1","2","5"],
					mode = 'text',
					showlegend = False,
					hoverinfo='skip',
					textposition="top center",
					textfont=dict(
						size=22,
					),
				),
			),

		self.Fig_2D.update_yaxes(
			visible=False,	 #Disabling the original axis value
			scaleanchor='x',
			range = [-Size_y*1.2, Size_y*1.2],
		)

		self.Fig_2D.update_xaxes(
			visible=False,
			range=[-Size_x * 1.2, Size_x * 1.2],
        )

		if plot == True:
			self.Fig_2D.show()

		elapstedtime = time.time() - starttime
		print("Smithchart Template Calculation Completed in {:.3}s".format(elapstedtime))
		TextWriter("Smithchart Template Calculation Completed in {:.3}s".format(elapstedtime))

	def AddData_2D(self,Data="",color="black",name="",FrameColor=""):#,title=""):
		if type(Data) == complex or type(Data) == np.ndarray:
			re = Data.real
			img = Data.imag
		try:
			re.tolist()
			img.tolist()
		except:
			pass
		customdata = []

		self.Fig_2D.add_trace(	#dammy for Frame
			go.Scatter(
				x =[10],
				y =[0],
				name = 'Stablity Circle' + ': ' + name,
				mode="lines",
				line=dict(color=FrameColor),
			),
		)

		self.Fig_2D.add_trace(	#dammy for Frame
			go.Scatter(
				x =[10],
				y =[0],
				name = 'Viewing Data' + ': ' + name,
				mode="markers",
				line=dict(color=FrameColor),
			),
		)

		if type(Data) == complex or type(Data) == np.ndarray:
			S11_UV_data = self.GtoUV(Data)
			if type(re) == float:
				customdata.append([re,img])

				self.Fig_2D.add_trace(
					go.Scatter(
						x=[S11_UV_data[0]],
						y=[S11_UV_data[1]],
						text=[f'Re: {Re:0.4f} <br>Img: {Img:0.4f}jj' for [Re,Img] in customdata],
						hoverinfo='text',
						name = name,
						line = dict(color = color)
					))
			else:

				for n in range(len(re)):
					customdata.append([self.Freq_Units[n],re[n],img[n]])

				self.Fig_2D.add_trace(
					go.Scatter(
						x=[U for [U,V] in S11_UV_data],
						y=[V for [U,V] in S11_UV_data],
						text=[f'Freq: {Freq} <br>Re: {Re:0.4f} <br>Img: {Img:0.4f}j' for [Freq, Re, Img] in customdata],
						hoverinfo='text',
						line = dict(color = color),
						name = name
					),
				),

	def AddData_3D(self,Data="",color="black",name="",FrameColor=""):#,title=""):
		if type(Data) == complex or type(Data) == np.ndarray:
			re = Data.real
			img = Data.imag
		try:
			re.tolist()
			img.tolist()
		except:
			pass
		customdata = []

		self.Fig_3D.add_trace(	#dammy for Frame
			go.Scatter3d(
				x =[0],
				y =[0],
				z = [0],
				name = 'Stablity Circle' + ': ' + name,
				mode="markers",
				line=dict(color=FrameColor),
			),
		)

		self.Fig_3D.add_trace(	#dammy for Frame
			go.Scatter3d(
				x =[1],
				y =[1],
				z = [1],
				name = 'Viewing Data' + ': ' + name,
				mode="markers",
				line=dict(color=FrameColor),
			),
		)


		if type(Data) == complex or type(Data) == np.ndarray:
			S11_UV_data = self.GtoUV(Data)
			if type(re) == float:
				customdata.append([re,img])

				self.Fig_3D.add_trace(
					go.Scatter3d(
						x=[self.Freq.tolist()],
						z=[S11_UV_data[0]],
						y=[S11_UV_data[1]],
						text=[f'Re: {Re:0.4f} <br>Img: {Img:0.4f}jj' for [Re,Img] in customdata],
						hoverinfo='text',
						mode="markers",
						name = name,
						line = dict(color = color)
					))
			else:
				for n in range(len(re)):
					customdata.append([self.Freq_Units[n],re[n],img[n]])

				#x = self.Freq.tolist()
				#x.append(None)
				#S11_UV_data.append([None,None])

				self.Fig_3D.add_trace(
					go.Scatter3d(
						visible=True,
						x=[self.Freq.tolist()],
						z=[U for [U,V] in S11_UV_data],
						y=[V for [U,V] in S11_UV_data],
						#text=[f'Freq: {Freq} <br>Re: {Re:0.4f} <br>Img: {Img:0.4f}j' for [Freq, Re, Img] in customdata],
						#hoverinfo='text',
						mode="markers",
						line = dict(color = color),
						name = name
					),
				),

	def Title_Change(self, Mode = "2D", title="", color="", size=""):
		if Mode == "2D":
			self.Fig_2D.update_layout(
				dict(
					title=dict(
						text=title,
						x = 0.5,
						font = dict(
							size = size,
							color = color,
						)
					)
				)
			)
		elif Mode == "3D":
			self.Fig_3D.update_layout(
				dict(
					title=dict(
						text=title,
						x = 0.5,
						font = dict(
							size = size,
							color = color,
						)
					)
				)
			)

	def ButtonSetting(self):
		return dict(type='buttons',
			 # showactive=False,
			 y=0,
			 x=1.15,
			 xanchor='right',
			 yanchor='top',
			 pad=dict(t=0, r=10),
			 showactive=False,
			 buttons=[
				 dict(
					 label='Play',
					 method='animate',
					 args=[None,
						   dict(
							   frame=dict(
								   duration=10,
								   redraw=True,
							   ),
							   fromcurrent=True,
							   transition=dict(
								   duration=0,
							   ),
							   mode='immediate'
						   )
						   ],
				 ),
				 dict(
					 args=[
						 [None], dict(
							 frame=dict(
								 duration=0,
								 redraw=False
							 ),
							 mode='immediate',
							 transition=dict(duration=0)
						 )
					 ],
					 label='Pause',
					 method='animate'
				 ),
			 ],
			 direction='right',

			 )

	def SliderSetting(self):
		return dict(
			steps=[dict(
				method='animate',
				args=[[f'{k}'], #This should match with Frame name
					  dict(mode='immediate',
						   frame=dict(duration=500, redraw=False),#Reaction Time
						   transition=dict(duration=0),
						   )
					  ],
				label=f'{k}Hz',

			) for k in self.Freq_Units],
			transition=dict(duration=0,),	#Moving speed
			x=0,  # slider starting position
			y=0,
			currentvalue=dict(font=dict(size=12),
							  prefix='Frequency: ',
							  visible=True,
							  xanchor='right',
							  ),
			len=1.0, # slider length)
			)

	def AddSliderButton_2D(self,Label=""):
		# fill in most of layout template
		self.Fig_2D["layout"]["updatemenus"] =[
			self.ButtonSetting()
		]

		print('AddSliderButton_2D Finish')
		TextWriter('AddSliderButton_2D Finish')

	def AddSlider(self, Label="",name=""):
		# Slider Setting
		self.Fig_2D["layout"]["sliders"] = [self.SliderSetting()]
		print("AddSliderButton_2D Finished")
		TextWriter("AddSliderButton_2D Finished")

	def AddFrames_2D(self,Data="",color=""):
		if type(Data) == complex or type(Data) == np.ndarray:
			re = Data.real
			img = Data.imag
		try:
			re.tolist()
			img.tolist()
		except:
			pass
		customdata = []
		if type(Data) == complex or type(Data) == np.ndarray:
			UV_data = self.GtoUV(Data)
			U = [row[0] for row in UV_data]
			V = [row[1] for row in UV_data]

			for n in range(len(re)):
				customdata.append([self.Freq_Units[n], re[n], img[n]])

			self.Fig_2D["frames"] = [
				go.Frame(
					data = [
						go.Scatter(
						visible = True,
						x = [U[n]],
						y = [V[n]],
						text=[f'Freq: {self.Freq_Units[n]} <br>Re: {re[n]:0.4f} <br>Img: {img[n]:0.4f}j'],# for [Freq, Re, Img] in customdata],
						hoverinfo='text',
						mode="markers",
						marker = dict(size=15,),
						line=dict(color=color),
						)
					],
					name = self.Freq_Units[n]
				) for n in range(len(self.Freq_Units))
			]

			print('Adding Frames Finished')
			TextWriter('Adding Frames Finished')

	def GenerateCircleList(self,Center,Radius,Resolution=100):
		ReturnList = []

		#[UC, VC] = self.GtoUV(Center)
		UV_Center = self.GtoUV(Center)
		UC = [row[0] for row in UV_Center]
		VC = [row[1] for row in UV_Center]


		for k in range(len(Radius)):
			circle_XY=[]
			circle_UV=[]
			for n in np.linspace(0, 2 * np.pi, Resolution):
				U_C = Radius[k] * np.cos(n) + UC[k]
				V_C = Radius[k] * np.sin(n) + VC[k]
				circle_UV.append([U_C, V_C])
				temp_XY = self.UVtoG([U_C, V_C])
				circle_XY.append([temp_XY.real, temp_XY.imag])

			ReturnList.append([circle_UV, circle_XY])

		return ReturnList

	def AddStablilityFrames_2D(self,DataCenter,DataRadius,Data, color):
		if type(Data) == complex or type(Data) == np.ndarray:
			re = Data.real
			img = Data.imag

		try:
			re.tolist()
			img.tolist()

		except:
			pass

		CircleList = self.GenerateCircleList(DataCenter,DataRadius)
		CircleData = [row[0] for row in CircleList]
		CircleName = [row[1] for row in CircleList]

		#if type(Data) == complex or type(Data) == np.ndarray:
		UV_data = self.GtoUV(Data)
		U = [row[0] for row in UV_data]
		V = [row[1] for row in UV_data]

			#customdata = []
			#for n in range(len(DataRadius)):
			#	customdata.append([self.Freq_Units[n], re[n], img[n]])

		self.Fig_2D["frames"] = [
				go.Frame(
					data = [
						go.Scatter(
						visible = True,
						x = [U for [U,V]in CircleData[n]],
						y = [V for [U,V]in CircleData[n]],
						text=[f'Freq: {self.Freq_Units[n]}<br>Re: {Re:0.4f} <br>Img: {Img:0.4f}' for [Re, Img] in CircleName[n]],
						hoverinfo='text',
						mode="lines",
						marker = dict(size=15,),
						line=dict(color=color),
						),
						go.Scatter(
							visible=True,
							x=[U[n]],
							y=[V[n]],
							text=[f'Freq: {self.Freq_Units[n]} <br>Re: {re[n]:0.4f} <br>Img: {img[n]:0.4f}j'],
							hoverinfo='text',
							mode="markers",
							marker=dict(size=15, ),
							line=dict(color=color),
						)
					],
					name = self.Freq_Units[n]
				) for n in range(len(self.Freq_Units))
			]
		print('Adding Stablitiy Frames Finished')
		TextWriter('Adding Stablitiy Frames Finished')

	def SmithChart_2D(self,Data='S11',Slider=True,TraceColor='black',FrameColor='black',Name='',Title='SmithChart_Plot',TitleSize=15,TitleColor='black'):
		S_out = Data[1]
		S_in = Data[2]
		ViewData_Spara = self.ring_slot.s[: ,int(S_out)-1, int(S_in)-1]
		ViewData = self.StoZ(ViewData_Spara)
		if Name == '':
			Name = Data		#Default name setting

		self.AddFrames_2D(ViewData, color=FrameColor)
		self.AddData_2D(ViewData, color=TraceColor, name=Name)
		self.Title_Change(title=Title, color=TitleColor, size=TitleSize)
		if Slider:
			self.AddSlider(Label=SMITH.Freq_Units, name=Name)
			self.AddSliderButton_2D()

	def Stability(self,Mode = "2D",Data='S11',Frame="", Slider=True,TraceColor='black',FrameColor='black',Name='Stability',Title='SmithChart_Plot',TitleSize=15,TitleColor='black'):
		starttime = time.time()
		self.Delta = []
		self.In_CenterLocation=[]
		self.Out_CenterLocation=[]
		self.In_Radius = []
		self.Out_Radius = []

		for n in range(len(self.S11)):
			self.Delta.append(self.S11[n] * self.S22[n] -  self.S12[n] *self.S21[n])

			## Center Location @ Input
			self.In_CenterLocation.append((self.S11[n] - self.S22[n].conjugate() * self.Delta[n]).conjugate() / (pow(abs(self.S11[n]),2) - pow(abs(self.Delta[n]),2)))
			self.Out_CenterLocation.append((self.S22[n] - self.S11[n].conjugate() * self.Delta[n]).conjugate() / (pow(abs(self.S22[n]),2) - pow(abs(self.Delta[n]),2)))

			# Radius @ Input
			self.In_Radius.append(abs(self.S12[n] * self.S21[n]) / (pow(abs(self.S11[n]),2) - pow(abs(self.Delta[n]),2)))
			self.Out_Radius.append(abs(self.S12[n] * self.S21[n]) / (pow(abs(self.S22[n]), 2) - pow(abs(self.Delta[n]), 2)))

		S_out = Data[1]
		S_in = Data[2]
		ViewData_Spara = self.ring_slot.s[:, int(S_out) - 1, int(S_in) - 1]
		ViewData = self.StoZ(ViewData_Spara)

		if (S_out == '1') and (S_in == '1'):
			Center_Circle = self.StoZ(np.array(self.In_CenterLocation))
			Radius_Circle = self.In_Radius
		elif(S_out == '2') and (S_in == '2'):
			Center_Circle = self.StoZ(np.array(self.Out_CenterLocation))
			Radius_Circle = self.Out_Radius

		if Name == '':
			Name = Data  # Default name setting

		if Mode == "2D":
			self.AddData_2D(ViewData, color=TraceColor, name=Name,FrameColor=FrameColor)
			if Frame:
				self.AddStablilityFrames_2D(DataCenter=Center_Circle,DataRadius=Radius_Circle,Data=ViewData, color=FrameColor)
			if Slider:
				self.AddSlider(Label=SMITH.Freq_Units, name=Name)
				self.AddSliderButton_2D()

		if Mode == "3D":
			self.AddData_3D(ViewData, color=TraceColor, name=Name,FrameColor=FrameColor)

			self.Fig_3D.update_layout(
				scene=dict(
					xaxis=dict(range=[-2, max(self.Freq)], ),
					yaxis=dict(range=[-2, 2], ),
					zaxis=dict(range=[-2, 2], ), ),
			)

		self.Title_Change(title=Title, Mode=Mode, color=TitleColor, size=TitleSize)
		elapstedtime = time.time() - starttime
		print("Stability Circle Calculation Completed in {:.3}s".format(elapstedtime))
		TextWriter("Stability Circle Calculation Completed in {:.3}s".format(elapstedtime))

	def RF_Check_2D(self, TraceColor='red', FrameColor='blue', Name='',	Title='SmithChart_Plot', TitleSize=15, TitleColor='black'):
		print("--- Preparing S11 data ---")
		self.Stability(Data='S11',Mode="2D", Frame=False, Slider=False, TraceColor=TraceColor, FrameColor=FrameColor, Name=Name, Title='S11',
					 TitleColor=TitleColor, TitleSize=TitleSize)
		self.PlotlyGraph(plot=False, Size_x=1.5, Size_y=1.5)
		self.S11_Smith_Fig = self.Fig_2D

		## Reset Fig_2D data
		self.Fig_2D = go.Figure()
		####################

		print("--- Preparing S22 data ---")
		TextWriter("--- Preparing S22 data ---")

		self.Stability(Data='S22',Mode="2D", Frame=False, Slider=False, TraceColor=TraceColor, FrameColor=FrameColor, Name=Name, Title='S22',
					 TitleColor=TitleColor, TitleSize=TitleSize)
		self.PlotlyGraph(plot=False, Size_x=1.5, Size_y=1.5)
		self.S22_Smith_Fig = self.Fig_2D

		self.RF_Check_Smith_2D = make_subplots(rows=2, cols=6,
											   specs = [ [{"colspan": 2}, None, {"colspan": 2}, None, {"colspan": 2}, None],
														[{"colspan": 3}, None, None,{"colspan": 3}, None, None ],
														],
											   shared_xaxes=False,
											   vertical_spacing=0.05,
											   subplot_titles = ("S-Parameter","Stability Factor","Ideal Gain",
																 "Input Stability Circle", "Output Stability Circle"),
											   row_width=[0.6, 0.4])

		# Creating Data
		print("")
		self.SparaTable(ViewPlot=False)
		print("")
		self.StabilityTable(ViewPlot=False)
		print("")
		self.GainTable(ViewPlot=False)
		#print("Subplot Data Ready")

		starttime = time.time()
		### Dummy Data import ###
		for n in range(4):
			self.RF_Check_Smith_2D.add_trace(self.SparaTable['data'][n],row=1, col=1)
		for n in range(2):
			self.RF_Check_Smith_2D.add_trace(self.StabilityTable['data'][n], row=1, col=3)
		for n in range(3):
			self.RF_Check_Smith_2D.add_trace(self.GainTable['data'][n], row=1, col=5)
		for n in range(2):
			self.RF_Check_Smith_2D.add_trace(self.S11_Smith_Fig['data'][n],row=2, col=1)
		for n in range(2):
			self.RF_Check_Smith_2D.add_trace(self.S22_Smith_Fig['data'][n],row=2, col=4)

		### Plot Data import ###
		for n in range(4):
			self.RF_Check_Smith_2D.add_trace(self.SparaTable['data'][n+4],row=1, col=1)
		for n in range(2):
			self.RF_Check_Smith_2D.add_trace(self.StabilityTable['data'][n+2], row=1, col=3)
		for n in range(3):
			self.RF_Check_Smith_2D.add_trace(self.GainTable['data'][n+3], row=1, col=5)
		for n in range(5):
			self.RF_Check_Smith_2D.add_trace(self.S11_Smith_Fig['data'][n+2],row=2, col=1)
		for n in range(5):
			self.RF_Check_Smith_2D.add_trace(self.S22_Smith_Fig['data'][n+2],row=2, col=4)

		## S-parameter Table Copy
		S11_VSWR = self.ring_slot.s_vswr[:, 0, 0].tolist()
		S22_VSWR = self.ring_slot.s_vswr[:, 1, 1].tolist()

		S11_dB = self.ring_slot.s_db[:, 0, 0].tolist() #for Frame Data
		S12_dB = self.ring_slot.s_db[:, 0, 1].tolist() #for Frame Data
		S21_dB = self.ring_slot.s_db[:, 1, 0].tolist() #for Frame Data
		S22_dB = self.ring_slot.s_db[:, 1, 1].tolist() #for Frame Data

		elapstedtime = time.time() - starttime
		print("Drawing Data Transfer Completed in {:.3}s".format(elapstedtime))
		TextWriter("Drawing Data Transfer Completed in {:.3}s".format(elapstedtime))

		##Frame Over write #####################################

		print("Preparing Frame Data...")
		TextWriter("Preparing Frame Data...")

		starttime = time.time()
		Operation = ["S11","S22"]
		for Data in Operation:
			S_out = Data[1]
			S_in = Data[2]
			ViewData_Spara = self.ring_slot.s[:, int(S_out) - 1, int(S_in) - 1]
			ViewData = self.StoZ(ViewData_Spara)

			if (S_out == '1') and (S_in == '1'):
				Center_Circle = self.StoZ(np.array(self.In_CenterLocation))
				Radius_Circle = self.In_Radius

				CircleList_S11 = self.GenerateCircleList(Center_Circle, Radius_Circle)
				CircleData_S11 = [row[0] for row in CircleList_S11]
				CircleName_S11 = [row[1] for row in CircleList_S11]

				# if type(Data) == complex or type(Data) == np.ndarray:
				viewdata = self.StoZ(ViewData_Spara)
				if type(viewdata) == complex or type(viewdata) == np.ndarray:
					re_S11 = viewdata.real
					img_S11 = viewdata.imag

				try:
					re_S11.tolist()
					img_S11.tolist()

				except:
					pass

				UV_data = self.GtoUV(viewdata)
				U_S11 = [row[0] for row in UV_data]
				V_S11 = [row[1] for row in UV_data]


			elif (S_out == '2') and (S_in == '2'):
				Center_Circle = self.StoZ(np.array(self.Out_CenterLocation))
				Radius_Circle = self.Out_Radius

				CircleList_S22 = self.GenerateCircleList(Center_Circle, Radius_Circle)
				CircleData_S22 = [row[0] for row in CircleList_S22]
				CircleName_S22 = [row[1] for row in CircleList_S22]

				viewdata = self.StoZ(ViewData_Spara)
				if type(viewdata) == complex or type(viewdata) == np.ndarray:
					re_S22 = viewdata.real
					img_S22 = viewdata.imag

				try:
					re_S22.tolist()
					img_S22.tolist()

				except:
					pass

				UV_data = self.GtoUV(viewdata)
				U_S22 = [row[0] for row in UV_data]
				V_S22 = [row[1] for row in UV_data]

		self.RF_Check_Smith_2D["frames"] = [
			go.Frame(
				data=[
					### Graph Plot #1 ###
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[S11_dB[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>S11: {S11_dB[n]:0.4f}dB <br>VSWR: {S11_VSWR[n]:0.4f}',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x1',
						yaxis='y1',
						line=dict(color=ColourTable[0]),
					),
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[S12_dB[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>S12: {S12_dB[n]:0.4f}dB',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x1',
						yaxis='y1',
						line=dict(color=ColourTable[1]),
					),
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[S21_dB[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>S21: {S21_dB[n]:0.4f}dB',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x1',
						yaxis='y1',
						line=dict(color=ColourTable[2]),
					),
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[S22_dB[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>S22: {S22_dB[n]:0.4f}dB<br>VSWR: {S22_VSWR[n]:0.4f}',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x1',
						yaxis='y1',
						line=dict(color=ColourTable[3]),
					),

					### Graph Plot #2 ###
				   go.Scatter(
					   visible=True,
						x=[self.Freq[n]],
						y=[self.Kfactor[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>K-Factor: {self.Kfactor[n]:0.4f}',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x2',
						yaxis='y2',
						line=dict(color=ColourTable[0]),
						),
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[self.Mufactor[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>MU-Factor: {self.Mufactor[n]:0.4f}',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x2',
						yaxis='y2',
						line=dict(color=ColourTable[1]),
					),
					#####################
					### Graph Plot #3 ###
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[self.Gt[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>Gt: {self.Gt[n]:0.4f}dB',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x3',
						yaxis='y3',
						line=dict(color=ColourTable[0]),
					),
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[self.Ga[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>Ga: {self.Ga[n]:0.4f}dB',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x3',
						yaxis='y3',
						line=dict(color=ColourTable[1]),
					),
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[self.Gp[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>Gp: {self.Gp[n]:0.4f}dB',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x3',
						yaxis='y3',
						line=dict(color=ColourTable[2]),
					),
					#####################
					### Graph Plot #4 ###
					go.Scatter(
						visible=True,
						x=[U for [U, V] in CircleData_S11[n]],
						y=[V for [U, V] in CircleData_S11[n]],
						text=[f'Freq: {self.Freq_Units[n]}<br>Re: {Re:0.4f} <br>Img: {Img:0.4f}' for [Re, Img]
							  in CircleName_S11[n]],
						hoverinfo='text',
						mode="lines",
						marker=dict(size=15,),
						xaxis='x4',
						yaxis='y4',
						line=dict(color=ColourTable[0]),
					),
					go.Scatter(
						visible=True,
						x=[U_S11[n]],
						y=[V_S11[n]],
						text=[f'Freq: {self.Freq_Units[n]} <br>Re: {re_S11[n]:0.4f} <br>Img: {img_S11[n]:0.4f}j'],
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x4',
						yaxis='y4',
						line=dict(color=ColourTable[0]),
					),
					### Graph Plot #5 ###
					go.Scatter(
						visible=True,
						x=[U for [U, V] in CircleData_S22[n]],
						y=[V for [U, V] in CircleData_S22[n]],
						text=[f'Freq: {self.Freq_Units[n]}<br>Re: {Re:0.4f} <br>Img: {Img:0.4f}' for [Re, Img]
							  in CircleName_S22[n]],
						hoverinfo='text',
						mode="lines",
						marker=dict(size=15, ),
						xaxis='x5',
						yaxis='y5',
						line=dict(color=ColourTable[3]),
					),

					go.Scatter(
						visible=True,
						x=[U_S22[n]],
						y=[V_S22[n]],
						text=[f'Freq: {self.Freq_Units[n]} <br>Re: {re_S22[n]:0.4f} <br>Img: {img_S22[n]:0.4f}j'],
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x5',
						yaxis='y5',
						line=dict(color=ColourTable[3]),
					),
					####

					],
					name=self.Freq_Units[n]
				) for n in range(len(self.Freq_Units))
			]
		elapstedtime = time.time() - starttime
		print("Frame Data Completed in {:.3}s".format(elapstedtime))
		TextWriter("Frame Data Completed in {:.3}s".format(elapstedtime))

		#print("Frame Data Ready")

		starttime = time.time()
		## Layout update
		self.RF_Check_Smith_2D.update_layout(
			title = dict(
					text = "RF Parameters of " + str(self.Path.split('\\')[-1:]),
					xanchor='auto'
					),
			title_font = dict(
				size = 20
			),
		)

		self.RF_Check_Smith_2D.update_yaxes(
			row=1,
			col=3,
			range = [0,5],
		)

		self.RF_Check_Smith_2D.update_xaxes(
			row=1,
			col=1,
			exponentformat="SI",
		)

		self.RF_Check_Smith_2D.update_xaxes(
			row=1,
			col=3,
			exponentformat="SI",
		)

		self.RF_Check_Smith_2D.update_xaxes(
			row=1,
			col=5,
			exponentformat="SI",
		)


		for n in [1, 4]:
			self.RF_Check_Smith_2D.update_xaxes(row=2, col=n,
												range=self.S22_Smith_Fig['layout']['xaxis']['range'],
												visible=self.S22_Smith_Fig['layout']['xaxis']['visible'])
			self.RF_Check_Smith_2D.update_yaxes(row=2, col=n,
												range=self.S22_Smith_Fig['layout']['yaxis']['range'],
												visible=self.S22_Smith_Fig['layout']['yaxis']['visible'],
												scaleanchor=self.RF_Check_Smith_2D['layout']['yaxis5']['scaleanchor'])


		#### Slider Setting
		self.RF_Check_Smith_2D["layout"]["sliders"] = [self.SliderSetting()]

		elapstedtime = time.time() - starttime
		print("Slider Data Completed in {:.3}s".format(elapstedtime))
		TextWriter("Slider Data Completed in {:.3}s".format(elapstedtime))

		#print("Slider Data Ready")

		####
		# fill in most of layout template
		#self.RF_Check_Smith_2D["layout"]["updatemenus"] = [self.ButtonSetting()]
		#print('Animation Button Ready')

		self.RF_Check_Smith_2D.show()

	def RF_Check_3D(self, TraceColor='black', FrameColor='black', Name='Stability', TitleSize=15, TitleColor='black'):

		self.Stability(Data='S11',Mode="3D", Frame=False, Slider=False, TraceColor=TraceColor, FrameColor=FrameColor, Name=Name, Title='S11',
					 TitleColor=TitleColor, TitleSize=TitleSize)
		self.PlotlyGraph(plot=False, Size_x=1.5, Size_y=1.5)
		self.S11_Smith_Fig = self.Fig_3D

		## Reset Fig_2D data
		self.Fig_2D = go.Figure()
		####################

		self.Stability(Data='S22',Mode="3D", Frame=False, Slider=False, TraceColor=TraceColor, FrameColor=FrameColor, Name=Name, Title='S22',
					 TitleColor=TitleColor, TitleSize=TitleSize)
		self.PlotlyGraph(plot=False, Size_x=1.5, Size_y=1.5)
		self.S22_Smith_Fig = self.Fig_2D

		self.RF_Check_Smith_2D = make_subplots(rows=2, cols=6,
											   specs = [ [{"colspan": 2}, None, {"colspan": 2}, None, {"colspan": 2}, None],
														[{"colspan": 3}, None, None,{"colspan": 3}, None, None ],
														],
											   shared_xaxes=False,
											   vertical_spacing=0.05,
											   subplot_titles = ("S-Parameter","Sabality Factor","Ideal Gain",
																 "Input Stability Circle", "Output Stability Circle"),
											   row_width=[0.6, 0.4])

		# Creating Data
		self.SparaTable(ViewPlot=False)
		self.StabilityTable(ViewPlot=False)
		self.GainTable(ViewPlot=False)
		print("Subplot Data Ready")
		TextWriter("Subplot Data Ready")

		### Dummy Data import ###
		for n in range(4):
			self.RF_Check_Smith_2D.add_trace(self.SparaTable['data'][n],row=1, col=1)
		for n in range(2):
			self.RF_Check_Smith_2D.add_trace(self.StabilityTable['data'][n], row=1, col=3)
		for n in range(3):
			self.RF_Check_Smith_2D.add_trace(self.GainTable['data'][n], row=1, col=5)
		for n in range(2):
			self.RF_Check_Smith_2D.add_trace(self.S11_Smith_Fig['data'][n],row=2, col=1)
		for n in range(2):
			self.RF_Check_Smith_2D.add_trace(self.S22_Smith_Fig['data'][n],row=2, col=4)

		### Plot Data import ###
		for n in range(4):
			self.RF_Check_Smith_2D.add_trace(self.SparaTable['data'][n+4],row=1, col=1)
		for n in range(2):
			self.RF_Check_Smith_2D.add_trace(self.StabilityTable['data'][n+2], row=1, col=3)
		for n in range(3):
			self.RF_Check_Smith_2D.add_trace(self.GainTable['data'][n+3], row=1, col=5)
		for n in range(5):
			self.RF_Check_Smith_2D.add_trace(self.S11_Smith_Fig['data'][n+2],row=2, col=1)
		for n in range(5):
			self.RF_Check_Smith_2D.add_trace(self.S22_Smith_Fig['data'][n+2],row=2, col=4)

		## S-parameter Table Copy
		S11_VSWR = self.ring_slot.s_vswr[:, 0, 0].tolist()
		S22_VSWR = self.ring_slot.s_vswr[:, 1, 1].tolist()

		S11_dB = self.ring_slot.s_db[:, 0, 0].tolist() #for Frame Data
		S12_dB = self.ring_slot.s_db[:, 0, 1].tolist() #for Frame Data
		S21_dB = self.ring_slot.s_db[:, 1, 0].tolist() #for Frame Data
		S22_dB = self.ring_slot.s_db[:, 1, 1].tolist() #for Frame Data

		##Frame Over write #####################################

		print("Preparing Frame Data...")
		TextWriter("Preparing Frame Data...")

		Operation = ["S11","S22"]
		for Data in Operation:
			S_out = Data[1]
			S_in = Data[2]
			ViewData_Spara = self.ring_slot.s[:, int(S_out) - 1, int(S_in) - 1]
			ViewData = self.StoZ(ViewData_Spara)

			if (S_out == '1') and (S_in == '1'):
				Center_Circle = self.StoZ(np.array(self.In_CenterLocation))
				Radius_Circle = self.In_Radius

				CircleList_S11 = self.GenerateCircleList(Center_Circle, Radius_Circle)
				CircleData_S11 = [row[0] for row in CircleList_S11]
				CircleName_S11 = [row[1] for row in CircleList_S11]

				# if type(Data) == complex or type(Data) == np.ndarray:
				viewdata = self.StoZ(ViewData_Spara)
				if type(viewdata) == complex or type(viewdata) == np.ndarray:
					re_S11 = viewdata.real
					img_S11 = viewdata.imag

				try:
					re_S11.tolist()
					img_S11.tolist()

				except:
					pass

				UV_data = self.GtoUV(viewdata)
				U_S11 = [row[0] for row in UV_data]
				V_S11 = [row[1] for row in UV_data]


			elif (S_out == '2') and (S_in == '2'):
				Center_Circle = self.StoZ(np.array(self.Out_CenterLocation))
				Radius_Circle = self.Out_Radius

				CircleList_S22 = self.GenerateCircleList(Center_Circle, Radius_Circle)
				CircleData_S22 = [row[0] for row in CircleList_S22]
				CircleName_S22 = [row[1] for row in CircleList_S22]

				viewdata = self.StoZ(ViewData_Spara)
				if type(viewdata) == complex or type(viewdata) == np.ndarray:
					re_S22 = viewdata.real
					img_S22 = viewdata.imag

				try:
					re_S22.tolist()
					img_S22.tolist()

				except:
					pass

				UV_data = self.GtoUV(viewdata)
				U_S22 = [row[0] for row in UV_data]
				V_S22 = [row[1] for row in UV_data]

		self.RF_Check_Smith_2D["frames"] = [
			go.Frame(
				data=[
					### Graph Plot #1 ###
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[S11_dB[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>S11: {S11_dB[n]:0.4f}dB <br>VSWR: {S11_VSWR[n]:0.4f}',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x1',
						yaxis='y1',
						line=dict(color=ColourTable[0]),
					),
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[S12_dB[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>S12: {S12_dB[n]:0.4f}dB',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x1',
						yaxis='y1',
						line=dict(color=ColourTable[1]),
					),
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[S21_dB[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>S21: {S21_dB[n]:0.4f}dB',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x1',
						yaxis='y1',
						line=dict(color=ColourTable[2]),
					),
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[S22_dB[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>S22: {S22_dB[n]:0.4f}dB<br>VSWR: {S22_VSWR[n]:0.4f}',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x1',
						yaxis='y1',
						line=dict(color=ColourTable[3]),
					),

					### Graph Plot #2 ###
				   go.Scatter(
					   visible=True,
						x=[self.Freq[n]],
						y=[self.Kfactor[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>K-Factor: {self.Kfactor[n]:0.4f}',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x2',
						yaxis='y2',
						line=dict(color=ColourTable[0]),
						),
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[self.Mufactor[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>MU-Factor: {self.Mufactor[n]:0.4f}',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x2',
						yaxis='y2',
						line=dict(color=ColourTable[1]),
					),
					#####################
					### Graph Plot #3 ###
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[self.Gt[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>Gt: {self.Gt[n]:0.4f}dB',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x3',
						yaxis='y3',
						line=dict(color=ColourTable[0]),
					),
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[self.Ga[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>Ga: {self.Ga[n]:0.4f}dB',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x3',
						yaxis='y3',
						line=dict(color=ColourTable[1]),
					),
					go.Scatter(
						visible=True,
						x=[self.Freq[n]],
						y=[self.Gp[n]],
						text=f'Freq: {self.Freq_Units[n]}Hz <br>Gp: {self.Gp[n]:0.4f}dB',
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x3',
						yaxis='y3',
						line=dict(color=ColourTable[2]),
					),
					#####################
					### Graph Plot #4 ###
					go.Scatter(
						visible=True,
						x=[U for [U, V] in CircleData_S11[n]],
						y=[V for [U, V] in CircleData_S11[n]],
						text=[f'Freq: {self.Freq_Units[n]}<br>Re: {Re:0.4f} <br>Img: {Img:0.4f}' for [Re, Img]
							  in CircleName_S11[n]],
						hoverinfo='text',
						mode="lines",
						marker=dict(size=15,),
						xaxis='x4',
						yaxis='y4',
						line=dict(color=ColourTable[0]),
					),
					go.Scatter(
						visible=True,
						x=[U_S11[n]],
						y=[V_S11[n]],
						text=[f'Freq: {self.Freq_Units[n]} <br>Re: {re_S11[n]:0.4f} <br>Img: {img_S11[n]:0.4f}j'],
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x4',
						yaxis='y4',
						line=dict(color=ColourTable[0]),
					),
					### Graph Plot #5 ###
					go.Scatter(
						visible=True,
						x=[U for [U, V] in CircleData_S22[n]],
						y=[V for [U, V] in CircleData_S22[n]],
						text=[f'Freq: {self.Freq_Units[n]}<br>Re: {Re:0.4f} <br>Img: {Img:0.4f}' for [Re, Img]
							  in CircleName_S22[n]],
						hoverinfo='text',
						mode="lines",
						marker=dict(size=15, ),
						xaxis='x5',
						yaxis='y5',
						line=dict(color=ColourTable[3]),
					),

					go.Scatter(
						visible=True,
						x=[U_S22[n]],
						y=[V_S22[n]],
						text=[f'Freq: {self.Freq_Units[n]} <br>Re: {re_S22[n]:0.4f} <br>Img: {img_S22[n]:0.4f}j'],
						hoverinfo='text',
						mode="markers",
						marker=dict(size=15, ),
						xaxis='x5',
						yaxis='y5',
						line=dict(color=ColourTable[3]),
					),
					####

					],
					name=self.Freq_Units[n]
				) for n in range(len(self.Freq_Units))
			]
		print("Frame Data Ready")
		TextWriter("Frame Data Ready")

		## Layout update
		self.RF_Check_Smith_2D.update_layout(
			title = dict(
					text = self.S2PFileName,
					),
			title_font = dict(
				size = 20
			),
		)

		self.RF_Check_Smith_2D.update_yaxes(
			row=1,
			col=3,
			range = [0,5],
		)

		for n in [1, 4]:
			self.RF_Check_Smith_2D.update_xaxes(row=2, col=n,
												range=self.S22_Smith_Fig['layout']['xaxis']['range'],
												visible=self.S22_Smith_Fig['layout']['xaxis']['visible'])
			self.RF_Check_Smith_2D.update_yaxes(row=2, col=n,
												range=self.S22_Smith_Fig['layout']['yaxis']['range'],
												visible=self.S22_Smith_Fig['layout']['yaxis']['visible'],
												scaleanchor=self.RF_Check_Smith_2D['layout']['yaxis5']['scaleanchor'])


		#### Slider Setting
		self.RF_Check_Smith_2D["layout"]["sliders"] = [self.SliderSetting()]
		print("Slider Data Ready")
		TextWriter("Slider Data Ready")

		####
		# fill in most of layout template
		self.RF_Check_Smith_2D["layout"]["updatemenus"] = [self.ButtonSetting()]
		print('Animation Button Ready')
		TextWriter('Animation Button Ready')

		self.RF_Check_Smith_2D.show()


if __name__ == "__main__":
	path = "S2PFile//2012-N10209-401723.s2p"
	SMITH = smith(path=path)

#	SMITH.S2PReader(path)

	#SMITH.Stability(Data='S22',Mode="2D",Slider=True,TraceColor='red',FrameColor='blue',Name='',Title='SmithChart_Plot',TitleColor='blue',TitleSize=15)
	#SMITH.Fig_3D.show()

#	SMITH.RF_Check_2D(TraceColor='red', FrameColor='blue', Name='', Title='SmithChart_Plot',TitleColor='blue', TitleSize=15)
	###SMITH.SmithChart_2D(Data='S11',Slider=True,TraceColor='red',FrameColor='red',Name='',Title='SmithChart_Plot',TitleColor='blue',TitleSize=15)
#	###SMITH.AddCircle_2D(Radius=0.6,Center=complex("0.5+0.6j"),Resolution=100, name="")

	# SMITH.SparaTable()
	# SMITH.StabilityTable(ViewPlot=True)
	# SMITH.GainTable(ViewPlot=True)

	#SMITH.PlotlyGraph(plot=True,Size_x=1.5,Size_y=1.5)
