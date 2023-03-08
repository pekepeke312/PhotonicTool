from flask import Flask, send_from_directory
from dash import Dash
import os


#desktop = os.path.expanduser("~/Desktop")
# the above is valid on Windows (after 7) but if you want it in os normalized form:
desktop = os.path.normpath(os.path.expanduser("~/Desktop"))
UPLOAD_DIRECTORY = "\\Checked_Files"
FILEPATH = desktop + UPLOAD_DIRECTORY

if not os.path.exists(FILEPATH):
    os.makedirs(FILEPATH)

#external_stylesheets = ["myproject/assets/stylesheet.css"]
server = Flask('DataAnalyzer')
app = Dash(server=server)#,external_stylesheets=external_stylesheets)


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(FILEPATH, path, as_attachment=True)



