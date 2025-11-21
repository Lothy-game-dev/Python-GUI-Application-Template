import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from repositories.user_repository import (
    create_user as create_user_repo,
    update_user as update_user_repo,
    delete_user as delete_user_repo,
    get_users as get_users_repo,
    get_user_by_id as get_user_by_id_repo,
)


def create_user(user_data):
    # Create a new user instance
    new_user, success = create_user_repo(user_data)
    if not success:
        print("\033[91mUser already exists\033[0m")
        success = False
    else:
        print("\033[92mUser created successfully\033[0m")
        success = True
    return new_user, success


def update_user(user_id, user_data):
    # Find the user by ID
    updated_user, success = update_user_repo(user_id, user_data)
    if not success:
        print("\033[91mUser already exists\033[0m")
    else:
        print("\033[92mUser updated successfully\033[0m")
    return updated_user


def delete_user(user_id):
    deleted_user, success = delete_user_repo(user_id)
    if not success:
        print("\033[91mUser not found\033[0m")
    else:
        print("\033[92mUser deleted successfully\033[0m")
    return deleted_user


def get_users():
    # Retrieve all users
    return get_users_repo()


def get_user_by_id(user_id):
    # Retrieve a user by ID
    return get_user_by_id_repo(user_id)
