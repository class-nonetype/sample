from src.core.database.base import Base
from src.core.database.engine import engine
from src.core.database.models import *


async def init() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
 
