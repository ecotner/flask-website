from flask import g, render_template
from flask_misaka import Misaka

from application.database.mysql import mysql_to_df
from application import app


@app.route("/blog")
def blog():
    query = """
        SELECT
            title
            ,text
        FROM posts
        """
    df = mysql_to_df(query)
    text = df["text"].iloc[0]
    title = df["title"].iloc[0]

    return render_template(
        template_name_or_list="sidebar_layout.html",
        title=f"{title} - Eric Cotner",
        sidebar_title="some title",
        text=text,
    )


@app.route("/admin")
def admin():
    return render_template(
        template_name_or_list="sidebar_layout.html", title="Admin portal"
    )

