from typing import Tuple, List, Dict, Union
from functools import wraps
import re
from collections import defaultdict

from flask import (
    abort,
    flash,
    g,
    redirect,
    render_template,
    render_template_string,
    request,
    session,
    url_for,
)
from flask_misaka import Misaka
import pandas as pd

from application import app
from application.models import db
from application.models import User, Post, Tag, Comment, post_tags
from application.helper import temp_lru_cache

Misaka(app=app, math_explicit=True, math=True, highlight=True, fenced_code=False)

########################################################################################
##                       Blog-database interaction functions                          ##
########################################################################################


def tag2posts_context(func):
    """ Creates context for the `g.tag2posts` object, mapping tags to posts.
    
    Arguments:
        func {route} -- Route function to be decorated with context
    
    Returns:
        func -- Returns original function with the g.tag2posts context
    """

    @wraps(func)
    def inner(*args, **kwargs):
        query = (
            db.session.query(Tag.tag, Tag.color, Post.title, Post.slug)
            .distinct()
            .join(post_tags, post_tags.c.tag_id == Tag.tag_id)
            .join(Post, post_tags.c.post_id == Post.post_id)
            .order_by(Tag.tag, Post.posted_date.desc(), Post.post_id.desc())
            .all()
        )
        # print(pd.DataFrame(query))
        tag2posts = defaultdict(list)
        for row in query:
            tag2posts[(row.tag, row.color)].append((row.title, row.slug))
        g.tag2posts = tag2posts
        return func(*args, **kwargs)

    return inner


########################################################################################
##                                   Blog routes                                      ##
########################################################################################


@app.route("/blog", strict_slashes=False)
@tag2posts_context
def blog_landing():
    # Query and return most recent blog post
    post = Post.query.order_by(Post.posted_date.desc(), Post.post_id.desc()).first()
    tags = post.tags
    return render_template(
        template_name_or_list="blog_layout.html",
        page_title=post.title,
        post_title=post.title,
        author=post.author_nm,
        content_text=post.text,
        posted_date=post.posted_date.strftime("%c"),
        post_tags=tags,
    )


@app.route("/blog/<slug>")
@tag2posts_context
def blog_post(slug: str):
    post = Post.query.filter(Post.slug == slug).first()
    tags = post.tags
    return render_template(
        template_name_or_list="blog_layout.html",
        page_title=post.title,
        post_title=post.title,
        author=post.author_nm,
        content_text=post.text,
        posted_date=post.posted_date.strftime("%c"),
        post_tags=tags,
    )


########################################################################################
##                                 Blog admin stuff                                   ##
########################################################################################


# @app.route("/blog/create", methods=["GET", "POST"])
# @tag2posts_context
# def create_post():
#     # If making GET request, just show the default (blank) post creation page.
#     if request.method == "GET":
#         return render_template("create_edit_post.html", title="Create new post")
#     # If making POST request, first verify that all necessary fields are valid
#     try:
#         post = BlogPost(
#             title=request.form["title"],
#             slug=request.form["slug"],
#             text=request.form["content"],
#             tags=request.form["tags"],
#             date=pd.Timestamp(pd.datetime.now()),
#         )
#     # Return flash warning of invalid submission
#     except (InvalidBlogPostException, KeyError):
#         flash("Invalid submission. Please fix and resubmit.", "warning")
#         return render_template(
#             template_name_or_list="create_edit_post.html",
#             title="Create new post",
#             post_title=request.form.get("title", ""),
#             post_slug=request.form.get("slug", ""),
#             post_tags=request.form.get("tags", ""),
#             post_content=request.form.get("content", ""),
#         )
#     # TODO: If everything is valid then submit to the database
#     return render_template("create_edit_post.html", title="Create new post")


# @app.route("/blog/preview", methods=["GET", "POST"])
# # @login_required
# @tag2posts_context
# def preview_post():
#     # Shouldn't be able to get here with a GET request
#     if request.method == "GET":
#         abort(404)
#     # Verify all entries are good
#     try:
#         post = BlogPost(
#             title=request.form["title"],
#             slug=request.form["slug"],
#             text=request.form["content"],
#             tags=request.form["tags"],
#             date=pd.Timestamp(pd.datetime.now()),
#         )
#     # Return flash warning of invalid submission
#     except (InvalidBlogPostException, KeyError):
#         flash("Invalid submission. Please fix and resubmit.", "warning")
#         return render_template(
#             template_name_or_list="create_edit_post.html",
#             title="Create new post",
#             post_title=request.form.get("title", ""),
#             post_slug=request.form.get("slug", ""),
#             post_tags=request.form.get("tags", ""),
#             post_content=request.form.get("content", ""),
#         )
#     # Return rendered preview of post
#     return render_template_string(
#         render_template(
#             template_name_or_list="blog_layout.html",
#             page_title=post.title,
#             posted_date=post.date,
#             post_tags=post.tags,
#             content_text=post.text,
#             is_submission=True,
#         )
#     )
