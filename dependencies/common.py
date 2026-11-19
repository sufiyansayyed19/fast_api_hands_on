def get_message():
    return "Hello from dependency"


def get_current_user():
    return {
        "id": 1,
        "name": "Sufiyan"
    }


def get_app_name():
    return "TaskFlow"


def get_environment():
    return "development"


def get_user_role(role: str):
    return role