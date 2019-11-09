from typing import Union

from flask import Flask

from application.config import BaseConfig
from application.config import DevConfig as config


def create_app(config: BaseConfig):
    # Initialize the app
    app = Flask(__name__)
    app.jinja_env.globals.update(zip=zip, len=len)

    # Add configuration
    app.config.from_object(config)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.get_uri()

    # Set up database stuff
    from application.database.models import db

    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


app = create_app(config())

from application.routes import main  # , blog
