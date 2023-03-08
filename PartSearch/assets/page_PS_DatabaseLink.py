#import dash_html_components as html
#import dash_core_components as dcc
from dash import dcc
from dash import html
import pathlib
import base64


#DATA_PATH = PATH.joinpath("../assets").resolve()

PATH = pathlib.Path(__file__).parent
PNG_PATH = str(PATH)+'\\File.PNG'
#encoded_image = base64.b64encode(open(PNG_PATH, 'rb').read()).decode('ascii')

def Image_Converter_To_Dash_Format(path):
	encoded_image = base64.b64encode(open(path, 'rb').read()).decode('ascii')
	return 'data:image/png;base64,{}'.format(encoded_image)

def create_layout(app):
	return html.Div([
		########## Banner Line ###########
		html.Div([
			html.Div([
				html.H2("Part Number Database File Location",
						className="eleven columns"),
				html.Div([
					html.Img(src=Image_Converter_To_Dash_Format(PNG_PATH),#'data:image/png;base64,{}'.format(encoded_image),
							 className="logo"),
				], className="one columns"),
			],
				className="row",
			),
		], className='banner'
		),
		########## Banner Line ###########
		html.Div([
			dcc.Graph(
				id="id_PartNumberFileAddress",
				style={"display": "true",
					   'textAlign': 'center',
					   },
			),
		],
		),

    ]),
