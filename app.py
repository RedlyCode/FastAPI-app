import uvicorn
from environs import Env
from fastapi import FastAPI, Request, Depends, HTTPException
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from config import DatabaseConfig
from database.functions.item_commands import select_items
from database.functions.setup import create_session_pool
from database.models import Item
from models.fastapi import MyItem

app = FastAPI()
env = Env()
env.read_env('.env')

session_pool = None


@app.on_event('startup')
async def setup():
    database_config = DatabaseConfig(
        host=env.str("DATABASE_HOST"),
        user=env.str("DATABASE_USER"),
        password=env.str("DATABASE_PASSWORD"),
        database=env.str("DATABASE_NAME"),
        port=env.int("DATABASE_PORT")
    )
    global session_pool
    session_pool = await create_session_pool(db=database_config, drop_all_tables=False)


async def get_session() -> AsyncSession:
    async with session_pool() as session:
        yield session


@app.get('/')
async def index(request: Request):
    return {'text': 'Hello FastAPI'}


@app.get('/items/', response_model=list[MyItem])
async def show_items(request: Request, session: AsyncSession = Depends(get_session)):
    items = await select_items(session=session, limit=100)
    return [
        MyItem(
            id=item.id,
            name=item.name,
            description=item.description,
            price=item.price,
            tax=item.tax
        ) for item in items
    ]


@app.post('/create/', status_code=201)
async def create_item(request: Request, item: MyItem, session: AsyncSession = Depends(get_session)):
    if item.id is None:
        item_data = item.dict(exclude={"id"})
    else:
        item_data = item.dict()

    result = await session.execute(
        insert(
            Item
        ).values(
            **item_data
        ).on_conflict_do_nothing().returning(Item.id)
    )
    await session.commit()

    created_item = result.scalar_one_or_none()

    if created_item is None:
        raise HTTPException(status_code=400, detail="Item creation failed")

    return {
        'status': 'OK',
        'item_id': created_item
    }


if __name__ == '__main__':
    uvicorn.run(
        app='app:app',
        host=env.str('SERVER_HOST'),
        port=env.int('SERVER_PORT'),
        workers=env.int('SERVER_WORKERS'),
        limit_concurrency=env.int('SERVER_LIMIT_CONCURRENCY'),
        reload=env.bool('SERVER_RELOAD'),
        use_colors=env.bool('SERVER_USE_COLORS')
    )
