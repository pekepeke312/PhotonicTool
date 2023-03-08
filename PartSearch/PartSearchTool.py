import pandas as pd
import numpy as np
import re
import pathlib
from TextWriter import *
import plotly.graph_objects as go
import time
from math import nan, isnan
from dash import dcc
import os

if __name__ != "__main__":
	Toppath = str(pathlib.Path(__file__).parent.resolve())
	PartInfoDatabaseAddress = Toppath + str('\\assets\\PartInfoDatabaseAddress.xlsx')
	#PATH = "PowerModuleCheck//assets//DatabaseLink.xlsx"
else:
	PartInfoDatabaseAddress = "assets//PartInfoDatabaseAddress.xlsx"

SEARCHRANGE=10

class PartSearchTool():
	def __init__(self, DebugMode=False):
		# Arguments  ------------------------------------
		self.DatabaseLoader(Path=PartInfoDatabaseAddress)
		self.PartNumberFileLoader()
		self.AddressFilesTable()
		self.MakingDDTableData()

	def DatabaseLoader(self,Path=""):		# This funtion will create self.DataBase_PM
		starttime = time.time()
		ReadAddress = Path
		print("--- Loading PartInformation File ---")
		TextWriter("--- Loading PartInformation File ---")

		try:
			self.DataBaseAddress = pd.read_excel(ReadAddress)
		except:
			self.DataBaseAddress = pd.read_excel(ReadAddress, header=None, engine='xlrd', index_col='Computer Name')

		self.DataBase={}
		for index, _ in enumerate(self.DataBaseAddress["No"]):
			# PN = int(PN)
			# PN = str(PN)
			try:
				self.DataBase = {
					"File Name": str(self.DataBaseAddress[self.DataBaseAddress["Computer Name"] == os.environ['COMPUTERNAME']]["File Name"].values[0]),
					"Address": self.DataBaseAddress[self.DataBaseAddress["Computer Name"] == os.environ['COMPUTERNAME']]['File Location'].values[0]

				}
			except:
				text = r'PartInfoDatabaseAddress needs to implement this computer setting'
				print(text)
				TextWriter(text)
				raise Exception("PartInfoDatabaseAddress needs to implement this computer setting")


		string = 'Loading from ' + str(self.DataBase["Address"]) + '" started'
		print(string)
		TextWriter(string)

		elapstedtime = time.time() - starttime
		text = 'Loading the all address of Database files Completed in {:.3}s'.format(elapstedtime)
		print(text)
		TextWriter(text)

	def AddressFilesTable(self):
		starttime = time.time()
		HeaderList = list(self.DataBaseAddress.columns)
		#title = "Supporting Power Modules and Link Address"
		DatabaseTableData = []
		for i in range(len(self.DataBaseAddress)):
			try:
				DatabaseTableData.append(
					(
						self.DataBaseAddress[self.DataBaseAddress.columns[0]][i],			#1st Column
						self.DataBaseAddress[self.DataBaseAddress.columns[1]][i],			#2nd Column
						self.DataBaseAddress[self.DataBaseAddress.columns[2]][i],			#3rd Column
						self.DataBaseAddress[self.DataBaseAddress.columns[3]][i],			#4th Column
					)
				)
			except:
				pass
		SwitchedDataBaseTable = np.array(DatabaseTableData).T
		self.DataBaseTable = go.Figure()
		self.DataBaseTable.add_trace(
			go.Table(
				header=dict(
					values=HeaderList,
					line_color='darkslategray',
					fill_color='royalblue',
					align='center',
					font=dict(color='white',size=20),
					height=30,
				),
				cells=dict(
					values=SwitchedDataBaseTable,
					line_color='darkslategray',
					fill_color='white',
					align='center',
					font=dict(color='black', size=18),
					height=25,
				),
				columnwidth = [25,150,150,500]
			)
		)
		self.DataBaseTable.update_layout(
			dict(
				margin=dict(
					l=20,
					r=20,
				),
			)
		)
		elapstedtime = time.time() - starttime
		text = 'Making Address files table Completed in {:.3}s'.format(elapstedtime)
		print(text)
		TextWriter(text)

	def PartNumberFileLoader(self):
		ExcelRaw = pd.read_excel(self.DataBase["Address"], sheet_name=None, header=None)

		## Finding Valid Sheet Names ------------------
		L_Valid_Sheet_Names = []
		for Value in ExcelRaw.keys():
			if(re.search(r'\d{2}', Value)):
				L_Valid_Sheet_Names.append(Value)

		## Making Database -----------------
		self.PartNumberDatabase = []

		# ## Making Headers ------

		starttime = time.time()
		for Sheet in L_Valid_Sheet_Names:
			for n in range(len(ExcelRaw[Sheet].values)):

				for k in range(len(ExcelRaw[Sheet].values[n,:])):
					if ExcelRaw[Sheet].values[n,k] == ("7-digit PN"):
						Column_PartNumber = k

					elif ExcelRaw[Sheet].values[n,k] == ("Description"):
						Column_Description = k

					elif ExcelRaw[Sheet].values[n,k] == ("Class Code"):
						Column_ClassCode = k

					try:
						if (ExcelRaw[Sheet].values[n,k] == "Mfg1") or (ExcelRaw[Sheet].values[n,k] == "Manufacturer") or (ExcelRaw[Sheet].values[n,k] == "Manufacturer/Vendor"):
							Column_Manufacturer = k
					except:
							Column_Manufacturer = nan

					try:
						if (ExcelRaw[Sheet].values[n,k] == "Mfg1 PN") or (ExcelRaw[Sheet].values[n,k] == "Manufacturer PN"):
							Column_ManufacturerPN = k
					except:
							Column_ManufacturerPN = nan

					try:
						if (ExcelRaw[Sheet].values[n,k] == "Supplier") or (ExcelRaw[Sheet].values[n,k] == "SUPPLIER"):
							Column_Supplier = k
					except:
							Column_Supplier = nan

					try:
						if (ExcelRaw[Sheet].values[n,k] == "Supplier PN") or (ExcelRaw[Sheet].values[n,k] == "SUPPLIER PN"):
							Column_SupplierPN = k
					except:
							Column_SupplierPN = nan

					try:
						if (ExcelRaw[Sheet].values[n,k] == "URL"):
							Column_URL = k
					except:
							Column_URL = nan

					try:
						if (ExcelRaw[Sheet].values[n,k] == "Type"):
							Column_Type = k
					except:
							Column_Type = nan

					try:
						if (ExcelRaw[Sheet].values[n,k] == "Value"):
							Column_Value = k
					except:
							Column_Value = nan

					try:
						if (ExcelRaw[Sheet].values[n,k] == "Tolerance"):
							Column_Tolerance = k
					except:
							Column_Tolerance = nan

					try:
						if (ExcelRaw[Sheet].values[n,k] == "Size"):
							Column_Size = k
					except:
							Column_Size = nan

					try:
						if (ExcelRaw[Sheet].values[n,k] == "Rating"):
							Column_Rating = k
					except:
							Column_Rating = nan

					try:
						if (ExcelRaw[Sheet].values[n,k] == "Operating Temp"):
							Column_Temp = k
					except:
							Column_Temp = nan

					try:
						if (ExcelRaw[Sheet].values[n,k] == "Lib SCH"):
							Column_LibSCH = k
					except:
							Column_LibSCH = nan

					try:
						if (ExcelRaw[Sheet].values[n,k] == "Lib PCB"):
							Column_LibPCB = k
					except:
							Column_LibPCB = nan

			for n in range(1,len(ExcelRaw[Sheet].values)):
				try:
					PartNumber = ExcelRaw[Sheet].values[n,Column_PartNumber]
				except:
					print()

				ClassCode = ExcelRaw[Sheet].values[n,Column_ClassCode]
				Description = ExcelRaw[Sheet].values[n,Column_Description]
				try:
					Manufacturer = ExcelRaw[Sheet].values[n,Column_Manufacturer]
				except:
					Manufacturer = ""

				try:
					ManufacturerPN = ExcelRaw[Sheet].values[n,Column_ManufacturerPN]
				except:
					ManufacturerPN = ""

				try:
					Supplier = ExcelRaw[Sheet].values[n,Column_Supplier]
				except:
					Supplier = ""

				try:
					SupplierPN = ExcelRaw[Sheet].values[n,Column_SupplierPN]
				except:
					SupplierPN = ""

				try:
					URL = ExcelRaw[Sheet].values[n,Column_URL]
				except:
					URL = ""

				try:
					Type = ExcelRaw[Sheet].values[n,Column_Type]
				except:
					Type = ""

				try:
					Value = ExcelRaw[Sheet].values[n,Column_Value]
				except:
					Value = ""

				try:
					Tolerance = ExcelRaw[Sheet].values[n,Column_Tolerance]
				except:
					Tolerance = ""

				try:
					Size = ExcelRaw[Sheet].values[n,Column_Size]
				except:
					Size = ""

				try:
					Rating = ExcelRaw[Sheet].values[n,Column_Rating]
				except:
					Rating = ""

				try:
					Temp = ExcelRaw[Sheet].values[n,Column_Temp]
				except:
					Temp = ""

				try:
					LibSCH = ExcelRaw[Sheet].values[n,Column_LibSCH]
				except:
					LibSCH = ""

				try:
					LibPCB = ExcelRaw[Sheet].values[n,Column_LibPCB]
				except:
					LibPCB = ""


				if (ClassCode != "Class Code") and ( Description != "Description"):
					self.PartNumberDatabase.append(
						(
							ClassCode,
							Sheet,
							PartNumber,
							Description,
							Manufacturer,
							ManufacturerPN,
							Type,
							Value,
							Tolerance,
							Size,
							Rating,
							Temp,
							LibSCH,
							LibPCB,
							# Supplier,
							# SupplierPN,
							URL,
						)
					)

				try:
					if (ExcelRaw[Sheet].values[n, k] == "Lib PCB"):
						Column_LibPCB = k
				except:
					Column_LibPCB = nan

			Column_PartNumber = nan
			Column_Description = nan
			Column_ClassCode = nan
			Column_Manufacturer = nan
			Column_ManufacturerPN = nan
			Column_Supplier = nan
			Column_SupplierPN = nan
			Column_URL = nan
			Column_Type = nan
			Column_Value = nan
			Column_Tolerance = nan
			Column_Size = nan
			Column_Rating = nan
			Column_Temp = nan
			Column_LibSCH = nan



		elapstedtime = time.time() - starttime
		text = 'Loading  Completed in {:.3}s'.format(elapstedtime)
		print(text)
		TextWriter(text)

		self.DF_PartDataBase =pd.DataFrame(self.PartNumberDatabase, dtype='str')
		self.DF_PartDataBase.columns = ["ClassCode",
										"Sheet",
										"PartNumber",
										"Description",
										"Manufacturer",
										"Manufacturer PN",
										"Type",
										"Value",
										"Tolerance",
										"Size",
										"Rating",
										"Temperature",
										"Lib SCH",
										"Lib PCB",
										# "Supplier",
										# "Supplier PN",
										"URL"
										]

	def MakingDDTableData(self):
		self.DD_SheetNames = []
		self.DD_SheetNames.append(
			dict(
				label = 'All',
				value = 'All'
			)
		)
		SheetNameList = sorted(set(self.DF_PartDataBase["Sheet"]))

		for n,name in enumerate(SheetNameList):
			self.DD_SheetNames.append(
				dict(
					label = name,
					value = name,
				)
			)
		# print("")

	def Plotly_Table_Generator(self, SheetFilter=""):
		viewtext = '--- Making Table, [Class Code = ' + str(SheetFilter) + '] ---'
		print(viewtext)
		TextWriter(viewtext)

		### Filter Process ###
		if SheetFilter != '':
			Condition = 'Sheet == "'+ SheetFilter + '"'
			CheckDataBase = self.DF_PartDataBase.query(Condition)
		else:
			CheckDataBase = self.DF_PartDataBase

		# Columnwidth = 10
		title = "Table of Filtered Items (Filter=" + str(SheetFilter) + ")"
		HeaderList = ["ClassCode",
										"Sheet",
										"PartNumber",
										"Description",
										"Manufacturer",
										"Manufacturer PN",
										"Type",
										"Value",
										"Tolerance",
										"Size",
										"Rating",
										"Temperature",
										"Lib SCH",
										"Lib PCB",
										# "Supplier",
										# "Supplier PN",
										"URL"
										]

		#### Making a result DataFrame for dash table ####
		# self.Searched_Result_Table_df = pd.DataFrame(list(CheckDataBase), columns=HeaderList)
		CheckDataBase = CheckDataBase.query('PartNumber != "nan"')
		CheckDataBase = CheckDataBase.query('PartNumber != "-0000"')
		CheckDataBase = CheckDataBase.reindex()
		for n in reversed(range(len(CheckDataBase['PartNumber']))):
			try:
				if type(CheckDataBase['PartNumber'][n]) == float:
					CheckDataBase['PartNumber'].drop(index=n)
			except:
				pass

		self.Searched_Result_Table_df = CheckDataBase


	def Export_Searched_Table(self, Data):
		# data = dcc.send_data_frame(self.Searched_Result_Table_df.to_excel, "Table.xlsx")
		df = pd.DataFrame(Data)
		data = dcc.send_data_frame(df.to_excel, "Table.xlsx")

		return data



if __name__ == "__main__":
	PSTool = PartSearchTool(DebugMode=False)
	PSTool.Plotly_Table_Generator(SheetFilter='210 - Analog ICs')
	PSTool.DataBaseTable.show()