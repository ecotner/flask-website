from typing import Tuple, List, Dict

from flask import g, render_template, url_for, redirect
from flask_misaka import Misaka
import pandas as pd

from application import app
from application.database.mysql import mysql_to_df
from application.helper import temp_lru_cache
from application.config import Config

config = Config()
Misaka(app=app, math_explicit=True, math=True, highlight=True, fenced_code=False)


def get_posts_chronologically(
    *, text=False, start: int = 1, end: int = 1
) -> pd.DataFrame:
    assert 0 < start <= end
    offset = start - 1
    limit = end - start + 1
    query = f"""
    SELECT
        p.post_id, p.title, p.posted_date, p.link
        {',p.text' if text else ''}
    FROM posts p
    ORDER BY p.posted_date DESC
    LIMIT {offset}, {limit}
    """
    return mysql_to_df(query, database="BLOG")


def get_post_by(
    *, post_id: int = None, link: str = None
) -> Tuple[pd.Series, List[str]]:
    err_msg = "exactly 1 argument must be None"
    assert sum([x is not None for x in (post_id, link)]) == 1, err_msg
    # First get the post metadata and text
    query = f"""
    SELECT
        p.post_id, p.title, p.posted_date, p.link, p.text
    FROM posts p
    {f"WHERE p.post_id = '{post_id}'" if post_id is not None else ""}
    {f"WHERE p.link = '{link}'" if link is not None else ""}
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
def get_post_by_link(link: str) -> Tuple[pd.Series, List[str]]:
    return get_post_by(link=link)


@temp_lru_cache(maxsize=1, dt=config["BLOG_REFRESH_INTERVAL"])
def get_most_recent_post_metadata():
    return get_posts_chronologically(text=False, start=1, end=1).iloc[0]


@temp_lru_cache(maxsize=1, dt=config["BLOG_REFRESH_INTERVAL"])
def map_tags_to_posts() -> Dict[str, Dict[str, str]]:
    """Queries the database for a map from tags to post links.

    Creates a JSON-like dictionary mapping tags to post metadata which will be useful in
    populating the sidebar with links. The dictionary is formatted as such:
    {
        '#computation': {
            'title': ['How to solve P=NP', 'AI is just a bunch of nested if statements']
            'link': ['how-solve-PNP', 'nested-if-statements']
        }
        '#physics': {
            'title': ['Dark matter: liberal conspiracy', 'I wish I had a Nobel Prize']
            'link': ['dm-lib-conspiracy', 'wish-i-had-a-nobel']
        }
        ...
    }

    Returns:
        dict: Dictionary mapping tags to lists of post 
    """
    # Query all (tag, link) pairs
    query = """
    SELECT
        t.tag, t.color, p.link, p.title
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
    # Get mapping from all distinct tags to list of post links
    X = X.groupby("tag").agg(list)
    for col in ("color",):
        X[col] = X[col].apply(lambda x: x[0])
    X = X.assign(count=X["title"].apply(len)).to_dict("index")
    f = lambda k: -X[k]["count"]
    X = {k: X[k] for k in sorted(X.keys(), key=f)}
    return X


@app.route("/blog", strict_slashes=False)
def blog_landing():
    # Redirect to the most recent post
    post = get_most_recent_post_metadata()
    return blog_post(post["link"])


@app.route("/blog/<link>")
def blog_post(link: str):
    tag2post = map_tags_to_posts()
    post, tags = get_post_by_link(link)
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
        tag_to_posts=tag2post,
    )


# @app.route("/admin")
# def admin():
#     return render_template(
#         template_name_or_list="blog_layout.html",
#         title="Admin portal",
#         content_text="no text here",
#     )

