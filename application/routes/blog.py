from typing import Tuple, List, Dict, Union
from functools import wraps
import re

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
# from application.database.mysql import mysql_to_df, open_mysql_connection
from application.helper import temp_lru_cache

Misaka(app=app, math_explicit=True, math=True, highlight=True, fenced_code=False)

########################################################################################
##                       Blog-database interaction functions                          ##
########################################################################################


def get_posts_chronologically(
    *, text: bool = False, start: int = 1, end: int = 1
) -> pd.DataFrame:
    assert 0 < start <= end
    offset = start - 1
    limit = end - start + 1
    query = f"""
    SELECT
        p.post_id, p.title, p.posted_date, p.slug
        {',p.text' if text else ''}
    FROM posts p
    ORDER BY p.posted_date DESC
    LIMIT {offset}, {limit}
    """
    return mysql_to_df(query, database="BLOG")


def get_post_by(
    *, post_id: int = None, slug: str = None
) -> Tuple[pd.Series, List[str]]:
    err_msg = "exactly 1 argument must be None"
    assert sum([x is not None for x in (post_id, slug)]) == 1, err_msg
    # First get the post metadata and text
    query = f"""
    SELECT
        p.post_id, p.title, p.posted_date, p.slug, p.text
    FROM posts p
    {f"WHERE p.post_id = '{post_id}'" if post_id is not None else ""}
    {f"WHERE p.slug = '{slug}'" if slug is not None else ""}
    """
    post = mysql_to_df(query, database="BLOG").iloc[0]
    # Then get the tag data associated with the post
    query = f"""
    SELECT
        t.tag, t.color
    FROM tags t
    INNER JOIN post_tags pt
        ON pt.tag_id = t.tag_id
    WHERE pt.post_id = {post['post_id']}
    """
    df = mysql_to_df(query, database="BLOG")
    tags = zip(df["tag"], df["color"])
    tags = [(t, c) for t, c in sorted(tags, key=lambda x: x[0])]
    return post, tags


@temp_lru_cache(maxsize=10, dt=app.config["BLOG_REFRESH_INTERVAL"])
def get_post_by_slug(slug: str) -> Tuple[pd.Series, List[str]]:
    return get_post_by(slug=slug)


@temp_lru_cache(maxsize=1, dt=app.config["BLOG_REFRESH_INTERVAL"])
def get_most_recent_post_metadata():
    return get_posts_chronologically(text=False, start=1, end=1).iloc[0]


@temp_lru_cache(maxsize=1, dt=app.config["BLOG_REFRESH_INTERVAL"])
def map_tags_to_posts() -> Dict[str, Dict[str, str]]:
    """Queries the database for a map from tags to post slugs.
)
    Creates a JSON-like dictionary mapping tags to post metadata which will be useful in
    populating the sidebar with links. The dictionary is formatted as such:
    {
        '#computation': {
            'title': ['How to solve P=NP', 'AI is just a bunch of nested if statements']
            'slug': ['how-solve-PNP', 'nested-if-statements']
        }
        '#physics': {
            'title': ['Dark matter: liberal conspiracy', 'I wish I had a Nobel Prize']
            'slug': ['dm-lib-conspiracy', 'wish-i-had-a-nobel']
        }
        ...
    }

    Returns:
        dict: Dictionary mapping tags to lists of post 
    """
    # Query all (tag, slug) pairs
    query = """
    SELECT
        t.tag, t.color, p.slug, p.title
    FROM post_tags pt
    INNER JOIN posts p
        ON pt.post_id = p.post_id
    INNER JOIN tags t
        ON pt.tag_id = t.tag_id
    ORDER BY t.tag, p.posted_date DESC
    """
    X = mysql_to_df(query, database="BLOG").drop_duplicates()
    X["tag"] = "#" + X["tag"]
    X["color"].fillna("#ffffff")
    # Get mapping from all distinct tags to list of post slugs
    X = X.groupby("tag").agg(list)
    for col in ("color",):
        X[col] = X[col].apply(lambda x: x[0])
    X = X.assign(count=X["title"].apply(len)).to_dict("index")
    f = lambda k: -X[k]["count"]
    X = {k: X[k] for k in sorted(X.keys(), key=f)}
    return X


def tag2posts_context(func):
    @wraps(func)
    def inner(*args, **kwargs):
        g.tag_to_posts = map_tags_to_posts()
        return func(*args, **kwargs)

    return inner


def parse_tags(tags: Union[List[str], str]) -> List[str]:
    if isinstance(tags, str):
        tags = re.sub(r"\s*", "", tags)
        tags = re.sub(r"#+", "#", tags)
        tags = re.sub(r"\-+", "-", tags)
        tags = re.findall(r"#(\w+(\-\w+)*),?", tags)
        tags = list(zip(*tags))[0]
    for t in tags:
        assert re.fullmatch(r"^(([a-zA-Z0-9]+)\-?)+[a-zA-Z0-9]$", t)
    return tags


def submit_post_to_database(post):
    conn = open_mysql_connection(database="BLOG")
    # Insert tags into `tags` table
    # Insert post into `posts` table
    # Get the
    # Insert post/tag pairs into


########################################################################################
##                                  Blog post class                                   ##
########################################################################################


class InvalidBlogPostException(Exception):
    pass


class BlogPost:
    def __init__(
        self,
        title: str,
        slug: str,
        text: str,
        tags: Union[List[str], str],
        date: Union[pd.Timestamp, str],
        tag_colors: List[str] = None,
    ):
        # Make sure it's valid input
        try:
            for s in [title, slug, text]:
                assert isinstance(s, str)
                assert len(s) > 0
            assert re.fullmatch(r"^(([a-zA-Z0-9]+)\-?)+[a-zA-Z0-9]$", slug)
            tags = parse_tags(tags)
            assert len(tags) > 0
            date = pd.Timestamp(date)
            assert isinstance(date, pd.Timestamp)
        except AssertionError:
            raise InvalidBlogPostException
        self.title = title
        self.slug = slug
        self.text = text
        self.tags = tags
        self.date = date
        self.tag_colors = tag_colors


########################################################################################
##                                   Blog routes                                      ##
########################################################################################


@app.route("/blog", strict_slashes=False)
@tag2posts_context
def blog_landing():
    # Redirect to the most recent post
    post = get_most_recent_post_metadata()
    return redirect(url_for("blog_post", slug=post["slug"]))


@app.route("/blog/<slug>")
@tag2posts_context
def blog_post(slug: str):
    post, tags = get_post_by_slug(slug)
    # tags = [f"<span style='color: {c}'>{t}</span>" for t, c in tags]
    # tags = ", ".join(tags)
    text = post["text"]
    title = post["title"]
    date = (
        post["posted_date"]
        .tz_localize("US/Eastern")
        .strftime("%b %-d, %Y; %H:%M:%S EST")
    )
    post = BlogPost(
        title=title, text=text, date=date, tags=list(zip(*tags))[0], slug=slug
    )
    return render_template(
        template_name_or_list="blog_layout.html",
        page_title=post.title,
        content_text=post.text,
        posted_date=post.date,
        post_tags=post.tags,
    )


########################################################################################
##                                 Blog admin stuff                                   ##
########################################################################################


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if session.get("logged_in"):
            return func(*args, **kwargs)
        return redirect(url_for("login", next=request.path))

    return inner


@app.route("/blog/login", methods=["GET", "POST"])
def login():
    next_url = request.args.get("next") or request.form.get("next")
    if request.method == "POST" and request.form.get("password"):
        password = request.form.get("password")
        if password == app.config["ADMIN_PASSWORD"]:
            session["logged_in"] = True
            session.permanent = True
            return redirect(next_url or url_for("index"))
        else:
            flash("Incorrect password.", "warning")
    return render_template("login.html", next_url=next_url)


@app.route("/blog/logout", methods=["GET", "POST"])
def logout():
    if request.method == "POST":
        session.clear()
        return redirect(url_for("login"))
    return render_template("logout.html")


@app.route("/blog/create", methods=["GET", "POST"])
@tag2posts_context
def create_post():
    # If making GET request, just show the default (blank) post creation page.
    if request.method == "GET":
        return render_template("create_edit_post.html", title="Create new post")
    # If making POST request, first verify that all necessary fields are valid
    try:
        post = BlogPost(
            title=request.form["title"],
            slug=request.form["slug"],
            text=request.form["content"],
            tags=request.form["tags"],
            date=pd.Timestamp(pd.datetime.now()),
        )
    # Return flash warning of invalid submission
    except (InvalidBlogPostException, KeyError):
        flash("Invalid submission. Please fix and resubmit.", "warning")
        return render_template(
            template_name_or_list="create_edit_post.html",
            title="Create new post",
            post_title=request.form.get("title", ""),
            post_slug=request.form.get("slug", ""),
            post_tags=request.form.get("tags", ""),
            post_content=request.form.get("content", ""),
        )
    # TODO: If everything is valid then submit to the database
    return render_template("create_edit_post.html", title="Create new post")


@app.route("/blog/preview", methods=["GET", "POST"])
# @login_required
@tag2posts_context
def preview_post():
    # Shouldn't be able to get here with a GET request
    if request.method == "GET":
        abort(404)
    # Verify all entries are good
    try:
        post = BlogPost(
            title=request.form["title"],
            slug=request.form["slug"],
            text=request.form["content"],
            tags=request.form["tags"],
            date=pd.Timestamp(pd.datetime.now()),
        )
    # Return flash warning of invalid submission
    except (InvalidBlogPostException, KeyError):
        flash("Invalid submission. Please fix and resubmit.", "warning")
        return render_template(
            template_name_or_list="create_edit_post.html",
            title="Create new post",
            post_title=request.form.get("title", ""),
            post_slug=request.form.get("slug", ""),
            post_tags=request.form.get("tags", ""),
            post_content=request.form.get("content", ""),
        )
    # Return rendered preview of post
    return render_template_string(
        render_template(
            template_name_or_list="blog_layout.html",
            page_title=post.title,
            posted_date=post.date,
            post_tags=post.tags,
            content_text=post.text,
            is_submission=True,
        )
    )
