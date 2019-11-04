from flask import Flask

app = Flask(__name__)
app.jinja_env.globals.update(zip=zip, len=len)

from application.routes import main, blog
