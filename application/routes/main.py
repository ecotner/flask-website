"""
Author: Eric Cotner, PhD
Date: 2019-10-14

A personal website. All works displayed here are subject to the Creative Commons'
'Attribution-NonCommercial-ShareAlike 4.0 International' license.
"""
from flask import (
    g,
    render_template,
    url_for,
    redirect,
    send_file,
    render_template_string,
)
from flask_misaka import Misaka

from application.database.mysql import mysql_to_df
from application import app

Misaka(app=app, math_explicit=True, math=True, highlight=True, fenced_code=False)

nav_links = {
    "index": "Home",
    "datascience": "Data Science",
    "physics": "Physics",
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
    return render_template(
        template_name_or_list="banner_layout.html",
        title="Eric Cotner",
        banner_img="banner-bullet-cluster.jpg",
        banner_desc="Bullet Cluster x-ray map taken by Chandra telescope",
        banner_h1="Eric Cotner",
        banner_h2="Data scientist / physicist",
        text=text,
    )


@app.route("/datascience")
def datascience():
    with app.open_resource("markdown/datascience.md", mode="r") as fo:
        text = fo.read()
    tmp = render_template(
        template_name_or_list="banner_layout.html",
        title="Data Science - Eric Cotner",
        banner_img="clustering_comparison.png",
        banner_desc="A comparison of several unsupervised clustering techniques from `scikit-learn`",
        banner_h1="Data Science",
        banner_h2="and Machine Learning, AI, etc...",
        text=text,
    )
    return render_template_string(tmp)


@app.route("/physics")
def physics():
    with app.open_resource("markdown/physics.md", mode="r") as fo:
        text = fo.read()
    tmp = render_template(
        template_name_or_list="banner_layout.html",
        title="Physics - Eric Cotner",
        banner_img="particle_tracks.svg",
        banner_desc="A collision event at the LHC",
        banner_h1="Physics",
        banner_h2="",
        text=text,
    )
    return render_template_string(tmp)


@app.route("/github")
def github():
    return redirect(location=r"https://github.com/ecotner")


@app.route("/resume")
def resume():
    return send_file("static/media/resume.pdf")


@app.route("/about")
def about():
    with app.open_resource("markdown/about.md", mode="r") as fo:
        text = fo.read()
    return render_template(
        template_name_or_list="banner_layout.html",
        title="About Me - Eric Cotner",
        banner_img="honduras_dive.jpg",
        banner_desc="Scuba diving in Roatán, Honduras",
        banner_h1="About me",
        banner_h2="",
        text=text,
    )


# if __name__ == "__main__":
#     app.run(debug=True)
