from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Post(db.Model):
    __tablename__ = "posts"

    post_id = db.Column(db.Integer, primary_key=True, nullable=False)
    posted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text)
    description = db.Column(db.String(255))
    title = db.Column(db.String(255), nullable=False)
    insert_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    slug = db.Column(db.String(255), unique=True, nullable=False)


class Tag(db.Model):
    __tablename__ = "tags"

    tag_id = db.Column(db.Integer, primary_key=True, nullable=False)
    tag = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(255))
    insert_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    color = db.Column(db.String(255))


class PostTag(db.Model):
    __tablename__ = "post_tags"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    post_id = db.Column(db.Integer, nullable=False)
    tag_id = db.Column(db.Integer, nullable=False)
