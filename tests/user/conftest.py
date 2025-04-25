import pytest


@pytest.fixture
def user_data() -> dict[str, str]:
    """
    Базовые данные для создания пользователя.
    """
    return {
        "name": "Иван",
        "surname": "Иванов",
        "patronymic": "Иванович",
        "type": "student",
        "class_name": "10A",
        "login": "ivanov_i",
        "password": "supersecret",
        "subject": None
    }


@pytest.fixture
def updated_user_data() -> dict[str, str | None]:
    """
    Данные для полного обновления пользователя.
    """
    return {
        "name": "Пётр",
        "surname": "Петров",
        "patronymic": "Петрович",
        "type": "teacher",
        "class_name": None,
        "login": "petrov_p",
        "password": "newsecret",
        "subject": "Физика"
    }


@pytest.fixture
def partial_update_data() -> dict[str, str]:
    """
    Данные для частичного обновления пользователя.
    """
    return {
        "name": "Алексей",
        "subject": "Информатика"
    }


@pytest.fixture
def users_data() -> list[dict[str, str]]:
    """
    Базовые данные для создания пользователей.
    """
    return [
        {
            "name": "Иван",
            "surname": "Иванов",
            "patronymic": "Иванович",
            "type": "student",
            "class_name": "10A",
            "login": "ivanov_i",
            "password": "supersecret",
            "subject": None
        },
        {
            "name": "Пётр",
            "surname": "Петров",
            "patronymic": "Петрович",
            "type": "student",
            "class_name": "10A",
            "login": "petr_petrov",
            "password": "supersecret",
            "subject": None
        },
        {
            "name": "Андрей",
            "surname": "Колмогоров",
            "patronymic": "Николаевич",
            "type": "teacher",
            "class_name": None,
            "login": "boss",
            "password": "supersecret",
            "subject": "Math"
        },
    ]

@pytest.fixture
def user_filter() -> dict[str, str]:
    """
    Базовые данные для создания пользователя.
    """
    return {
        "name": None,
        "surname": None,
        "patronymic": None,
        "type": "student",
        "class_name": "10A",
        "login": None,
        "subject": None
    }
