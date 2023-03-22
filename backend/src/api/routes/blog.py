from fastapi import APIRouter, Depends, HTTPException, Request, Response, Security, status
from fastapi.encoders import jsonable_encoder

from src.api.dependency.crud import get_crud
from src.api.dependency.user import get_current_user
from src.repository.crud.blog import BlogCRUDRepository
from src.schema.blog import BlogCreateSchema, BlogDeletionResponseSchema, BlogResponseSchema, BlogsResponseSchema
from src.schema.user import UserBaseSchema
from src.services.exceptions.http.exc_400 import http_exc_400_bad_request
from src.services.exceptions.http.exc_401 import http_exc_401_unauthorized_request
from src.services.security.auth.oauth2.scopes import cookie_scopes_keys

router = APIRouter(prefix="/blogs", tags=["Blog"])


@router.post(
    path="/write",
    name="blog:blog-writing",
    response_model=BlogResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def write_blog(
    payload: BlogCreateSchema,
    current_user: UserBaseSchema = Security(get_current_user, scopes=[cookie_scopes_keys[3]]),
    blog_repo: BlogCRUDRepository = Depends(get_crud(repo_type=BlogCRUDRepository, collection_name="blogs")),
) -> BlogResponseSchema:
    if not current_user:
        raise await http_exc_400_bad_request()
    jsonified_blog_data = jsonable_encoder(obj=payload)
    jsonified_current_user_data = jsonable_encoder(obj=current_user)
    jsonified_blog_data["authorName"] = jsonified_current_user_data["username"]
    jsonified_blog_data["authorId"] = jsonified_current_user_data["_id"]
    try:
        new_blog = await blog_repo.create_blog(blog_data=jsonified_blog_data)
    except Exception:
        raise await http_exc_400_bad_request()
    return BlogResponseSchema(**new_blog)  # type: ignore


@router.get(
    path="/",
    name="blog:blogs-retrieval",
    response_model=list[BlogResponseSchema],
    status_code=status.HTTP_202_ACCEPTED,
)
async def get_all_blogs(
    blog_repo: BlogCRUDRepository = Depends(get_crud(repo_type=BlogCRUDRepository, collection_name="blogs")),
) -> list[BlogResponseSchema]:
    try:
        db_blogs = await blog_repo.read_all()
    except Exception:
        raise await http_exc_400_bad_request()
    blogs = list()
    for db_blog in db_blogs:
        blog = BlogResponseSchema(**db_blog)  # type: ignore
        blogs.append(blog)
    return blogs


@router.get(
    path="/{blog_id}",
    name="blog:blog-retrieval",
    response_model=BlogResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def get_blog(
    blog_id: str,
    blog_repo: BlogCRUDRepository = Depends(get_crud(repo_type=BlogCRUDRepository, collection_name="blogs")),
) -> BlogResponseSchema:
    try:
        db_blog = await blog_repo.read_blog_by_id(id=blog_id)
    except Exception:
        raise await http_exc_400_bad_request()
    return BlogResponseSchema(**db_blog)  # type: ignore


@router.delete(
    path="/{id}/delete",
    name="blog:blog-deletion",
    response_model=BlogDeletionResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete_blog(
    blog_id: str,
    current_user: UserBaseSchema = Security(get_current_user, scopes=[cookie_scopes_keys[5]]),
    blog_repo: BlogCRUDRepository = Depends(get_crud(repo_type=BlogCRUDRepository, collection_name="blogs")),
) -> BlogDeletionResponseSchema:
    if not current_user:
        raise await http_exc_400_bad_request()
    try:
        db_blog = await blog_repo.read_blog_by_id(id=blog_id)
    except Exception:
        raise await http_exc_400_bad_request()
    if db_blog["author_id"] != str(current_user.id):
        raise await http_exc_401_unauthorized_request()
    try:
        is_blog_deleted = await blog_repo.delete_blog_by_id(id=db_blog["id"])  # type: ignore
    except Exception:
        raise await http_exc_400_bad_request()
    return BlogDeletionResponseSchema(is_blog_deleted=is_blog_deleted)
