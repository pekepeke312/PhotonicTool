from dash import html
from ..pdf2base64 import *
from textwriter import textwriter

def create_layout(app, file):
	html_list = []
	print("-- Mode: Cheatsheet Viewer --")
	textwriter("-- Mode: Cheatsheet Viewer --")

	ConvertedData = pdf2base64(file)
	for n in range(len(ConvertedData)):
		html_list.append(html.Img(src='data:image/png;base64,{}'.format(ConvertedData[n]),
								  style={'width':'80%'}),
						 )

	return html.Div(
		html_list
		, style={'textAlign': 'center'}
	)