# pylint: disable=cyclic-import
import sys
import os
import json
import warnings
import openpyxl

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app.database.sqlite import config_db

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from app import create_app
from app.controllers.user_controller import create_user, get_users

warnings.simplefilter(action="ignore", category=UserWarning)


def read_excel_and_save_to_db(file_path):
    # Load the Excel workbook and select the active sheet
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    # Extract employee_id from column L, row 6 (L6)
    employee_id = sheet["L6"].value

    # Extract name from column L, row 8 (L8)
    name = sheet["L8"].value

    # Prepare user data
    user_data = {"employee_id": employee_id, "name": name}

    # Save to database
    _, success = create_user(user_data)
    if success:
        print("\033[92mUser saved successfully\033[0m")
        message = "User saved successfully"
        status = "success"
    else:
        print("\033[91mUser already exists\033[0m")
        message = "User already exists"
        status = "exists"

    return {
        "user_data": user_data,
        "message": message,
        "status": status,
    }


def validate_excel_file(file_path):
    workbook = openpyxl.load_workbook(file_path, data_only=True)
    sheet = workbook.active

    app, _ = create_app()
    _, app = config_db()
    with app.app_context():
        users_data = fetch_users_data()

        excel_users, users_not_found_in_db = collect_excel_users(sheet, users_data)
        users_not_in_excel = find_users_not_in_excel(users_data, excel_users)

        # Collect closest matches for users not found in the database
        closest_matches = [
            suggest_closest_match(user["employee_id"], users_data)
            for user in users_not_found_in_db
        ]

        # print_users_not_found(users_not_found_in_db)
        print_users_not_in_excel(users_not_in_excel)

    return {
        # "excel_users": excel_users,
        "users_not_found_in_db": users_not_found_in_db,
        "users_not_in_excel": users_not_in_excel,
        "closest_matches": closest_matches,
    }


def fetch_users_data():
    users = get_users()
    users_json = json.dumps([user.serialize() for user in users], indent=4)
    return json.loads(users_json)


def collect_excel_users(sheet, users_data):
    excel_users = []
    users_not_found_in_db = []
    row = 8
    while True:
        employee_id = sheet[f"E{row}"].value
        name = sheet[f"F{row}"].value
        custom_row = sheet[f"A{row}"].value

        if employee_id is None and name is None:
            break

        excel_users.append(
            {"employee_id": employee_id, "name": name, "custom_row": custom_row}
        )
        if not user_exists_in_db(employee_id, name, users_data):
            users_not_found_in_db.append(
                {
                    "employee_id": employee_id,
                    "name": name,
                    # "row": row - 7,
                    "custom_row": custom_row,
                }
            )
            # suggest_closest_match(employee_id, users_data)

        row += 1

    return excel_users, users_not_found_in_db


# Similar to check_user_in_db but not prints the result
def user_exists_in_db(employee_id, name, users_data):
    user_exists = any(
        user["employee_id"] == employee_id and user["name"] == name
        for user in users_data
    )
    if not user_exists:
        print(
            f"\033[91mUser with Employee ID: {employee_id} and "
            + f"Name: {name} does not exist in the database\033[0m"
        )
        suggest_closest_match(employee_id, users_data)
    else:
        print(
            f"\033[92mUser with Employee ID: {employee_id} and "
            + f"Name: {name} already exists in the database\033[0m"
        )
    return user_exists


def suggest_closest_match(employee_id, users_data):
    closest_match = next(
        (user for user in users_data if user["employee_id"] == employee_id), None
    )
    if closest_match:
        print(
            f"\033[93mDid you mean: Employee ID: {closest_match['employee_id']}, "
            + f"Name: {closest_match['name']}?\033[0m"
        )
    else:
        print("\033[93mNo similar user found in the database.\033[0m")
        return {"employee_id": employee_id, "status": "no_similar_user"}
    return closest_match


def find_users_not_in_excel(users_data, excel_users):
    return [
        user
        for user in users_data
        if not any(
            excel_user["employee_id"] == user["employee_id"]
            and excel_user["name"] == user["name"]
            for excel_user in excel_users
        )
    ]


def print_users_not_found(users_not_found_in_db):
    for user in users_not_found_in_db:
        print(
            f"\033[91mUser with Employee ID: {user['employee_id']} "
            + f"and Name: {user['name']} does not exist in the database\033[0m"
        )


def print_users_not_in_excel(users_not_in_excel):
    print(
        "\033[94mThese are the users that are in the database but not in the Excel file\033[0m"
    )
    for user in users_not_in_excel:
        print(
            f"\033[96mEmployee ID: {user['employee_id']}, Name: {user['name']}\033[0m"
        )


# if __name__ == "__main__":
#     get_excel_compare_data("app/static/testing_files/excel_compare/admin_form.xlsx")
