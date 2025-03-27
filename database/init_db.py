from database.sqlalchemy_session import engine
from database.base import Base
from models.models import PostModel 
from utils.log_utils import logger

async def init_db():
    async with engine.begin() as conn:
        logger.info("Creating tables PostModel...")
        await conn.run_sync(Base.metadata.create_all)
