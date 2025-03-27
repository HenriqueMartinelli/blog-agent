""" 
Rotas relacionadas aos posts do Blog Agent.

Este módulo define os endpoints REST para:
- Listar todos os posts
- Buscar post por ID
- Atualizar post
- Deletar post
- Criar post autonomamente com IA (OpenAI + Reddit)
"""

from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from typing import List

from schemas.post import Post, PostCreate, PostUpdate, ErrorMessage, PostOut
from controllers.posts_controller import PostsController
from services.posts_service import PostService

router = APIRouter(prefix='/posts', tags=['posts'])


@router.get(
    '/',
    response_model=List[Post],
    status_code=HTTPStatus.OK,
    summary="Listar todos os posts",
    description="Retorna uma lista com todos os posts cadastrados no sistema, ordenados por data de criação."
)
async def read_posts():
    """
    Recupera todos os posts disponíveis no banco de dados.

    Returns:
        List[Post]: Lista de posts existentes.
    """
    return await PostsController(PostService).get_all_posts()


@router.get(
    '/{post_id}',
    response_model=Post,
    status_code=HTTPStatus.OK,
    summary="Buscar post por ID",
    description="Retorna os detalhes de um post específico a partir do seu ID.",
    responses={
        HTTPStatus.NOT_FOUND: {'description': 'Post não encontrado', 'model': ErrorMessage}
    },
)
async def read_post_by_id(post_id: int):
    """
    Busca um post específico utilizando seu ID.

    Args:
        post_id (int): ID do post a ser buscado.

    Returns:
        Post: Objeto contendo os dados do post.

    Raises:
        HTTPException: Se o post não for encontrado.
    """
    post = await PostsController(PostService).get_post_by_id(post_id)
    if post:
        return post
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Post not found")


@router.put(
    '/{post_id}',
    response_model=Post,
    status_code=HTTPStatus.OK,
    summary="Atualizar post existente",
    description="Atualiza os dados de um post já existente, identificando-o pelo seu ID.",
    responses={
        HTTPStatus.NOT_FOUND: {'description': 'Post não encontrado', 'model': ErrorMessage}
    },
)
async def update_post(post_id: int, post_data: PostUpdate):
    """
    Atualiza um post com novos dados fornecidos.

    Args:
        post_id (int): ID do post a ser atualizado.
        post_data (PostUpdate): Novos dados do post.

    Returns:
        Post: Objeto atualizado do post.

    Raises:
        HTTPException: Se o post não for encontrado.
    """
    updated_post = await PostsController(PostService).update_post(post_id, post_data)
    if updated_post:
        return updated_post
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Post not found")


@router.delete(
    '/{post_id}',
    status_code=HTTPStatus.NO_CONTENT,
    summary="Excluir post por ID",
    description="Remove um post do sistema com base no ID fornecido.",
    responses={
        HTTPStatus.NOT_FOUND: {'description': 'Post não encontrado', 'model': ErrorMessage}
    },
)
async def delete_post(post_id: int):
    """
    Exclui um post a partir do seu ID.

    Args:
        post_id (int): ID do post a ser removido.

    Raises:
        HTTPException: Se o post não for encontrado.
    """
    deleted = await PostsController(PostService).delete_post(post_id)
    if not deleted:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Post not found")


@router.post(
    "/autonomous",
    response_model=PostOut,
    status_code=HTTPStatus.CREATED,
    summary="Criar post autônomo com IA",
    description="""
Gera automaticamente um post completo utilizando:

- Temas populares coletados via Reddit
- Conteúdo original gerado por IA (OpenAI GPT)
- Post estruturado com título, subtítulos, corpo e chamada para ação

Este endpoint é a principal funcionalidade do agente autônomo.
"""
)
async def create_autonomous_post():
    """
    Gera um novo post de forma autônoma utilizando inteligência artificial.

    Returns:
        PostOut: Objeto contendo o post gerado automaticamente.
    """
    return await PostService().create_post_autonomously()
