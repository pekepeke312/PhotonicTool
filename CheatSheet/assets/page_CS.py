from dash import html
from ..pdf2base64 import *

def create_layout(app, file):
	html_list = []
	ConvertedData = pdf2base64(file)
	for n in range(len(ConvertedData)):
		html_list.append(html.Img(src='data:image/png;base64,{}'.format(ConvertedData[n]),
								  style={'width':'60%'}),
						 )

	return html.Div(
		html_list
		, style={'textAlign': 'center'}
	)