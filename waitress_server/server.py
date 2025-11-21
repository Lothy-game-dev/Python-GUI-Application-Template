import os
import sys
import importlib.util
import logging
import traceback
from waitress import serve
from app import create_app


def run_flask():
    if getattr(sys, "frozen", False):
        # If running in a bundled application
        script_path = os.path.join(sys._MEIPASS, "app/hidden_web_run.py")
        module_name = "app"
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        flask_app, flask_socketio = create_app()
        logging.info(f"Flask path: {script_path}")
        logging.info(f"Flask app: {flask_app}")

        # Start Waitress
        logging.info("Starting Waitress server...")
        try:
            serve(flask_app, host="0.0.0.0", port=5002)
        except Exception as e:
            logging.error(f"Failed to run Flask app with Waitress: {str(e)}")
            logging.error(traceback.format_exc())
    else:
        # Run Flask directly
        flask_app, flask_socketio = create_app()
        flask_socketio.run(flask_app, debug=True, host="0.0.0.0", port=5002)


def stop_waitress():
    # Nothing to do as Waitress runs in the same process
    pass
