from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Item


async def select_items(session: AsyncSession, limit: int = None, offset: int = None):
    result = await session.execute(
        select(Item).offset(offset).limit(limit)
    )
    return result.scalars().all()
