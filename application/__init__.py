from typing import Union
from importlib import import_module

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
    from application.models import db

    db.init_app(app)
    with app.app_context():
        # Make fresh DB if specified by config
        if app.config["BUILD_FRESH_DB"]:
            # Drop and recreate tables
            db.drop_all()
            db.create_all()
            # Seed the database with some fresh data
            pkg = import_module(app.config["DB_SEED_MODULE"])
            pkg.seed_db(app, db)
        else:
            db.create_all()
    return app


app = create_app(config())

from application.routes import main  # , blog
