# pylint: disable=cyclic-import
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.database.sqlite import config_db

from scripts.excel_compare.helper import read_excel_and_save_to_db, validate_excel_file


def get_data_from_employee(file_path):
    from app import create_app

    app, _ = create_app()
    _, app = config_db()
    with app.app_context():
        return read_excel_and_save_to_db(file_path)


def validate_with_database(file_path):
    from app import create_app

    app, _ = create_app()
    _, app = config_db()
    with app.app_context():
        return validate_excel_file(file_path)
