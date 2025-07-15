# tests/conftest.py

from fastapi.testclient import TestClient
from unittest.mock import patch
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from faker import Faker

from src.schemas.user import UserCreate
from src.models import Base
from src.crud.user import create_user
from src.main import main_app
from src.database.core import get_db

fake = Faker()

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

AsyncTestingSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

def hash_password(password: str) -> str:
    return f"hashed-{password}"

# Створити і дропнути БД для кожної сесії pytest
@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Сесія для кожного тесту
@pytest.fixture()
async def db_session():
    async with AsyncTestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

@pytest.fixture(scope="session")
def client():
    # Створюємо тестовий клієнт
    with TestClient(main_app) as client:
        yield client

@pytest.fixture()
async def test_user(db_session: AsyncSession):
    with patch("src.crud.user.hash_password", hash_password):
        user_data = UserCreate(
            email=fake.email(),
            password=fake.password(),
            first=fake.first_name(),
            last=fake.last_name()
        )
        user = await create_user(user_in=user_data, session=db_session)
        await db_session.refresh(user)
        return user

@pytest.fixture(autouse=True)
def override_dependencies(db_session):
    # Підміняємо залежність для всіх тестів
    main_app.dependency_overrides[get_db] = lambda: db_session
    yield
    # Очищаємо підміни після тесту
    main_app.dependency_overrides.clear()
