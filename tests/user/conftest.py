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
        "email": "ivanov@example.com",
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
        "email": "petrov@example.com",
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
