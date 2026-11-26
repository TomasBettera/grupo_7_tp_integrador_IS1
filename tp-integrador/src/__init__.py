from flask import Flask
from src.extensions import db


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    if test_config:
        app.config.update(test_config)
    db.init_app(app)

    from src import models
    from src.routes import web_bp
    app.register_blueprint(web_bp)

    return app