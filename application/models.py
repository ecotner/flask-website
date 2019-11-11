from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):  # noqa
    __tablename__ = "users"

    username = db.Column(db.String(255), nullable=False, primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_address = db.Column(db.String(255), nullable=True)
    insert_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=True)


# Define many-to-many relationship between posts and tags
post_tags = db.Table(
    "post_tags",
    db.Model.metadata,
    db.Column("post_id", db.Integer, db.ForeignKey("posts.post_id"), nullable=False),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.tag_id"), nullable=False),
)


class Post(db.Model):  # noqa
    __tablename__ = "posts"

    # Column defintions
    post_id = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True
    )
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    slug = db.Column(db.String(255), unique=True, index=True, nullable=False)
    author_nm = db.Column(
        db.String(255), db.ForeignKey("users.username"), nullable=False
    )
    text = db.Column(db.Text, nullable=False)
    visible = db.Column(db.Boolean, nullable=False, default=True)
    posted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    insert_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=True)

    # Relationships
    author = db.relationship("User", foreign_keys=author_nm, backref="posts")
    tags = db.relationship("Tag", secondary=post_tags, backref="posts")

    def __repr__(self):
        return f"<Post '{self.title}'>"


class Tag(db.Model):  # noqa
    __tablename__ = "tags"

    tag_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    tag = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    color = db.Column(db.String(255), nullable=True)
    insert_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Tag '#{self.tag}'>"


class Comment(db.Model):  # noqa
    __tablename__ = "comments"

    # Column definitions
    comment_id = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True
    )
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"), nullable=False)
    author_nm = db.Column(
        db.String(255), db.ForeignKey("users.username"), nullable=False
    )
    text = db.Column(db.Text, nullable=False)
    posted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    visible = db.Column(db.Boolean, nullable=False, default=True)
    deleted = db.Column(db.Boolean, nullable=False, default=False)
    insert_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=True)

    # Relationships
    post = db.relationship("Post", foreign_keys=post_id, backref="comments")
    author = db.relationship("User", foreign_keys=author_nm, backref="comments")

    def __repr__(self):
        return (
            f"<Comment (comment_id={self.comment_id}, post_id={self.post_id}, "
            f"author_id={self.author_id})>"
        )
