from app.database.sqlite import db
from app.models.user import User


def create_user(user_data):
    existing_user = get_user_by_employee_id_and_name(user_data.get("employee_id"))
    if existing_user:
        return existing_user, False
    new_user = User(**user_data)
    db.session.add(new_user)
    db.session.commit()
    return new_user, True


def update_user(user_id=-1, user_data=None):
    if user_id != -1 and (user_data is None or user_data.get("employee_id") is None):
        existing_user = User.query.get(user_id)
    elif user_id == -1 and not (
        user_data is None or user_data.get("employee_id") is None
    ):
        existing_user = get_user_by_employee_id_and_name(user_data.get("employee_id"))
    elif user_id != -1 and not (
        user_data is None or user_data.get("employee_id") is None
    ):
        existing_user = User.query.get(user_id)
        existing_user_by_employee_id = get_user_by_employee_id_and_name(
            user_data.get("employee_id")
        )
        if existing_user_by_employee_id and existing_user_by_employee_id.id == user_id:
            pass
        else:
            return None, False
    else:
        return None, False
    if not existing_user:
        return None, False
    if existing_user:
        for key, value in user_data.items():
            setattr(existing_user, key, value)
        db.session.commit()
        return existing_user, True
    return None, False


def delete_user(user_id=-1):
    if user_id == -1:
        return None, False
    user = get_user_by_id(user_id)
    if user:
        user.deleted_at = db.func.current_timestamp()
        db.session.commit()
        return user, True
    return None, False


def get_user_by_employee_id_and_name(employee_id, name=None):
    if employee_id is None:
        raise ValueError("Employee ID must not be None")

    try:
        if name is None:
            return User.query.filter(
                User.employee_id == employee_id, User.deleted_at == None
            ).first()
        else:
            return User.query.filter(
                User.employee_id == employee_id,
                User.name == name,
                User.deleted_at == None,
            ).first()
    except Exception as e:  # pragma: no cover
        return None  # pragma: no cover


def get_users():
    try:
        return User.query.filter(User.deleted_at == None).all()
    except Exception as e:  # pragma: no cover
        return None  # pragma: no cover


def get_users_with_deleted():
    try:
        return User.query.all()
    except Exception as e:  # pragma: no cover
        return None  # pragma: no cover


def get_user_by_id(user_id):
    try:
        return User.query.filter(User.id == user_id, User.deleted_at == None).first()
    except Exception as e:  # pragma: no cover
        return None  # pragma: no cover
