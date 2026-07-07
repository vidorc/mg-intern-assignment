from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

# SQLite async engine – note the connect_args for aiosqlite
engine = create_async_engine(
    settings.database_url.get_secret_value(),
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
