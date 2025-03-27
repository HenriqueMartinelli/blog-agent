from typing import Self
from protocols.posts import IPostService
from schemas.post import Post, PostCreate, PostUpdate


class PostsController:
    __slots__ = ('service',)

    def __init__(self: Self, service: IPostService) -> None:
        """
        Injeta o serviço de postagens (implementação do protocolo IPostService).

        Args:
            service (IPostService): classe concreta que implementa a lógica de negócio.
        """
        self.service = service()

    async def get_all_posts(self: Self) -> list[Post]:
        return await self.service.get_all_posts()

    async def get_post_by_id(self: Self, post_id: int) -> Post | None:
        return await self.service.get_post_by_id(post_id)

    async def create_post(self: Self, post_data: PostCreate) -> Post:
        return await self.service.create_post(post_data)

    async def update_post(self: Self, post_id: int, post_data: PostUpdate) -> Post | None:
        return await self.service.update_post(post_id, post_data)

    async def delete_post(self: Self, post_id: int) -> bool:
        return await self.service.delete_post(post_id)
