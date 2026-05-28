from __future__ import annotations

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from app.routes import main
from app.auth import auth

from config import Config


db: SQLAlchemy = SQLAlchemy()

login_manager: LoginManager = LoginManager()


def create_app() -> Flask:
    app: Flask = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "login"
    
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app