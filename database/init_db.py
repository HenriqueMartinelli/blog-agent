from database.sqlalchemy_session import engine
from database.base import Base
from models.models import PostModel  # importe todos os modelos aqui

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
