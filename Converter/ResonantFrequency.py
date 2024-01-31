import plotly.graph_objs as go
import numpy as np
import math
from TextWriter import TextWriter

VERTICALRANGE = [np.log10(1e-3), np.log10(6.1e6)]

class ResonantFrequency:
    def __init__(self):
        self.MakingFrequencyDomainGraph(FreqRange=[100,10e9],Plot=False)


    def MakingFrequencyDomainGraph(self, FreqRange, Plot=False):
        self.Fig_2D = go.Figure()
        self.FreqRange = np.array(FreqRange)
        FrequencyList = np.logspace(start=np.log10(FreqRange[0]), stop=np.log10(FreqRange[1]), num=2, base=10)

        # tickvals = []
        # # ticktext = []
        # for digit in range(int(np.log10(FreqRange[0])),int(np.log10(FreqRange[1]))):
        #     for n in range(1,10):
        #         tickvals.append(pow(10, digit) * n)
                # if n == 1:
                #     ticktext.append(str(pow(10,digit)))
                # else:
                #     ticktext.append("")


        # tickvals = np.concatenate((np.logspace(start=np.log10(FreqRange[0]), stop=np.log10(FreqRange[1]), num=int(10* np.log10(FreqRange[1])/np.log10(FreqRange[0]), base=10)))
        # ticktext = [str(val) if val in FrequencyList else '' for val in tickvals]
        # fig.update_xaxes(type="log", tickvals=tickvals, ticktext=ticktext)

        #### Inductors Line #####
        Inductance_List =np.logspace(start=-11, stop=0, num=12, base=10)
        for Inductance in Inductance_List:
            self.Fig_2D.add_trace(
                go.Scatter(
                    x=FrequencyList,
                    y=2 * math.pi * FrequencyList * Inductance,
                    hoverinfo='skip',
                    text=[f'Trace:{Inductance}'],
                    showlegend = False,
                    mode='lines',
                    line=dict(width=1.50,
                          # dash='dash',
                          color="blue"),
                )
            )

            #### Capacitors Line #####
            Capacitance_List = np.logspace(start=-12, stop=-1, num=12, base=10)
            # Capacitance_List_x5 = Capacitance_List*5
            for Capacitance in Capacitance_List:
                self.Fig_2D.add_trace(
                    go.Scatter(
                        x=FrequencyList,
                        y=1/ (2 * math.pi * FrequencyList * Capacitance),
                        hoverinfo='skip',
                        text=[f'Trace:{Capacitance}'],
                        showlegend=False,
                        mode='lines',
                        line=dict(width=1.50,
                                  # dash='dash',
                                  color="orange"),
                    )
                )

                # for times in range(2,10):
                #     Capacitance_list_lowerdigit = Capacitance_List * times
                #
                #     if times != 5:
                #         for Capacitance_lowerdigit in Capacitance_list_lowerdigit:
                #             self.Fig_2D.add_trace(
                #                 go.Scatter(
                #                     x=FrequencyList,
                #                     y=1 / (2 * math.pi * FrequencyList * Capacitance_lowerdigit),
                #                     hoverinfo='skip',
                #                     text=[f'Trace:{Capacitance}'],
                #                     showlegend=False,
                #                     mode='lines',
                #                     line=dict(width=0.75,
                #                               dash='dot',
                #                               color="orange"),
                #                 )
                #             )
                #
                #     else:
                #         for Capacitance_lowerdigit in Capacitance_list_lowerdigit:
                #             self.Fig_2D.add_trace(
                #             go.Scatter(
                #                     x=FrequencyList,
                #                     y=1 / (2 * math.pi * FrequencyList * Capacitance_lowerdigit),
                #                     hoverinfo='skip',
                #                     text=[f'Trace:{Capacitance}'],
                #                     showlegend=False,
                #                     mode='lines',
                #                     line=dict(width=0.5,
                #                               dash='solid',
                #                               color="orange"),
                #                 )
                #             )


            self.Fig_2D.update_yaxes(type="log",
                                     # scaleanchor="x",
                                     scaleratio=1,
                                     range=VERTICALRANGE,
                                     exponentformat="SI",
                                     )
            self.Fig_2D.update_xaxes(type="log",
                                     range=[np.log10(FreqRange[0]), np.log10(FreqRange[1])],
                                     exponentformat="SI",
                                     tickformat = '0.1s',
                                     dtick = "D1",
                                     tickangle = -90,
                                     # automargin = True,
                                     )
        self.AddingAnnotation()

        if __name__ == "__main__":
            self.Fig_2D.update_layout(
                title= dict(
                    text = "Frequency vs Impedance",
                    x = 0.5,
                ),
                xaxis_title="Frequency [Hz]",
                yaxis_title="|Z| [ohm]",
                xaxis={'automargin': True},
            )
        else:
            self.Fig_2D.update_layout(
                xaxis_title="Frequency [Hz]",
                yaxis_title="|Z| [ohm]",
                xaxis={'automargin': True},
                margin=dict(
                    l=10,
                    r=10,
                    b=10,
                    t=10,
                    pad=4
                ),
            )

        if Plot:
            self.Fig_2D.show()

    def AddingAnnotation(self):
        ### Inductance ####
        TEXTANGLE = -25
        self.Fig_2D.add_annotation(
                text="1[H]",
                xref="x", yref="y",
                x=5.25, y=6.2,
                showarrow=False,
                textangle=TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="Blue"
                ),
        )

        self.Fig_2D.add_annotation(
                text="100[mH]",
                xref="x", yref="y",
                x=6.25, y=6.2,
                showarrow=False,
                textangle=TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="Blue"
                ),
        )

        self.Fig_2D.add_annotation(
                text="10[mH]",
                xref="x", yref="y",
                x=7.25, y=6.2,
                showarrow=False,
                textangle=TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="Blue"
                ),
        )

        self.Fig_2D.add_annotation(
                text="1[mH]",
                xref="x", yref="y",
                x=8.25, y=6.2,
                showarrow=False,
                textangle=TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="Blue"
            ),
        )

        self.Fig_2D.add_annotation(
                text="100[\u03BCH]",
                xref="x", yref="y",
                x=9.25, y=6.2,
                showarrow=False,
                textangle=TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="Blue"
                ),
            )

        self.Fig_2D.add_annotation(
                text="10[\u03BCH]",
                xref="x", yref="y",
                x=9.8, y=5.75,
                showarrow=False,
                textangle=TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="Blue"
                ),
        )

        self.Fig_2D.add_annotation(
                text="1[\u03BCH]",
                xref="x", yref="y",
                x=9.8, y=4.75,
                showarrow=False,
                textangle=TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="Blue"
                ),
        )

        self.Fig_2D.add_annotation(
                text="100[nH]",
                xref="x", yref="y",
                x=9.8, y=3.75,
                showarrow=False,
                textangle=TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="Blue"
                ),
        )

        self.Fig_2D.add_annotation(
                text="10[nH]",
                xref="x", yref="y",
                x=9.8, y=2.75,
                showarrow=False,
                textangle=TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="Blue"
                ),
        )

        self.Fig_2D.add_annotation(
                text="1[nH]",
                xref="x", yref="y",
                x=9.8, y=1.75,
                showarrow=False,
                textangle=TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="Blue"
                ),
        )

        self.Fig_2D.add_annotation(
                text="100[pH]",
                xref="x", yref="y",
                x=9.8, y=0.75,
                showarrow=False,
                textangle=TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="Blue"
                ),
        )

        self.Fig_2D.add_annotation(
                text="10[pH]",
                xref="x", yref="y",
                x=9.8, y=-0.25,
                showarrow=False,
                textangle=TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="Blue"
                ),
        )
        ### Capacitance ####
        self.Fig_2D.add_annotation(
                text="1[pF]",
                xref="x", yref="y",
                x=9.5, y=1.9,
                showarrow=False,
                textangle=-1*TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="orange"
                ),
        )

        self.Fig_2D.add_annotation(
                text="10[pF]",
                xref="x", yref="y",
                x=9.5, y=0.9,
                showarrow=False,
                textangle=-1*TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="orange"
                ),
        )

        self.Fig_2D.add_annotation(
                text="100[pF]",
                xref="x", yref="y",
                x=9.5, y=-0.1,
                showarrow=False,
                textangle=-1*TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="orange"
                ),
        )
        self.Fig_2D.add_annotation(
                text="1[nF]",
                xref="x", yref="y",
                x=9.5, y=-1.1,
                showarrow=False,
                textangle=-1*TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="orange"
                ),
        )
        self.Fig_2D.add_annotation(
                text="10[nF]",
                xref="x", yref="y",
                x=9.5, y=-2.1,
                showarrow=False,
                textangle=-1*TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="orange"
                ),
        )
        self.Fig_2D.add_annotation(
                text="100[nF]",
                xref="x", yref="y",
                x=9.0, y=-2.6,
                showarrow=False,
                textangle=-1*TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="orange"
                ),
        )

        self.Fig_2D.add_annotation(
                text="1[\u03BCF]",
                xref="x", yref="y",
                x=8.0, y=-2.6,
                showarrow=False,
                textangle=-1*TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="orange"
                ),
        )

        self.Fig_2D.add_annotation(
                text="10[\u03BCF]",
                xref="x", yref="y",
                x=7.0, y=-2.6,
                showarrow=False,
                textangle=-1*TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="orange"
                ),
        )

        self.Fig_2D.add_annotation(
                text="100[\u03BCF]",
                xref="x", yref="y",
                x=6.0, y=-2.6,
                showarrow=False,
                textangle=-1*TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="orange"
                ),
        )
        self.Fig_2D.add_annotation(
                text="1[mF]",
                xref="x", yref="y",
                x=5.0, y=-2.6,
                showarrow=False,
                textangle=-1*TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="orange"
                ),
        )

        self.Fig_2D.add_annotation(
                text="10[mF]",
                xref="x", yref="y",
                x=4.0, y=-2.6,
                showarrow=False,
                textangle=-1*TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="orange"
                ),
        )

        self.Fig_2D.add_annotation(
                text="100[mF]",
                xref="x", yref="y",
                x=3.0, y=-2.6,
                showarrow=False,
                textangle=-1*TEXTANGLE,
                font=dict(
                    family="sans serif",
                    size=16,
                    color="orange"
                ),
        )

    def CapaciantceCalculator(self, ResonantFrequency, Resonant_Frequency_Unit, ChipInductance):
        n = 1 / (pow((2 * math.pi * float(ResonantFrequency) * float(Resonant_Frequency_Unit)), 2) * float(ChipInductance))

        Digits = 4

        if n >= pow(10, -15) and n < (pow(10, -12)):
            Cap = round(n / pow(10, -15), Digits)
            Unit = 'f'

        elif n >= pow(10, -12) and n < (pow(10, -9)):
            Cap = round(n / pow(10, -12), Digits)
            Unit = 'p'

        elif n >= pow(10, -9) and n < (pow(10, -6)):
             Cap =round(n / pow(10, -9), Digits)
             Unit ='n'

        elif n >= pow(10, -6) and n < (pow(10, -3)):
             Cap = round(n / pow(10, -6), Digits)
             Unit = "u"

        elif n >= pow(10, -3) and n < (pow(10, 0)):
             Cap = round(n / pow(10, -3), Digits)
             Unit = 'm'

        return [Cap, Unit]

    def FindingResonant(self, ResonantFrequency,Resonant_Frequency_Unit, ChipInductance):
        text = (f"Line added, Vertical Line: {ResonantFrequency} x {Resonant_Frequency_Unit} Hz, Slash Line: {ChipInductance} H")
        print(text)
        TextWriter(text)

        [Cap, Unit] = self.CapaciantceCalculator(ResonantFrequency,Resonant_Frequency_Unit,ChipInductance)

        text2 = (f"Suitable Capacitance Value : {Cap} {Unit}F")
        print(text2)
        TextWriter(text2)

        GraphTemplate = self.Fig_2D

        GraphTemplate.add_trace(
            go.Scatter(
                x=self.FreqRange,
                y=2 * math.pi * self.FreqRange * float(ChipInductance),
                # hoverinfo='skip',
                text=[f'Trace:{ChipInductance}'],
                showlegend=False,
                mode='lines',
                line=dict(width=3,
                          # dash='dash',
                          color="red"),
            )
        )

        GraphTemplate.add_trace(
            go.Scatter(
                x=np.array([float(ResonantFrequency),float(ResonantFrequency)]) * float(Resonant_Frequency_Unit),
                y=[pow(10,VERTICALRANGE[0]),pow(10,VERTICALRANGE[1])],
                hoverinfo="text",
                text=[f'Frequency:{ResonantFrequency}'],
                showlegend=False,
                mode='lines',
                line=dict(width=3,
                          # dash='dash',
                          color="red"),
            )
        )
        return GraphTemplate


if __name__ == "__main__":
    Resonant = ResonantFrequency()
    # Resonant.MakingFrequencyDomainGraph
