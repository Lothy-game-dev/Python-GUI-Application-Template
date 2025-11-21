import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.__init__ import create_app
from app.database.sqlite import config_db
from app.controllers.user_controller import *
from app.repositories.user_repository import (
    create_user as create_user_repo,
    update_user as update_user_repo,
    delete_user as delete_user_repo,
)
from app.repositories.user_repository import (
    get_users as get_users_repo,
    get_user_by_id as get_user_by_id_repo,
    get_user_by_employee_id_and_name as get_user_by_employee_id_and_name_repo,
    get_users_with_deleted as get_users_with_deleted_repo,
)
from app.models.user import User
import numpy as np
import pytest
from test_environment import frozen_config, reset_frozen_config

app, db = None, None


@pytest.fixture(scope="session")
def setup_module(request):
    global app, db
    if request.param == "frozen":
        frozen_config()
    else:
        reset_frozen_config()
    app, _ = create_app()
    db, app = config_db()
    yield
    reset_frozen_config()


def generate_random_new_user():
    random_employee_id = str(np.random.randint(10000000000, 99999999999))
    random_name = f"Test User {random_employee_id}"
    return random_employee_id, random_name


def get_random_user():
    with app.app_context():
        users = get_users_repo()
        return users[np.random.randint(-1, len(users))]


@pytest.mark.parametrize("setup_module", ["frozen", "non-frozen"], indirect=True)
def test_random_create_user(setup_module):

    random_employee_id, random_name = generate_random_new_user()
    with app.app_context():
        user_from_repo, test = create_user_repo(
            {"employee_id": random_employee_id, "name": random_name}
        )

        user = get_user_by_employee_id_and_name_repo(random_employee_id)

    assert test == True
    assert user is not None
    assert user.name == random_name
    assert user.employee_id == random_employee_id
    assert user_from_repo.name == random_name
    assert user_from_repo.employee_id == random_employee_id


@pytest.mark.parametrize("setup_module", ["frozen", "non-frozen"], indirect=True)
def test_create_existing_user(setup_module):

    random_user = get_random_user()
    with app.app_context():
        user_from_repo, test = create_user_repo(
            {"employee_id": random_user.employee_id, "name": random_user.name}
        )

    assert test == False
    assert user_from_repo.serialize() == random_user.serialize()


@pytest.mark.parametrize("setup_module", ["frozen", "non-frozen"], indirect=True)
def test_random_update_user_repo(setup_module):

    random_user = get_random_user()
    random_new_name = f"Updated Name {np.random.randint(0, 999999999999)}"
    with app.app_context():
        user_from_repo, test = update_user_repo(
            random_user.id,
            {"employee_id": random_user.employee_id, "name": random_new_name},
        )

        user = get_user_by_id_repo(random_user.id)

    assert test == True
    assert user is not None
    assert user.name == random_new_name
    assert user_from_repo.name == random_new_name


@pytest.mark.parametrize("setup_module", ["frozen", "non-frozen"], indirect=True)
def test_update_non_existing_user(setup_module):

    random_employee_id, random_name = generate_random_new_user()
    with app.app_context():
        user_from_repo, test = update_user_repo(
            -1, {"employee_id": random_employee_id, "name": random_name}
        )

    assert test == False
    assert user_from_repo is None


@pytest.mark.parametrize("setup_module", ["frozen", "non-frozen"], indirect=True)
def test_random_delete_user_repo(setup_module):

    random_user = get_random_user()
    with app.app_context():
        user_from_repo, test = delete_user_repo(random_user.id)

        user = get_user_by_id_repo(random_user.id)

    assert test == True
    assert user_from_repo is not None
    assert user is None


@pytest.mark.parametrize("setup_module", ["frozen", "non-frozen"], indirect=True)
def test_delete_non_existing_user(setup_module):
    with app.app_context():
        user_from_repo, test = delete_user_repo(-1)

    assert test == False
    assert user_from_repo is None


@pytest.mark.parametrize("setup_module", ["frozen", "non-frozen"], indirect=True)
def test_get_all_users_include_deleted(setup_module):
    with app.app_context():
        users = get_users_with_deleted_repo()
        non_deleted_users = get_users_repo()

        deleted_users = [user for user in users if user.deleted_at is not None]
        non_deleted_users_2 = [user for user in users if user.deleted_at is None]

    assert users is not None
    assert len(deleted_users) + len(non_deleted_users_2) == len(users)
    assert len(non_deleted_users) == len(non_deleted_users_2)


@pytest.mark.parametrize("setup_module", ["frozen", "non-frozen"], indirect=True)
def test_get_user_with_employee_id_and_name(setup_module):
    random_user = get_random_user()
    with app.app_context():
        user = get_user_by_employee_id_and_name_repo(random_user.employee_id)

    assert user is not None
    assert user.id == random_user.id
