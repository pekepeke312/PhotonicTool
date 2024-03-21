from TextWriter import *
import time
import pandas as pd
import numpy as np
import sympy
import plotly.graph_objs as go

if __name__ != "__main__":
	Toppath = str(pathlib.Path(__file__).parent.resolve())
	PartInfoDatabaseAddress = Toppath + str('\\assets\\UnitConversion.xlsx')
else:
	PartInfoDatabaseAddress = "assets//UnitConversion.xlsx"

DATALENGTH = 1001

class UnitConversion():
	def __init__(self, DebugMode=False):
		# Arguments  ------------------------------------
		self.DatabaseLoader(Path=PartInfoDatabaseAddress)
		self.GraphState = False

	def RemainintParts(self, Category="", From="", To=""):
		if Category != "" and Category != None:
			LimitedCategory = self.DataBase[self.DataBase["Category"] == Category]
		else:
			LimitedCategory = self.DataBase

		if From != "" and From != None:
			LimitedFrom = LimitedCategory[LimitedCategory["From"] == From]
		else:
			LimitedFrom = LimitedCategory

		if To != "" and To != None:
			LimitedList = LimitedFrom[LimitedFrom["To"] == To]
		else:
			LimitedList = LimitedFrom

		# LimitedList = self.DataBase[self.DataBase["Category"] == Category]
		# LimitedList = LimitedList[LimitedList["From"] == From]
		# LimitedList = LimitedList[LimitedList["To"] == To]

		if len(LimitedList) > 1:
			text = fr"Remaining Possible Conditions are {len(LimitedList)} cases"
			print(text)
			TextWriter(text)
			self.GraphState = False
			self.SelectedData = ""
		else:
			text = "Remaining Possible Condition is only 1 case"
			print(text)
			TextWriter(text)
			self.SelectedData = LimitedList
			self.GraphState = True
			self.InputWidgetUpdate() ## Update GUI View
			self.RelationShipGraphGenerator() ## Calling the last one condition.

	def InputWidgetUpdate(self):
		Data = self.SelectedData
		self.SympyParameterList = []
		self.ParamList = []
		try:
			for n, Param in enumerate(str(Data["Input"].values[0]).split(" ")):
				if len(Data.Input.values[0].split(" ")) > 1:
					self.SympyParameterList.append(sympy.symbols(str(Data.Input.values[0]))[n])
				else:
					self.SympyParameterList.append(sympy.symbols(str(Data.Input.values[0])))
				self.ParamList.append(Param)
		except:
			pass

	def InputParameterValueUpdate(self):
		Data = self.SelectedData
		self.Param1_min_value = Data["Default min"]
		self.Param1_max_value = Data["Default max"]
		self.Param2_value = Data["Default Param2"]
		self.Param3_value = Data["Default Param3"]
		self.Param4_value = Data["Default Param4"]
		self.Param5_value = Data["Default Param5"]
		self.Param6_value = Data["Default Param6"]
		self.Param7_value = Data["Default Param7"]
		self.Param8_value = Data["Default Param8"]
		print("")

	def RelationShipGraphGenerator(self, Param1_MAX=100, Param1_MIN=0, Param2="", Param3="", Param4="", Param5="", Param6="", Param7="" , Param8=""):
		self.Fig_2D = go.Figure()

		Param1_MAX = float(Param1_MAX)
		Param1_MIN = float(Param1_MIN)

		try:
			Param2 = float(Param2)
		except:
			Param2 = ""

		try:
			Param3 = float(Param3)
		except:
			Param3 = ""

		try:
			Param4 = float(Param4)
		except:
			Param4 = ""

		try:
			Param5 = float(Param5)
		except:
			Param5 = ""

		try:
			Param6 = float(Param6)
		except:
			Param6 = ""

		try:
			Param7 = float(Param7)
		except:
			Param7 = ""

		try:
			Param8 = float(Param8)
		except:
			Param8 = ""

		Data = self.SelectedData
		P = self.SympyParameterList

		try:
			Y = eval(Data["Sympy Formula"].values[0])

			# Param2
			if Param2:
				Y = Y.subs(P[1], Param2)

			if Param3:
				Y = Y.subs(P[2], Param3)

			if Param4:
				Y = Y.subs(P[3], Param4)

			if Param5:
				Y = Y.subs(P[4], Param5)

			if Param6:
				Y = Y.subs(P[5], Param6)

			if Param7:
				Y = Y.subs(P[6], Param7)

			if Param8:
				Y = Y.subs(P[7], Param8)

			func = sympy.lambdify(P[0], Y)  # , modules="numpy")
		except:
			pass



		if "log" in str(self.SelectedData["X-Axis"]):
			x_vals = np.logspace(np.log10(float(Param1_MIN)), np.log10(float(Param1_MAX)), DATALENGTH)
		else:
			x_vals = np.linspace(float(Param1_MIN), float(Param1_MAX), DATALENGTH)

		try:
			y_vals = func(x_vals)
		except:
			pass

		try:
			CustomData = []
			Converted_x = self.UnitConverter(x_vals,"")
			Converted_y = self.UnitConverter(y_vals,"")
			for n in range(DATALENGTH):
				CustomData.append(
					[Converted_x[0][n], #x_vals[n],
					 Converted_x[1][n], #x-unit
					 Converted_y[0][n], #y_vals[n],
					 Converted_y[1][n],
					 Param2,
					 Param3,
					 Param4,
					 Param5,
					 Param6,
					 Param7,
					 Param8,
					 ]
				)  # for Data
		except:
			pass

		try:
			if y_vals[1].is_Mul:
				return []
		except:
			if len(self.ParamList) == 1:
				text = [f'{self.SelectedData["To"].values[0]}: {y:0.4f}{y_unit}{self.SelectedData["To Unit"].values[0]}'
				 		f'<br>{self.SelectedData["From"].values[0]}: {x:0.4f}{x_unit}{self.SelectedData["From Unit"].values[0]}'
				 		for [x,x_unit, y,y_unit, param2, param3, param4, param5, param6, param7, param8,] in CustomData]

			elif len(self.ParamList) == 2:
				text = [f'{self.SelectedData["To"].values[0]}: {y:0.4f}{y_unit}{self.SelectedData["To Unit"].values[0]}'
				 		f'<br>{self.SelectedData["From"].values[0]}: {x:0.4f}{x_unit}{self.SelectedData["From Unit"].values[0]}'
						f'<br>{self.ParamList[1]}: {param2:0.4f}'
				 		for [x,x_unit, y,y_unit, param2, param3, param4, param5, param6, param7, param8,] in CustomData]

			elif len(self.ParamList) == 3:
				text = [f'{self.SelectedData["To"].values[0]}: {y:0.4f}{y_unit}{self.SelectedData["To Unit"].values[0]}'
				 		f'<br>{self.SelectedData["From"].values[0]}: {x:0.4f}{x_unit}{self.SelectedData["From Unit"].values[0]}'
						f'<br>{self.ParamList[1]}: {param2:0.4f}'
						f'<br>{self.ParamList[2]}: {param3:0.4f}'
						for [x, x_unit, y, y_unit, param2, param3, param4, param5, param6, param7, param8, ] in
						CustomData]

			elif len(self.ParamList) == 4:
				text = [f'{self.SelectedData["To"].values[0]}: {y:0.4f}{y_unit}{self.SelectedData["To Unit"].values[0]}'
						f'<br>{self.SelectedData["From"].values[0]}: {x:0.4f}{x_unit}{self.SelectedData["From Unit"].values[0]}'
						f'<br>{self.ParamList[1]}: {param2:0.4f}'
						f'<br>{self.ParamList[2]}: {param3:0.4f}'
						f'<br>{self.ParamList[3]}: {param4:0.4f}'
						for [x, x_unit, y, y_unit, param2, param3, param4, param5, param6, param7, param8, ] in
						CustomData]

			elif len(self.ParamList) == 5:
				text = [f'{self.SelectedData["To"].values[0]}: {y:0.4f}{y_unit}{self.SelectedData["To Unit"].values[0]}'
						f'<br>{self.SelectedData["From"].values[0]}: {x:0.4f}{x_unit}{self.SelectedData["From Unit"].values[0]}'
						f'<br>{self.ParamList[1]}: {param2:0.4f}'
						f'<br>{self.ParamList[2]}: {param3:0.4f}'
						f'<br>{self.ParamList[3]}: {param4:0.4f}'
						f'<br>{self.ParamList[4]}: {param5:0.4f}'
						for [x, x_unit, y, y_unit, param2, param3, param4, param5, param6, param7, param8, ] in
						CustomData]

			elif len(self.ParamList) == 6:
				text = [f'{self.SelectedData["To"].values[0]}: {y:0.4f}{y_unit}{self.SelectedData["To Unit"].values[0]}'
						f'<br>{self.SelectedData["From"].values[0]}: {x:0.4f}{x_unit}{self.SelectedData["From Unit"].values[0]}'
						f'<br>{self.ParamList[1]}: {param2:0.4f}'
						f'<br>{self.ParamList[2]}: {param3:0.4f}'
						f'<br>{self.ParamList[3]}: {param4:0.4f}'
						f'<br>{self.ParamList[4]}: {param5:0.4f}'
						f'<br>{self.ParamList[5]}: {param6:0.4f}'
						for [x, x_unit, y, y_unit, param2, param3, param4, param5, param6, param7, param8, ] in
						CustomData]

			elif len(self.ParamList) == 7:
				text = [f'{self.SelectedData["To"].values[0]}: {y:0.4f}{y_unit}{self.SelectedData["To Unit"].values[0]}'
						f'<br>{self.SelectedData["From"].values[0]}: {x:0.4f}{x_unit}{self.SelectedData["From Unit"].values[0]}'
						f'<br>{self.ParamList[1]}: {param2:0.4f}'
						f'<br>{self.ParamList[2]}: {param3:0.4f}'
						f'<br>{self.ParamList[3]}: {param4:0.4f}'
						f'<br>{self.ParamList[4]}: {param5:0.4f}'
						f'<br>{self.ParamList[5]}: {param6:0.4f}'
						f'<br>{self.ParamList[6]}: {param7:0.4f}'
						for [x, x_unit, y, y_unit, param2, param3, param4, param5, param6, param7, param8, ] in
						CustomData]

			elif len(self.ParamList) == 8:
				text = [f'{self.SelectedData["To"].values[0]}: {y:0.4f}{y_unit}{self.SelectedData["To Unit"].values[0]}'
						f'<br>{self.SelectedData["From"].values[0]}: {x:0.4f}{x_unit}{self.SelectedData["From Unit"].values[0]}'
						f'<br>{self.ParamList[1]}: {param2:0.4f}'
						f'<br>{self.ParamList[2]}: {param3:0.4f}'
						f'<br>{self.ParamList[3]}: {param4:0.4f}'
						f'<br>{self.ParamList[4]}: {param5:0.4f}'
						f'<br>{self.ParamList[5]}: {param6:0.4f}'
						f'<br>{self.ParamList[6]}: {param7:0.4f}'
						f'<br>{self.ParamList[7]}: {param8:0.4f}'
						for [x, x_unit, y, y_unit, param2, param3, param4, param5, param6, param7, param8, ] in
						CustomData]


			try:
				self.Fig_2D.add_trace(
					go.Scatter(
						x=x_vals,
						y=y_vals,
						hoverinfo='text',
						text=text,
						showlegend=False,
						mode='lines',
						line=dict(width=1.50,
								  # dash='dash',
								  color="blue"),
					)
				)

				self.Fig_2D.update_layout(
					xaxis_title=Data["From"].values[0],
					yaxis_title=Data["To"].values[0],
					autosize=True,
					margin=dict(l=20, r=20, t=150, b=20),
				)

				try:
					self.Fig_2D.update_layout(
						dict(
							title=dict(
								text=self.SelectedData["Latex Formula"].values[0],
								x = 0.5,
								font = dict(
									size = 24,
									color = "black",
								)
							)
						)
					)

					if "log" in str(self.SelectedData["Y-Axis"].values):
						Scale_Y = "log"
					else:
						Scale_Y = None

					self.Fig_2D.update_yaxes(
						type=Scale_Y,
						exponentformat="SI",
					)

					if "log" in str(self.SelectedData["X-Axis"].values):
						Scale_X = "log"
					else:
						Scale_X = None

					self.Fig_2D.update_xaxes(
						type=Scale_X,
						exponentformat="SI",
					)

				except:
					self.Fig_2D.update_layout(
						dict(
							title=dict(
								text='Title is not ready yet',
								x = 0.5,
								font = dict(
									size = 24,
									color = "black",
								)
							)
						)
					)

				return self.Fig_2D
			except:
				pass

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

	def DatabaseLoader(self, Path=""):		# This funtion will create self.DataBase_PM
		starttime = time.time()
		ReadAddress = Path
		print("--- Loading Database File ---")
		TextWriter("--- Loading Database File ---")

		try:
			self.DataBase = pd.read_excel(ReadAddress)
		except:
			self.DataBase = pd.read_excel(ReadAddress, header=None, engine='xlrd', index_col='No')

		self.CategoryListData = []
		for Value in sorted(set(self.DataBase["Category"])):
			self.CategoryListData.append(
				{
					'label': Value,			#Serial Number
					'value': Value,			#Serial Number
				}
			)


		self.FromListData = []
		for Value in sorted(set(self.DataBase["From"])):
			self.FromListData.append(
				{
					'label': Value,			#Serial Number
					'value': Value,			#Serial Number
				}
			)

		self.ToListData = []
		for Value in sorted(set(self.DataBase["To"])):
			self.ToListData.append(
				{
					'label': Value,			#Serial Number
					'value': Value,			#Serial Number
				}
			)



		elapstedtime = time.time() - starttime
		text = 'Loading the all address of Database files Completed in {:.3}s'.format(elapstedtime)
		print(text)
		TextWriter(text)


	def CategoryList(self,To="", From="", Reset=False):

		try:
			if From != "" and From != None:
				LimitedFrom = self.DataBase[self.DataBase["From"] == From]
			else:
				LimitedFrom = self.DataBase
		except:
			LimitedFrom = self.DataBase

		try:
			if To != "" and To != None:
				LimitedTo = LimitedFrom[LimitedFrom["To"] == To]
			else:
				LimitedTo = LimitedFrom
		except:
			LimitedTo = LimitedFrom


		self.CategoryListData = []
		for Value in sorted(set(LimitedTo["Category"])):
			self.CategoryListData.append(
				{
					'label': Value,  # Serial Number
					'value': Value,  # Serial Number
				}
			)

		return self.CategoryListData

	def FromList(self, Category="", To="", Reset=False):
		try:
			if Category != "" and Category != None:
				LimitedCategory = self.DataBase[self.DataBase["Category"] == Category]
			else:
				LimitedCategory = self.DataBase
		except:
			LimitedCategory = self.DataBase

		try:
			if To != "" and To != None:
				LimitedTo = LimitedCategory[LimitedCategory["To"] == To]
			else:
				LimitedTo = LimitedCategory
		except:
			LimitedTo = LimitedCategory

		self.FromListData = []
		for Value in sorted(set(LimitedTo["From"])):
			self.FromListData.append(
				{
					'label': Value,  # Serial Number
					'value': Value,  # Serial Number
				}
			)

		return self.FromListData

	def ToList(self, Category="", From="", Reset=False):
		try:
			if Category != "" and Category != None:
				LimitedCategory = self.DataBase[self.DataBase["Category"] == Category]
			else:
				LimitedCategory = self.DataBase
		except:
			LimitedCategory = self.DataBase

		try:
			if From != "" and From != None:
				LimitedFrom = LimitedCategory[LimitedCategory["From"] == From]
			else:
				LimitedFrom = LimitedCategory
		except:
			LimitedFrom = LimitedCategory

		self.ToListData = []
		for Value in sorted(set(LimitedFrom["To"])):
			self.ToListData.append(
				{
					'label': Value,  # Serial Number
					'value': Value,  # Serial Number
				}
			)

		return self.ToListData


if __name__ == "__main__":
	PSTool = UnitConversion(DebugMode=False)
	PSTool.CategoryList()
	PSTool.ToList()

	# PSTool.Plotly_Table_Generator(SheetFilter='210 - Analog ICs')
	# PSTool.DataBaseTable.show()