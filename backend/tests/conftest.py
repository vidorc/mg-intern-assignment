import pytest_asyncio
from httpx import AsyncClient
from app.main import app
from app.db.session import AsyncSessionLocal
from app.db.base import Base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
from app.models.signature import SignatureRequest

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    # Use test database (override settings maybe)
    # For simplicity, we assume a test DB; we can skip real DB tests
    pass
