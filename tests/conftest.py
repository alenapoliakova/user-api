from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from app.db.base import Base, get_db
from app.main import app

settings = get_settings()


@pytest.fixture(scope="function")
def engine() -> AsyncEngine:
    """
    Создает движок базы данных для тестов.
    Используется новый движок для каждого теста.
    """
    return create_async_engine(settings.DATABASE_URL, future=True)


@pytest.fixture(scope="function")
def session_factory(engine: AsyncEngine):
    """
    Создает фабрику сессий для тестовой БД.
    """
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture
async def db_session(session_factory) -> AsyncGenerator[AsyncSession, None]:
    """
    Создает новую сессию для каждого теста.
    """
    async with session_factory() as session:
        yield session


@pytest.fixture(autouse=True)
async def prepare_database(engine: AsyncEngine):
    """
    Создаёт чистые таблицы перед каждым тестом
    и удаляет их после завершения теста.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_client(prepare_database) -> AsyncGenerator[AsyncClient, None]:
    """
    Создаёт асинхронный клиент для тестирования FastAPI приложения.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True)
def override_dependency(db_session: AsyncSession, prepare_database):
    """
    Автоматически переопределяет зависимость get_db для всех тестов.
    Ждет создания таблиц перед переопределением зависимости.
    """
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
