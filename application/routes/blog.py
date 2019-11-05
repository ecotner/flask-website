from typing import Tuple, List, Dict
from functools import wraps

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
from application.database.mysql import mysql_to_df
from application.helper import temp_lru_cache
from application.config import Config
from application.secrets import SecretConfig

config = Config()
sconfig = SecretConfig()
Misaka(app=app, math_explicit=True, math=True, highlight=True, fenced_code=False)


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
    tags = [(f"#{t}", c) for t, c in sorted(tags, key=lambda x: x[0])]
    return post, tags


@temp_lru_cache(maxsize=10, dt=config["BLOG_REFRESH_INTERVAL"])
def get_post_by_slug(slug: str) -> Tuple[pd.Series, List[str]]:
    return get_post_by(slug=slug)


@temp_lru_cache(maxsize=1, dt=config["BLOG_REFRESH_INTERVAL"])
def get_most_recent_post_metadata():
    return get_posts_chronologically(text=False, start=1, end=1).iloc[0]


@temp_lru_cache(maxsize=1, dt=config["BLOG_REFRESH_INTERVAL"])
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


def add_blog_sidebar(func):
    @wraps(func)
    def inner(*args, **kwargs):
        g.tag_to_posts = map_tags_to_posts()
        return func(*args, **kwargs)

    return inner


@app.route("/blog", strict_slashes=False)
@add_blog_sidebar
def blog_landing():
    # Redirect to the most recent post
    post = get_most_recent_post_metadata()
    return blog_post(post["slug"])


@app.route("/blog/<slug>")
@add_blog_sidebar
def blog_post(slug: str):
    # tag2post = map_tags_to_posts()
    post, tags = get_post_by_slug(slug)
    tags = [f"<span style='color: {c}'>{t}</span>" for t, c in tags]
    tags = ", ".join(tags)
    text = post["text"]
    title = post["title"]
    date = (
        post["posted_date"]
        .tz_localize("US/Eastern")
        .strftime("%b %-d, %Y; %H:%M:%S EST")
    )
    return render_template(
        template_name_or_list="blog_layout.html",
        page_title=title,
        content_text=text,
        posted_date=date,
        post_tags=tags,
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
        if password == sconfig.ADMIN_PASSWORD:
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
@add_blog_sidebar
def create_post():
    if request.method == "POST":
        pass
    return render_template("create_edit_post.html", title="Create new post")


@app.route("/blog/preview", methods=["GET", "POST"])
# @login_required
@add_blog_sidebar
def preview_post():
    if request.method == "GET":
        abort(404)
    title = request.form["title"]
    # slug = request.form["slug"]
    text = request.form["content"]
    tags = request.form["tags"]
    date = pd.Timestamp(pd.datetime.now())
    return render_template_string(
        render_template(
            template_name_or_list="blog_layout.html",
            page_title=title,
            content_text=text,
            posted_date=date,
            post_tags=tags,
        )
    )
