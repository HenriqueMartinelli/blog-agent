
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.settings import settings
from contextlib import asynccontextmanager  

engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

@asynccontextmanager
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
