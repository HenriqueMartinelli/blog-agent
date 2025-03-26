# app/services/post_service.py

from datetime import datetime
from typing import List

from protocols.posts import IPostService
from schemas.post import Post, PostCreate, PostUpdate
from repositories.post_repository import PostRepository
from services.topic_service import TopicService
from services.LLMService import LLMService


class PostService(IPostService):
    def __init__(self) -> None:
        self.repository = PostRepository()

    # === CRUD ===

    async def get_all_posts(self) -> List[Post]:
        return await self.repository.fetch_all()

    async def get_post_by_id(self, post_id: int) -> Post:
        return await self.repository.fetch_by_id(post_id)

    async def create_post(self, post_data: PostCreate) -> Post:
        new_post = Post(
            id=0,
            titulo=post_data.titulo,
            conteudo=post_data.conteudo,
            autor=post_data.autor,
            data_criacao=datetime.utcnow()
        )
        return await self.repository.create(new_post)

    async def update_post(self, post_id: int, post_data: PostUpdate) -> Post:
        return await self.repository.update(post_id, post_data)

    async def delete_post(self, post_id: int) -> bool:
        return await self.repository.delete(post_id)

    # === AUTONOMOUS ===

    async def create_post_autonomously(self) -> Post:
        topics = await TopicService().get_trending_topics(limit=1)
        if not topics:
            raise Exception("Nenhum tópico encontrado.")

        selected_topic = topics[0]

        generated = await LLMService().generate_post(topic=selected_topic)

        post_data = PostCreate(
            titulo=generated["title"],
            conteudo=generated["body"],
            autor="Autonomous Agent"
        )

        return await self.create_post(post_data)
