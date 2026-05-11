from pathlib import Path
from typing import Annotated, Final

import api_v1.crud.post as crud
from api_v1.core.dependencies import check_active_posts_limit, user_data
from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from schemas.post import (
    ActivatePostResponse,
    ArchivatePostResponse,
    CreatePost,
    CreatePostResponse,
    GetPostsResponse,
)

router: Final[APIRouter] = APIRouter()


@router.post(
    "/create", response_model=CreatePostResponse, status_code=status.HTTP_201_CREATED
)
async def create_new_post(
    tg_id: int,
    image: UploadFile = File(...),
    post_data: CreatePost = Depends(),
    user_data: tuple = Depends(user_data),
) -> CreatePostResponse:
    user_id, sub_data = user_data
    await check_active_posts_limit(user_id=user_id, sub_data=sub_data)

    extension = Path(image.filename).suffix or ".jpg"
    file_content = await image.read()
    post_id = await crud.create_new_post(
        user_id=user_id,
        sub_data=sub_data,
        image=file_content,
        extension=extension,
        post_data=post_data,
    )
    return CreatePostResponse(post_id=post_id)


@router.get(
    "/by-user/{tg_id}",
    response_model=GetPostsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_posts_by_user(
    tg_id: int, user_data: tuple = Depends(user_data)
) -> GetPostsResponse:
    user_id, _ = user_data
    posts = await crud.get_posts_by_user(user_id=user_id)
    return GetPostsResponse(posts=posts)


@router.get(
    "/by-products",
    response_model=GetPostsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_posts_by_products(
    products: Annotated[list[int], Query()],
) -> GetPostsResponse:
    posts = await crud.get_posts_by_products(products=products)
    return GetPostsResponse(posts=posts)


@router.post(
    "/{tg_id}/{post_id}/activate",
    response_model=ActivatePostResponse,
    status_code=status.HTTP_200_OK,
)
async def activate_post(
    tg_id: int,
    post_id: int,
    user_data: tuple = Depends(user_data),
) -> ActivatePostResponse:
    user_id, sub_data = user_data
    await check_active_posts_limit(user_id=user_id, sub_data=sub_data)
    await crud.activate_post(post_id=post_id, sub_data=sub_data)
    return ActivatePostResponse()


@router.post(
    "/{post_id}/archivate",
    response_model=ArchivatePostResponse,
    status_code=status.HTTP_200_OK,
)
async def archivate_post(post_id: int) -> ArchivatePostResponse:
    await crud.archivate_post(post_id=post_id)
    return ArchivatePostResponse()
