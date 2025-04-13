import plotly.graph_objs as go
import numpy as np
import skrf as rf
from typing import Union
import time
import math

from textwriter import textwriter

VSWR = GAMMA = RL = ML_dB = ML_P = RSource = RLoad = ''
VSWR_ABS = GAMMA_ABS = ''

class smithchart:
    #def __init__(self, Z=50):
        #self.Fig_2D = go.Figure()
        #self.PlotlyGraph(Size_x=1, Size_y=1, plot=False)

    def UVtoG(self, UVList):
        if len([UVList]) > 1:
            list = []
            for n in UVList:
                [U, V] = n
                base = pow(U,2) - 2*U + pow(V,2) +1
                re = -1* (pow(U,2) + pow(V,2) - 1) / base
                imag = (2*V)/base
                list.append(complex(re+imag*1.0j))
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

    def AddCircle_2D(self, Radius=0, Center:[complex]="", Resolution=100, color="red", name=""):
        #re=Center.real
        #img=Center.imag
        r = Radius
        if name == "":
            name = 'R=' + str(round(r,4)) + ' Center=' + str(Center)

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
            for img in np.linspace(-100, 100, 2000, endpoint=False):
                [U,V] = self.GtoUV(r + 1j*img)
                Circle_U.append(U)
                Circle_V.append(V)

        ## Constant Imaginary line, Impedance
        for img in Constantlist2:
            for r in np.linspace(100, 0, 300, endpoint=False):
                [U,V] = self.GtoUV(r+1j*img)
                Imp_U.append(U)
                Imp_V.append(V)
            for r in np.linspace(0, 100, 300, endpoint=False):
                [U,V] = self.GtoUV(r+1j*img)
                Imp_U.append(U)
                Imp_V.append(V)

        ## Constant Imaginary line, Admittance
        for img in Constantlist3:
            for r in np.linspace(100, 0, 300, endpoint=False):
                [U,V] = self.GtoUV(1/(r+1j*img))
                Adm_U.append(U)
                Adm_V.append(V)
            for r in np.linspace(0, 100, 300, endpoint=False):
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
                    color= "aqua"),
            ),
        ),

        self.Fig_2D.add_trace(
            go.Scatter(
                x=[-1.05,-1.04,-0.66, 0, 0.62, 1, 1.05,
                   -1.04,-0.7,0,0.62, 0.98,
                    -0.66,-0.33,0,0.33,0.67],
                y=[-0.05,0.38,0.81, 1.02, 0.81,0.38,-0.05,
                    -0.45,-0.9,-1.1, -0.9,-0.47,
                    -0.02,-0.02,-0.02,-0.02,-0.02],
                text=["0", "+0.2j", "+0.5j", "+1j","+2j","+5j","\u221e",
                    "-0.2j","-0.5j","-1j","-2j","-5j",
                    "0.2","0.5","1","2","5"],
                mode = 'text',
                showlegend = False,
                hoverinfo='skip',
                textposition="top center",
                textfont=dict(
                    size=15,
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

        self.Fig_2D.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
        )

        if plot == True:
            self.Fig_2D.show()

        elapstedtime = time.time() - starttime
        # print("Making Smithchart Template Completed in {:.3}s".format(elapstedtime))
        # textwriter("Making Smithchart Template Completed in {:.3}s".format(elapstedtime))

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

    def DrawingGraph(self,Zo=50,Rs=complex(50-50j),Rl=complex(100+100j),Gamma_ABS=1/3,Gamma=""):
        starttime = time.time()

        self.Fig_2D = go.Figure()
        self.PlotlyGraph(plot=False)
        Zo = float(Zo)
        Gamma = complex(Gamma)
        [Rs_U,Rs_V] = self.GtoUV(complex(Rs/Zo))
        [Rl_U,Rl_V] = self.GtoUV(complex(Rl/Zo))
        [Rs_UC,Rs_VC] = self.GtoUV(complex(Rs.conjugate()/Zo))

        #### Trace #1
        name = '|Γ|=' + str(round(Gamma_ABS,4)) + ' Center=' + str(Rl)
        self.AddCircle_2D(Radius=Gamma_ABS,Center=complex(Rl/Zo), name=name)

        #### Trace #2
        try:
            Angle = math.atan(Gamma.imag/Gamma.real) * 180 / math.pi
        except:
            Angle = 0

        Gamma_ABS = str(round(Gamma_ABS,4))
        Gamma = str(round(Gamma.real,4) +1j*round(Gamma.imag,4))[1:][:-1]

        self.Fig_2D.add_trace(
            go.Scatter(
                x=[Rs_UC,Rl_U],
                y=[Rs_VC,Rl_V],
                text=[f'Γ={Gamma}:{str(Gamma_ABS) +"∠" + str(round(Angle,4))}\u00B0'],
                hoverinfo='text',
                mode='lines',
                line=dict(color='brown'),
                name=f'Γ={Gamma}:{str(Gamma_ABS) +"∠" + str(round(Angle,4))}\u00B0',
            )
        )

        ### Trace #3
        self.Fig_2D.add_trace(
            go.Scatter(
                x=[Rs_U],
                y=[Rs_V],
                text=[f'U(Re): {Rs.real/Zo:0.4f}<br>V(Img): {Rs.imag/Zo:0.4f}j<br>---------------------<br>Re: {Rs.real:0.4f}<br>Img: {Rs.imag:0.4f}'],
                hoverinfo='text',
                marker=dict(size=10),
                showlegend=True,
                line=dict(color='blue'),
                name='Source: {}'.format(Rs)
            ),
        ),

        ### Trace #4
        self.Fig_2D.add_trace(
            go.Scatter(
                x=[Rs_UC],
                y=[Rs_VC],
                text=[f'U(Re): {Rs.real/Zo:0.4f}<br>V(Img): {Rs.conjugate().imag/Zo:0.4f}j<br>---------------------<br>Re: {Rs.real:0.4f}<br>Img: {Rs.conjugate().imag:0.4f}'],
                hoverinfo='text',
                marker=dict(size=10),
                showlegend=True,
                line=dict(color='purple'),
                name='*Source: {}'.format(Rs.conjugate())
            ),
        ),

        #Trace #5
        self.Fig_2D.add_trace(
            go.Scatter(
                x=[Rl_U],
                y=[Rl_V],
                text=[f'U(Re): {Rl.real/Zo:0.4f}<br>V(Img): {Rl.imag/Zo:0.4f}j<br>---------------------<br>Re: {Rl.real:0.4f}<br>Img: {Rl.imag:0.4f}'],
                hoverinfo='text',
                marker=dict(size=10),
                showlegend=True,
                line=dict(color='green'),
                name='Load: {}'.format(Rl)
            ),
        ),

        elapstedtime = time.time() - starttime
        print("Making Smithchart Completed in {:.3}s".format(elapstedtime))
        textwriter("Making Smithchart Completed in {:.3}s".format(elapstedtime))

# if __name__ == "__main__":
# 	SMITH = smith(path=path)
