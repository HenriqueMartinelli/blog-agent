# app/repositories/post_repository.py

from typing import List, Optional
from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.post import Post, PostUpdate
from models.models import PostModel
from database.sqlalchemy_session import get_session


class PostRepository:
    def __init__(self) -> None:
        self.get_session = get_session  

    async def fetch_all(self) -> List[Post]:
        async with self.get_session() as session:
            result = await session.execute(select(PostModel))
            rows = result.scalars().all()
            return [self._to_schema(post) for post in rows]

    async def fetch_by_id(self, post_id: int) -> Optional[Post]:
        async with self.get_session() as session:
            result = await session.execute(
                select(PostModel).where(PostModel.id == post_id)
            )
            post = result.scalar_one_or_none()
            return self._to_schema(post) if post else None

    async def create(self, post: Post) -> Post:
        async with self.get_session() as session:
            db_post = PostModel(
                titulo=post.titulo,
                conteudo=post.conteudo,
                autor=post.autor,
                data_criacao=post.data_criacao or datetime.utcnow(),
            )
            session.add(db_post)
            await session.commit()
            await session.refresh(db_post)
            return self._to_schema(db_post)

    async def update(self, post_id: int, data: PostUpdate) -> Optional[Post]:
        async with self.get_session() as session:
            result = await session.execute(select(PostModel).where(PostModel.id == post_id))
            db_post = result.scalar_one_or_none()
            if not db_post:
                return None

            for field, value in data.dict().items():
                setattr(db_post, field, value)

            await session.commit()
            await session.refresh(db_post)
            return self._to_schema(db_post)

    async def delete(self, post_id: int) -> bool:
        async with self.get_session() as session:
            result = await session.execute(select(PostModel).where(PostModel.id == post_id))
            db_post = result.scalar_one_or_none()
            if not db_post:
                return False

            await session.delete(db_post)
            await session.commit()
            return True

    def _to_schema(self, model: PostModel) -> Post:
        return Post(
            id=model.id,
            titulo=model.titulo,
            conteudo=model.conteudo,
            autor=model.autor,
            data_criacao=model.data_criacao,
        )
