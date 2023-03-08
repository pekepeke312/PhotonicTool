import pandas as pd
import dask.dataframe as dd
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import os	#for Filename check
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from statistics import mean, variance, stdev, median
from scipy.stats import norm
import plotly.graph_objs as go
import plotly.figure_factory as ff
import time
from scipy.fft import fft
from scipy.signal import blackman
import math
from scipy import fftpack


from plotly.offline import init_notebook_mode, iplot
#init_notebook_mode()

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)