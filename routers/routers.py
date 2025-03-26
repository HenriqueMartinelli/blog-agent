from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from typing import List

from schemas.post import Post, PostCreate, PostUpdate, ErrorMessage
from controllers.posts_controller import PostsController
from services.posts_service import PostService

router = APIRouter(prefix='/posts', tags=['posts'])

@router.get('/', response_model=List[Post])
async def read_posts():
    return await PostsController().get_all_posts()

# @router.get(
#     '/{post_id}',
#     response_model=Post,
#     responses={
#         HTTPStatus.NOT_FOUND: {'description': 'Post not found', 'model': ErrorMessage}
#     },
# )
# async def read_post_by_id(post_id: int):
#     post = await PostsController().get_post_by_id(post_id)
#     if post:
#         return post
#     raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Post not found")

# @router.put(
#     '/{post_id}',
#     response_model=Post,
#     responses={
#         HTTPStatus.NOT_FOUND: {'description': 'Post not found', 'model': ErrorMessage}
#     },
# )
# async def update_post(post_id: int, post_data: PostUpdate):
#     updated_post = await PostsController().update_post(post_id, post_data)
#     if updated_post:
#         return updated_post
#     raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Post not found")

# @router.delete(
#     '/{post_id}',
#     status_code=HTTPStatus.NO_CONTENT,
#     responses={
#         HTTPStatus.NOT_FOUND: {'description': 'Post not found', 'model': ErrorMessage}
#     },
# )
# async def delete_post(post_id: int):
#     deleted = await PostsController().delete_post(post_id)
#     if not deleted:
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Post not found")


@router.post("/autonomous", response_model=Post)
async def create_autonomous_post():
    return await PostService().create_post_autonomously()