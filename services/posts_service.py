
from datetime import datetime
from typing import List

from protocols.posts import IPostService
from models.models import PostModel
from schemas.post import Post, PostCreate, PostUpdate
from repositories.post_repository import PostRepository
from services.topic_service import TopicService
from services.LLMService import LLMService
# from services.mock_llm_service import MockLLMService as LLMService
from utils.log_utils import logger



class PostService(IPostService):
    def __init__(self) -> None:
        self.repository = PostRepository()

    # === CRUD ===

    async def get_all_posts(self) -> List[Post]:
        return await self.repository.fetch_all()

    async def get_post_by_id(self, post_id: int) -> Post:
        return await self.repository.fetch_by_id(post_id)

    async def create_post(self, post_data: PostCreate) -> Post:
        """
        Creates a new post.
        args:
            post_data (PostCreate): Post data.
        returns:
            Post: Created post.
        """
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
        """
        Creates a post autonomously by fetching a trending topic and generating a post.
        """
        logger.info("Creating post autonomously...")
        topics = await TopicService().get_trending_topics(limit=15)
        if not topics:
            raise Exception("Nenhum tópico encontrado.")

        selected_topic = topics[0]
        
        logger.info("Selected topic: %s", selected_topic)
        generated = await LLMService().generate_post(topic=selected_topic)
        
        post_data = PostCreate(
            titulo=generated["title"],
            conteudo=generated["body"],
            autor="Autonomous Agent"
        )
        logger.info("Creating post...")
        return await self.create_post(post_data)
