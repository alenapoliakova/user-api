import pytest
from fastapi import status
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio

@pytest.mark.asyncio
async def test_create_user(
    async_client: AsyncClient,
    user_data: dict[str, str]
) -> None:
    """Тест создания пользователя."""
    response = await async_client.post("/api/v1/users", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["login"] == user_data["login"]
    assert "id" in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_get_user(
    async_client: AsyncClient,
    user_data: dict[str, str]
) -> None:
    """Тест получения пользователя по id."""
    # Создаем пользователя
    create_response = await async_client.post("/api/v1/users", json=user_data)
    assert create_response.status_code == status.HTTP_201_CREATED
    data = create_response.json()
    user_id = data["id"]

    # Получаем пользователя
    response = await async_client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["login"] == user_data["login"]
    assert "password" not in data
    assert "password_hash" not in data


@pytest.mark.asyncio
async def test_update_user(
    async_client: AsyncClient,
    user_data: dict[str, str],
    updated_user_data: dict[str, str]
) -> None:
    """Тест полного обновления пользователя."""
    # Создаем пользователя
    create_response = await async_client.post("/api/v1/users", json=user_data)
    assert create_response.status_code == status.HTTP_201_CREATED
    data = create_response.json()
    user_id = data["id"]
    
    # Обновляем пользователя
    response = await async_client.put(
        f"/api/v1/users/{user_id}",
        json=updated_user_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["login"] == updated_user_data["login"]
    assert data["name"] == updated_user_data["name"]
    assert "password" not in data
    assert "password_hash" not in data


@pytest.mark.asyncio
async def test_partial_update_user(
    async_client: AsyncClient,
    user_data: dict[str, str],
    partial_update_data: dict[str, str]
) -> None:
    """Тест частичного обновления пользователя."""
    # Создаем пользователя
    create_response = await async_client.post("/api/v1/users", json=user_data)
    assert create_response.status_code == status.HTTP_201_CREATED
    data = create_response.json()
    user_id = data["id"]

    # Частично обновляем пользователя
    response = await async_client.patch(
        f"/api/v1/users/{user_id}",
        json=partial_update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["login"] == user_data["login"]  # login не менялся
    assert data["name"] == partial_update_data["name"]
    assert data["subject"] == partial_update_data["subject"]
    assert "password" not in data
    assert "password_hash" not in data


@pytest.mark.asyncio
async def test_delete_user(
    async_client: AsyncClient,
    user_data: dict[str, str]
) -> None:
    """Тест удаления пользователя."""
    # Создаем пользователя
    create_response = await async_client.post("/api/v1/users", json=user_data)
    assert create_response.status_code == status.HTTP_201_CREATED
    data = create_response.json()
    user_id = data["id"]

    # Удаляем пользователя
    response = await async_client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_get_deleted_user(
    async_client: AsyncClient,
    user_data: dict[str, str]
) -> None:
    """Тест получения удаленного пользователя."""
    # Создаем пользователя
    create_response = await async_client.post("/api/v1/users", json=user_data)
    assert create_response.status_code == status.HTTP_201_CREATED
    data = create_response.json()
    user_id = data["id"]

    # Удаляем пользователя
    delete_response = await async_client.delete(f"/api/v1/users/{user_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    # Пытаемся получить удаленного пользователя
    response = await async_client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_users(
    async_client: AsyncClient,
    users_data: list[dict[str, str]],
    user_filter: dict[str, str]
) -> None:
    """Тест получения пользователей в соответствии с фильтром."""
    # Создаем пользователей
    for user_data in users_data:
        create_response = await async_client.post("/api/v1/users", json=user_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        data = create_response.json()

    # Получаем пользователей
    response = await async_client.post(f"/api/v1/users/user_filter", json=user_filter)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    for data_user in data:
        for key, val in user_filter.items():
            if val is not None:
                assert data_user[key] == user_filter[key]
        assert "password" not in data_user
        assert "password_hash" not in data_user
