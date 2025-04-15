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
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_get_user(
    async_client: AsyncClient,
    user_data: dict[str, str]
) -> None:
    """Тест получения пользователя по email."""
    # Создаем пользователя
    create_response = await async_client.post("/api/v1/users", json=user_data)
    assert create_response.status_code == status.HTTP_201_CREATED
    
    # Получаем пользователя
    response = await async_client.get(f"/api/v1/users/{user_data['email']}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == user_data["email"]
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
    
    # Обновляем пользователя
    response = await async_client.put(
        f"/api/v1/users/{user_data['email']}", 
        json=updated_user_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == updated_user_data["email"]
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
    
    # Частично обновляем пользователя
    response = await async_client.patch(
        f"/api/v1/users/{user_data['email']}", 
        json=partial_update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == user_data["email"]  # email не менялся
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

    # Удаляем пользователя
    response = await async_client.delete(f"/api/v1/users/{user_data['email']}")
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

    # Удаляем пользователя
    delete_response = await async_client.delete(f"/api/v1/users/{user_data['email']}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    # Пытаемся получить удаленного пользователя
    response = await async_client.get(f"/api/v1/users/{user_data['email']}")
    assert response.status_code == status.HTTP_404_NOT_FOUND 
