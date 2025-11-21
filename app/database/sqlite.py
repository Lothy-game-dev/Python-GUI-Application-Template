from flask_sqlalchemy import SQLAlchemy
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from __init__ import create_app

db = SQLAlchemy()


def config_db():
    app, _ = create_app()
    # Initialize the database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # Ensure the app context is pushed
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    return db, app


def import_models():
    from app.models.user import User
