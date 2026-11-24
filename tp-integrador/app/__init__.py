from flask import Flask
from app.extensions import db


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    db.init_app(app)

    from app import models  # noqa: registra los modelos en SQLAlchemy

    return app