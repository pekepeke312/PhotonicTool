import sympy
import plotly.graph_objs as go
import numpy as np
from textwriter import *
import time

from sympy import exp, symbols, pi, sqrt, tanh, Function
from sympy.functions.special.elliptic_integrals import elliptic_k
from scipy.special import ellipk
from sympy import Piecewise, nan

DATALENGTH = 5001

class PCB_Pattern_Width():
    def __init__(self,Width_min,Width_max, Param1, Param2, Param3, Param4, Param5, Mode,): # DebugMode=False):
        self.Width_min = Width_min
        self.Width_max = Width_max
        try:
            self.Param1 = float(Param1)
        except:
            self.Param1 = ""

        try:
            self.Param2 = float(Param2)
        except:
            self.Param2 = ""

        try:
            self.Param3 = float(Param3)
        except:
            self.Param3 = ""

        try:
            self.Param4 = float(Param4)
        except:
            self.Param4 = ""

        try:
            self.Param5 = float(Param5)
        except:
            self.Param5 = ""

        self.Mode = Mode

        # self.GraphState = False
        # self.DebugMode = DebugMode

        self.FormulaDataCreateor()
        self.InputWidgetUpdate()
        # self.FormulaInput()
        self.ParameterOverwrite()
        # self.Graph_Gnerator()


    def FormulaDataCreateor(self):
        self.SelectedData = {}
        if self.Mode == "Microstrip" or self.Mode == "Stripline":
            self.ParamList = ["DC", "t", "h"]

        elif self.Mode == "Asymmetric Stripline":
            self.ParamList = ["DC", "t", "ha", "hb"]

        elif self.Mode == "Embedded Microstrip":
            self.ParamList = ["DC", "t", "h", "hp"]

        elif self.Mode == "Edge Coupled Microstrip" or self.Mode == "Edge Coupled Stripline":
            self.ParamList = ["DC", "t", "h", "S"]

        elif self.Mode == "Broadside Coupled Stripline":
            self.ParamList = ["DC", "t", "hp", "ht"]

        elif self.Mode == "Coplanar Waveguide With Ground":
            self.ParamList = ["DC", "t", "Gap", "h"]

        elif self.Mode == "Asymmetric Coplanar Waveguide":
            self.ParamList = ["DC", "t", "Gap", "ha", "hb"]

    def InputWidgetUpdate(self):
        self.SympyParameterList = []
        try:
            for n, Param in enumerate(self.ParamList):
                self.SympyParameterList.append(sympy.symbols(Param))
        except:
            pass

    def FormulaInput(self):
        P = self.SympyParameterList
        W = sympy.symbols("Width")
        if self.Mode == "Microstrip":
            self.De = sympy.Piecewise(((P[0]+1)/2 + ((P[0]-1)/2) *(1/(sympy.Pow(1+12*(P[2]/W),0.5)) +0.4*sympy.Pow(1-W/P[2],2)),W<P[2]),
                                    ((P[0]+1)/2 + ((P[0]-1)/(2*sympy.Pow(1+12*(P[2]/W),0.5))),W>=P[2]))

            self.Z = sympy.Piecewise((((60/sympy.Pow(self.De,0.5)) * sympy.ln(8*(P[2]/W + 0.25*W/P[2]))),W<P[2]),
                                    ((120*sympy.pi)/(sympy.Pow(self.De,0.5)*((W/P[2])+1.393+(2/3)*sympy.ln(W/P[2] + 1.444))),W>=P[2]))

        elif self.Mode == "Stripline":
            self.Z = 60/sympy.Pow(P[0],0.5) * sympy.ln((1.9*(2*P[2]+P[1]))/(0.8*W + P[1]))

        elif self.Mode == "Asymmetric Stripline":
            self.Z = 80 / sympy.Pow(P[0], 0.5) * sympy.ln((1.9*(2*P[2]+P[1]))/(0.8*W + P[1])) *(1 - P[2]/(4*P[3]))

        elif self.Mode == "Embedded Microstrip":
            # self.De = P[0]*(1-sympy.exp(-1.55*P[2]/P[3]))
            # self.Z = 60 / sympy.Pow(self.De, 0.5) * sympy.ln(5.98*P[3] / (0.8 * W + P[1]))
            # if isinstance(self.Z, sympy.Basic) and self.Z.has(exp):
            #     self.Z = self.Z.replace(exp, Function("exp"))

            self.De = P[0] * (1 - sympy.exp(-1.55 * P[2] / P[3]))
            self.Z = 60 / sympy.sqrt(self.De) * sympy.log(5.98 * P[3] / (0.8 * W + P[1]))

        elif self.Mode == "Edge Coupled Microstrip":
            self.Z = (174/(sympy.Pow(P[0] +1.41, 0.5)))* sympy.ln(5.98*P[3] / (0.8 * W + P[1])) * (1- 0.48 * sympy.exp(-0.96 * P[3]/P[2]))

        elif self.Mode == "Edge Coupled Stripline":
            self.Z = 60/sympy.Pow(P[0],0.5) * sympy.ln((1.9*(2*P[2]+P[1]))/(0.8*W + P[1]))

        elif self.Mode == "Broadside Coupled Stripline":
            self.Z = 80 / sympy.Pow(P[0], 0.5) * sympy.ln((1.9*(2*P[2]+P[1]))/(0.8*W + P[1])) *(1 - P[2]/(4*(P[1]+P[2]+P[3])))

        elif self.Mode == "Coplanar Waveguide With Ground":
            def clip_expr(x, min_val, max_val):
                return sympy.Min(sympy.Max(x, min_val), max_val)

            # tanh_sym = Function('tanh')

            W = sympy.symbols("Width")
            P = self.SympyParameterList
            er = P[0]
            s = P[2]
            h = P[3]
            h_eff = h

            a = W
            b = W + 2 * s
            epsilon = 1e-9

            k = a / b
            kp = sqrt(1 - k ** 2)

            k1 = tanh(pi * a / (4 * h_eff)) / tanh(pi * b / (4 * h_eff))
            k1p = sqrt(1 - k1 ** 2)

            try:
                Kk = elliptic_k(k ** 2)
                Kkp = elliptic_k(kp ** 2)
                Kk1 = elliptic_k(k1 ** 2)
                Kkp1 = elliptic_k(k1p ** 2)

                self.De = (1 + er * (Kkp / Kk) * (Kk1 / Kkp1)) / (1 + (Kkp / Kk) * (Kk1 / Kkp1))
                self.Z = (60 * pi / sqrt(self.De)) / ((Kk / Kkp) + (Kk1 / Kkp1))

                # 🔧 lambdify 用に tanh を安全に変換
                if isinstance(self.Z, sympy.Basic) and "tanh" in str(self.Z):
                    self.Z = self.Z.replace(sympy.tanh, Function("tanh"))
                    self.Z = sympy.simplify(self.Z)
                if isinstance(self.De, sympy.Basic) and "tanh" in str(self.De):
                    self.De = self.De.replace(sympy.tanh, Function("tanh"))

                if self.Z.has(sympy.zoo) or self.Z.has(sympy.oo) or self.Z.has(sympy.nan):
                    raise ValueError("ComplexInfinity detected in expression")

            except Exception as e:
                print("Error in CPW calculation:", e)
                self.Z = nan

            except Exception as e:
                self.Z = sympy.nan
                print("⚠ self.Z 計算中にエラー:", e)

                print("self.Z =", self.Z)
                print("free symbols =", getattr(self.Z, "free_symbols", None))

        elif self.Mode == "Asymmetric Coplanar Waveguide":
            def clip_expr(x, min_val, max_val):
                return sympy.Min(sympy.Max(x, min_val), max_val)
            def safe_replace_expr(expr):
                return expr.replace(sympy.tanh, Function('tanh')).replace(sympy.exp, Function('exp'))

            W = sympy.symbols("Width")
            P = self.SympyParameterList
            er = P[0]
            s = P[2]
            ha = P[3]  # 上側の基板厚み
            hb = P[4]  # 下側の基板厚み
            h_eff = 2 * ha * hb / (ha + hb)  # 有効高さ
            a = W
            b = W + 2 * s
            epsilon = 1e-9

            k = a / b
            kp = sqrt(1 - k ** 2)
            k1 = tanh(pi * a / (4 * h_eff)) / tanh(pi * b / (4 * h_eff))
            k1p = sqrt(1 - k1 ** 2)
            try:
                Kk = elliptic_k(k ** 2)
                Kkp = elliptic_k(kp ** 2)
                Kk1 = elliptic_k(k1 ** 2)
                Kkp1 = elliptic_k(k1p ** 2)

                self.De = (1 + er * (Kkp / Kk) * (Kk1 / Kkp1)) / (1 + (Kkp / Kk) * (Kk1 / Kkp1))
                self.Z = (60 * pi / sqrt(self.De)) / ((Kk / Kkp) + (Kk1 / Kkp1))

                # lambdify 対応のために tanh, exp を Function に変換
                self.Z = self.Z.replace(sympy.tanh, sympy.Function("tanh")).replace(sympy.exp, sympy.Function("exp"))
                if isinstance(self.De, sympy.Basic):
                    self.De = self.De.replace(sympy.tanh, sympy.Function("tanh")).replace(sympy.exp,
                                                                                          sympy.Function("exp"))

                if self.Z.has(sympy.zoo) or self.Z.has(sympy.oo) or self.Z.has(sympy.nan):
                    raise ValueError("ComplexInfinity detected in expression")

            except Exception as e:
                self.Z = sympy.nan
                print("⚠ self.Z 計算中にエラー:", e)
                print("self.Z =", self.Z)
                print("free symbols =", getattr(self.Z, "free_symbols", None))

    def ParameterOverwrite(self):
        P = self.SympyParameterList
        self.FormulaInput()
        if self.Param1:
            self.Z = self.Z.subs(P[0], self.Param1)

        if self.Param2:
            self.Z = self.Z.subs(P[1], self.Param2)

        if self.Param3:
            self.Z = self.Z.subs(P[2], self.Param3)

        try:
            if self.Param4:
                self.Z = self.Z.subs(P[3], self.Param4)
        except:
            pass

        try:
            if self.Param5:
                self.Z = self.Z.subs(P[4], self.Param5)
        except:
            pass
        ## ---------
        try:
            if self.Param1:
                self.De = self.De.subs(P[0], self.Param1)

            if self.Param2:
                self.De = self.De.subs(P[1], self.Param2)

            if self.Param3:
                self.De = self.De.subs(P[2], self.Param3)

            if self.Param4:
                self.De = self.De.subs(P[3], self.Param4)

            if self.Param5:
                self.De = self.De.subs(P[4], self.Param5)
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

    def Graph_Gnerator(self):
        self.Fig_2D = go.Figure()
        W = sympy.symbols("Width")

        try:
            def safe_elliptic_k(x):
                import numpy as np
                from scipy.special import ellipk
                x = np.clip(x, 1e-9, 1 - 1e-9)
                return ellipk(x)

            safe_numpy_funcs = {
                "exp": np.exp,
                "log": np.log,
                "sqrt": np.sqrt,
                "tanh": np.tanh,
                "elliptic_k": safe_elliptic_k
            }

            func = sympy.lambdify(W, self.Z, modules=[safe_numpy_funcs, "numpy"])

        except Exception as e:
            print("lambdify error:", e)
            self.Z = None
            return None

        x_vals = np.logspace(np.log10(self.Width_min), np.log10(self.Width_max), DATALENGTH)
        y_vals = func(x_vals)

        try:
            CustomData = []
            Converted_x = self.UnitConverter(x_vals, "")
            Converted_y = self.UnitConverter(y_vals, "")
            for n in range(DATALENGTH):
                CustomData.append([
                    Converted_x[0][n], Converted_x[1][n],
                    Converted_y[0][n], Converted_y[1][n],
                    self.Param1, self.Param2, self.Param3,
                    self.Param4, self.Param5
                ])
        except:
            pass

        try:
            if y_vals[1].__class__.__name__ == 'Mul':
                return []
        except:
            pass

        try:
            text = []
            if len(self.ParamList) == 3:
                text = [
                    f'Zo: {y:0.4f}{y_unit}[ohm]<br>Width : {x:0.4f}{x_unit}m<br>Dielectric Constant Er: {param1:0.2f}<br>{self.ParamList[1]}: {1e6 * param2:0.4f}um<br>{self.ParamList[2]}: {1000 * param3:0.4f}mm'
                    for [x, x_unit, y, y_unit, param1, param2, param3, param4, param5] in CustomData]
            elif len(self.ParamList) == 4:
                text = [
                    f'Zo: {y:0.4f}{y_unit}[ohm]<br>Width : {x:0.4f}{x_unit}m<br>Dielectric Constant Er: {param1:0.2f}<br>{self.ParamList[1]}: {1e6 * param2:0.4f}um<br>{self.ParamList[2]}: {1000 * param3:0.4f}mm<br>{self.ParamList[3]}: {1000 * param4:0.4f}mm'
                    for [x, x_unit, y, y_unit, param1, param2, param3, param4, param5] in CustomData]
            elif len(self.ParamList) == 5:
                text = [
                    f'Zo: {y:0.4f}{y_unit}[ohm]<br>Width : {x:0.4f}{x_unit}m<br>Dielectric Constant Er: {param1:0.2f}<br>{self.ParamList[1]}: {1e6 * param2:0.4f}um<br>{self.ParamList[2]}: {1000 * param3:0.4f}mm<br>{self.ParamList[3]}: {1000 * param4:0.4f}mm<br>{self.ParamList[4]}: {1000 * param5:0.4f}mm'
                    for [x, x_unit, y, y_unit, param1, param2, param3, param4, param5] in CustomData]
        except:
            text = []

        # Plot main graph
        self.Fig_2D.add_trace(
            go.Scatter(
                x=x_vals,
                y=y_vals,
                hoverinfo='text',
                text=text,
                showlegend=False,
                mode='lines',
                line=dict(width=1.50, color="blue"),
            )
        )

        self.Fig_2D.update_layout(
            xaxis_title="Width (W) [m]",
            yaxis_title="Impedance: Zo [ohm]",
            autosize=True,
            margin=dict(l=20, r=20, t=80, b=20),
            hovermode="x unified",
            yaxis=dict(range=[0, max(y_vals) * 1.1], exponentformat="SI"),
            xaxis=dict(type="log", exponentformat="SI"),
            title=dict(
                text="Width vs Impedance Characteristics",
                x=0.5,
                font=dict(size=20, color="black")
            )
        )

        # ----- ⬇ Highlight 50Ω / 75Ω / 100Ω intersection ⬇ -----
        try:
            from scipy.interpolate import interp1d
            x_log = np.log10(x_vals)
            f_inv = interp1d(y_vals, x_vals, kind='linear', bounds_error=False, fill_value="extrapolate")

            target_impedances = [50, 75, 100]
            colors = ["red", "orange", "green"]

            def find_intersection(x_vals, y_vals, target):
                idx = np.argmin(np.abs(np.array(y_vals) - target))
                return x_vals[idx], y_vals[idx]

            for Z, color in zip(target_impedances, colors):
                x_int, y_int = find_intersection(x_vals, y_vals, Z)

                self.Fig_2D.add_shape(
                    type="line",
                    x0=x_int, x1=x_int,
                    y0=0, y1=Z,
                    line=dict(color=color, dash="dot", width=2),
                )

                self.Fig_2D.add_annotation(
                    x=x_int,
                    y=Z,
                    text=f"{Z}Ω<br>{x_int * 1000:.3f} mm",
                    showarrow=True,
                    arrowhead=3,
                    ax=40,
                    ay=-40,
                    font=dict(color=color, size=12),
                    bordercolor=color,
                    borderwidth=1,
                    bgcolor="white",
                )
        except Exception as e:
            print("⚠ 交点描画エラー:", e)

        return self.Fig_2D


if __name__ == "__main__":
    Param1 = 4.78
    Param2 = 33.02e-6
    Param3 = 0.0016
    Param4 = ""
    Width = 0.001

    PCB = PCB_Pattern_Width(Param1=Param1, Param2=Param2, Param3=Param3, Param4=Param4, Mode="Microstrip") #,DebugMode=False,)
    De = PCB.De
    Zo = PCB.Z

    print(f'Ee= {De.subs("Width", Width)}')
    print(f'Zo= {Zo.subs("Width",Width)}')

    #     if self.Mode == "Microstrip":
    #
    #
    #         Y = Y.subs(P[1], Param1)
    #
    #        self.Df_Low_func = sympy.lambdify(P[0], Y)
    #         sympy.Piecewise(
    #             (66, (P[0] > 0.15 * sympy.Pow(10, 6)) & (P[0] < 0.5 * sympy.Pow(10, 6))),
    #             (60, (P[0] >= 0.5 * sympy.Pow(10, 6)) & (P[0] < 30 * sympy.Pow(10, 6))),
    #         )
