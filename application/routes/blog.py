from functools import wraps
from collections import defaultdict
import pickle
import time
import os

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
from flask_sqlalchemy import sqlalchemy
from sqlalchemy.exc import IntegrityError
import pandas as pd

from application import app
from application.models import db
from application.models import User, Post, Tag, Comment, post_tags
from application.helper import temp_lru_cache

Misaka(app=app, math_explicit=True, math=True, highlight=True, fenced_code=False)

########################################################################################
##                       Blog-database interaction functions                          ##
########################################################################################


@temp_lru_cache(1, 15 * 60)
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


def publish_post(*, tags, title, author_nm, slug, text):
    tags = db.session.query(Tag).filter(Tag.tag.in_(tags)).all()
    post = Post(
        title=title,
        author_nm=author_nm,
        slug=slug,
        text=text,
        posted_date=pd.datetime.utcnow(),
        tags=tags,
    )
    db.session.add(post)
    db.session.commit()


# TODO: make sure you have proper authorization to access this page
@app.route("/blog/create", methods=["GET", "POST"])
@tag2posts_context
def create_post():
    # If making GET request, just show the default (blank) post creation page.
    if request.method == "GET":
        all_tags = Tag.query.order_by(Tag.tag).all()
        return render_template(
            "create_edit_post.html", title="Create new post", all_tags=all_tags
        )
    # If making POST request, first verify that all necessary fields are valid
    elif request.method == "POST":
        if request.form["button"] == "publish":
            try:
                # If everything is valid then submit to the database
                slug = request.form["slug"]
                publish_post(
                    tags=request.form.getlist("tags"),
                    title=request.form["title"],
                    author_nm="admin",
                    slug=slug,
                    text=request.form["content"],
                )
                return redirect(url_for("blog_post", slug=slug))
            # Return flash warning of invalid submission
            except (KeyError, AssertionError, IntegrityError) as e:
                db.session.rollback()
                flash("Invalid submission. Please fix and resubmit.", "warning")
                all_tags = Tag.query.order_by(Tag.tag).all()
                return render_template(
                    template_name_or_list="create_edit_post.html",
                    title="Create new post",
                    post_title=request.form.get("title", ""),
                    post_slug=request.form.get("slug", ""),
                    post_tags=request.form.get("tags", ""),
                    post_content=request.form.get("content", ""),
                    all_tags=all_tags,
                )
                return render_template("create_edit_post.html", title="Create new post")
        elif request.form["button"] == "return-from-preview":
            # Get the pickled post from the session
            filename = session["previewed_post"]
            with open(os.path.join(app.root_path, filename), "rb") as fp:
                post = pickle.load(fp)
            # Delete the pickle
            del session["previewed_post"]
            os.remove(os.path.join(app.root_path, filename))
            all_tags = Tag.query.order_by(Tag.tag).all()
            return render_template(
                template_name_or_list="create_edit_post.html",
                title="Create new post",
                post_title=post.title,
                post_slug=post.slug,
                post_tags=[t.tag for t in post.tags],
                post_content=post.text,
                all_tags=all_tags,
            )
    else:
        abort(404)


@app.route("/blog/preview", methods=["GET", "POST"])
# @login_required
@tag2posts_context
def preview_post():
    if request.method == "POST":
        # Prepare the post
        tags = request.form.getlist("tags")
        tags = db.session.query(Tag).filter(Tag.tag.in_(tags)).all()
        post = Post(
            title=request.form["title"],
            author_nm="admin",
            slug=request.form["slug"],
            text=request.form["content"],
            posted_date=pd.datetime.utcnow(),
            tags=tags,
        )
        # Pickle it and store the file name in the session
        filename = f"temp_posts/temp_post_{time.time()}.pickle"
        with open(os.path.join(app.root_path, filename), "wb+") as fp:
            pickle.dump(post, fp)
        session["previewed_post"] = filename
        return render_template(
            template_name_or_list="blog_layout.html",
            is_preview=True,
            page_title=post.title,
            post_title=post.title,
            author=post.author_nm,
            content_text=post.text,
            posted_date=post.posted_date.strftime("%c"),
            post_tags=tags,
        )
    else:
        # Shouldn't be able to get here unless you make a POST request
        abort(404)
