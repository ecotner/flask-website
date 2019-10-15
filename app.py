"""
Author: Eric Cotner, PhD
Date: 2019-10-14

A personal website. All works displayed here are subject to the Creative Commons'
'Attribution-NonCommercial-ShareAlike 4.0 International' license.
"""

import flask

app = flask.Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world!"

