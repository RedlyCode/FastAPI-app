from typing import Callable, AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config import DatabaseConfig
from database.models import BaseModel


async def create_session_pool(
        db: DatabaseConfig, echo=False, drop_all_tables: bool = False
) -> Callable[[], AsyncContextManager[AsyncSession]]:
    engine = create_async_engine(
        db.construct_sqlalchemy_url(),
        query_cache_size=1200,
        pool_size=10,
        max_overflow=200,
        echo=echo,
    )

    async with engine.begin() as connection:
        # Synchronization tables
        if drop_all_tables:
            await connection.run_sync(BaseModel.metadata.drop_all)  # Deleting all used tables
        await connection.run_sync(BaseModel.metadata.create_all)  # Creation of all used tables

    session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)
    return session_pool
