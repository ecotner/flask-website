"""
Author: Eric Cotner, PhD
Date: 2019-10-14

A personal website. All works displayed here are subject to the Creative Commons'
'Attribution-NonCommercial-ShareAlike 4.0 International' license.
"""

from flask import Flask, g, render_template, url_for

app = Flask(__name__)
nav_links = {
    "index": "Home",
    "datascience": "Data Science",
    "physics": "Physics",
    "bio": "Bio",
    "resume": "Resume",
}


@app.before_request
def first():
    g.nav_links = nav_links


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/datascience")
def datascience():
    return render_template("index.html")


@app.route("/physics")
def physics():
    return render_template("index.html")


@app.route("/bio")
def bio():
    return f"This is my about page, {url_for('bio')}"


@app.route("/resume")
def resume():
    return "Not yet!"
