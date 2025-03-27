# tests/test_services/test_post_service.py
import pytest
from services.posts_service import PostService

@pytest.mark.asyncio
async def test_create_post_autonomously_returns_post():
    service = PostService()
    post = await service.create_post_autonomously()

    assert post.titulo
    assert post.conteudo
    assert post.autor == "Autonomous Agent"
