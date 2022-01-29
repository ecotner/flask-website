from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):  # noqa
    __tablename__ = "users"

    # Required columns
    username = db.Column(db.String(255), nullable=False, primary_key=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)

    # Nullable or have defaults
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

    # Required columns
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, index=True, nullable=False)
    author_nm = db.Column(
        db.String(255), db.ForeignKey("users.username"), nullable=False
    )
    text = db.Column(db.Text, nullable=False)

    # Nullable or have defaults
    post_id = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True
    )
    description = db.Column(db.String(255), nullable=True)
    update_date = db.Column(db.DateTime, nullable=True)
    visible = db.Column(db.Boolean, nullable=False, default=True)
    posted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    insert_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    author = db.relationship("User", foreign_keys=author_nm, backref="posts")
    tags = db.relationship("Tag", secondary=post_tags, backref="posts")

    def __repr__(self):
        return f"<Post '{self.title}'>"


class Tag(db.Model):  # noqa
    __tablename__ = "tags"

    # Required columns
    tag = db.Column(db.String(255), nullable=False, unique=True)

    # Nullable or have defaults
    tag_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    description = db.Column(db.String(255), nullable=True)
    color = db.Column(db.String(255), nullable=True)
    insert_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Tag '#{self.tag}'>"


class Comment(db.Model):  # noqa
    __tablename__ = "comments"

    # Required columns
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"), nullable=False)
    author_nm = db.Column(
        db.String(255), db.ForeignKey("users.username"), nullable=False
    )
    text = db.Column(db.Text, nullable=False)

    # Nullable or have defaults
    comment_id = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True
    )
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
