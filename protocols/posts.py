from abc import ABC, abstractmethod
from typing import List
from schemas.post import PostCreate, PostUpdate, Post

class IPostService(ABC):
    @abstractmethod
    async def get_all_posts(self) -> List[Post]: ...

    @abstractmethod
    async def get_post_by_id(self, post_id: int) -> Post: ...

    @abstractmethod
    async def create_post(self, post: PostCreate) -> Post: ...

    @abstractmethod
    async def update_post(self, post_id: int, post: PostUpdate) -> Post: ...

    @abstractmethod
    async def delete_post(self, post_id: int) -> bool: ...
