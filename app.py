"""
Author: Eric Cotner, PhD
Date: 2019-10-14

A personal website. All works displayed here are subject to the Creative Commons'
'Attribution-NonCommercial-ShareAlike 4.0 International' license.
"""

from flask import Flask, g, render_template, url_for, redirect
from flask_misaka import Misaka

app = Flask(__name__)
Misaka(app=app, math_explicit=True, math=True, highlight=True, fenced_code=False)

nav_links = {
    "index": "Home",
    "physics": "Physics",
    "datascience": "Data Science",
    "machinelearning": "Machine Learning",
    "github": "GitHub",
    "bio": "Bio",
    "resume": "Resume",
    "blog": "Blog",
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


@app.route("/machinelearning")
def machinelearning():
    return index()


@app.route("/physics")
def physics():
    return index()


@app.route("/github")
def github():
    return redirect(location=r"https://github.com/ecotner")


@app.route("/bio")
def bio():
    return f"This is my about page, {url_for('bio')}"


@app.route("/resume")
def resume():
    return "Not yet!"


@app.route("/blog")
def blog():
    return index()


if __name__ == "__main__":
    app.run(debug=True)
