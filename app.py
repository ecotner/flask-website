"""
Author: Eric Cotner, PhD
Date: 2019-10-14

A personal website. All works displayed here are subject to the Creative Commons'
'Attribution-NonCommercial-ShareAlike 4.0 International' license.
"""

import flask
from flask import Flask, g, render_template, url_for, redirect
from flask_misaka import Misaka

app = Flask(__name__)
Misaka(app=app, math_explicit=True, math=True, highlight=True, fenced_code=False)

nav_links = {
    "index": "Home",
    "physics": "Physics",
    "datascience": "Data / AI",
    "github": "GitHub",
    "blog": "Blog",
    "about": "About / Contact",
}


@app.before_request
def first():
    g.nav_links = nav_links


@app.route("/")
def index():
    with app.open_resource("markdown/index.md", mode="r") as fo:
        text = fo.read()
    return render_template("index.html", text=text)


@app.route("/datascience")
def datascience():
    return index()


@app.route("/physics")
def physics():
    with app.open_resource("markdown/physics.md", mode="r") as fo:
        text = fo.read()
    tmp = render_template("physics.html", text=text)
    return flask.render_template_string(tmp)


@app.route("/github")
def github():
    return redirect(location=r"https://github.com/ecotner")


@app.route("/about")
def about():
    return f"This is my about page, {url_for('about')}"


@app.route("/blog")
def blog():
    return index()


if __name__ == "__main__":
    app.run(debug=True)
