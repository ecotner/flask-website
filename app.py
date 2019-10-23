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
    # "datascience": "Data / AI",
    "github": "GitHub",
    # "blog": "Blog",
    "about": "About / Contact",
}


@app.before_request
def first():
    g.nav_links = nav_links


@app.route("/")
def index():
    with app.open_resource("markdown/index.md", mode="r") as fo:
        text = fo.read()
    return render_template(
        template_name_or_list="banner_page.html",
        title="Eric Cotner",
        banner_img="banner-bullet-cluster.jpg",
        banner_desc="Bullet Cluster x-ray map taken by Chandra telescope",
        banner_h1="Eric Cotner",
        banner_h2="Data scientist / physicist",
        text=text,
    )


@app.route("/datascience")
def datascience():
    return index()


@app.route("/physics")
def physics():
    with app.open_resource("markdown/physics.md", mode="r") as fo:
        text = fo.read()
    tmp = render_template(
        template_name_or_list="banner_page.html",
        title="Physics - Eric Cotner",
        banner_img="particle_tracks.svg",
        banner_desc="A collision event at the LHC",
        banner_h1="Physics",
        banner_h2="",
        text=text,
    )
    return flask.render_template_string(tmp)


@app.route("/github")
def github():
    return redirect(location=r"https://github.com/ecotner")


@app.route("/about")
def about():
    text = """
    <h1>This page is under construction. In the meantime, you can contact me at 
    2.71828cotner@gmail.com.</h1>
    """
    return text.replace(r"\n", "")


@app.route("/blog")
def blog():
    return index()


# if __name__ == "__main__":
#     app.run(debug=True)
