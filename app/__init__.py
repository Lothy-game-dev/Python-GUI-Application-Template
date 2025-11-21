"""
This module initializes the Flask application and
sets up the necessary configurations and blueprints.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS


def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)
    CORS(app, resources={r"/validate/*": {"origins": "*"}})
    CORS(app, resources={r"/excel-compare/*": {"origins": "*"}})
    app.config["MAX_CONTENT_LENGTH"] = 15 * 1024 * 1024
    socketio = SocketIO(app, async_mode="threading", cors_allowed_origins="*")

    app.name = "e -Tax"
    from app.config import save_to_env
    from app.routes import main as main_blueprint

    # Load the config
    save_to_env()

    # Register blueprints
    def register_blueprints(app):
        """
        Register Flask blueprints.
        """
        app.register_blueprint(main_blueprint)

    register_blueprints(app)

    # Example of setting up an after_request handler
    @app.after_request
    def after_request(response):
        """
        Modify the response if needed.
        """
        return response

    return app, socketio
