from importlib import import_module
import os

from flask import Flask

from application.config import BaseConfig

if os.environ["FLASK_ENV"] == "production":
    from application.config import ProdConfig as config
elif os.environ["FLASK_ENV"] == "development":
    from application.config import DevConfig as config
else:
    raise ValueError("FLASK_ENV must be one of [production, development]")


def create_app(config: BaseConfig):
    # Initialize the app
    app = Flask(__name__)
    app.jinja_env.globals.update(zip=zip, len=len, bool=bool)

    # Add configuration
    app.config.from_object(config)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.get_uri()
    app.secret_key = config.ADMIN_PASSWORD

    # Set up database stuff
    from application.models import db

    db.init_app(app)
    with app.app_context():
        # Make fresh DB if specified by config
        if (
            os.environ.get("WERKZEUG_RUN_MAIN") == "true"
            and app.config["BUILD_FRESH_DB"]
        ):
            # Seed the database with some fresh data
            pkg = import_module(app.config["DB_SEED_MODULE"])
            pkg.seed_db(app, db)
        else:
            db.create_all()
    return app


app = create_app(config())

from application.routes import main, blog
