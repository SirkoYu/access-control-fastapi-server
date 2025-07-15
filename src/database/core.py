from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.core.config import settings

engine = create_async_engine(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    max_overflow=settings.db.max_overflow,
    pool_size=settings.db.pool_size,
)

AsyncSessionFactory = async_sessionmaker(
    bind=engine, 
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        yield session