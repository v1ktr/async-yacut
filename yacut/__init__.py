import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def database_uri():
    return (
        os.environ.get('DATABASE_URI')
        or os.environ.get('DB')
        or 'sqlite:///db.sqlite3'
    )


app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static'),
)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DISK_TOKEN'] = os.environ.get('DISK_TOKEN')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from yacut import api_views, error_handlers, models, views  # noqa: E402, F401
