from fastapi import APIRouter, Depends, Security, status

from src.api.dependency.crud import get_crud
from src.api.dependency.user import get_current_user
from src.repository.crud.user import UserCRUDRepository
from src.schema.user import UserBaseSchema, UserDeletionResponseSchema, UserResponseSchema
from src.services.exceptions.http.exc_400 import http_exc_400_bad_request
from src.services.exceptions.http.exc_401 import http_exc_401_unauthorized_request
from src.services.security.auth.oauth2.scopes import cookie_scopes_keys

router = APIRouter(prefix="/users", tags=["User"])


@router.get(
    path="/",
    name="user:users",
    response_model=list[UserResponseSchema],
    status_code=status.HTTP_200_OK,
)
async def get_all_users(
    user_repo: UserCRUDRepository = Depends(get_crud(repo_type=UserCRUDRepository, collection_name="users")),
) -> list[UserResponseSchema]:
    try:
        db_users = await user_repo.read_all()
    except Exception:
        raise await http_exc_400_bad_request()
    users = list()
    for db_user in db_users:
        user = UserResponseSchema(**db_user)  # type: ignore
        users.append(user)
    return users


@router.delete(
    path="/{id}/delete",
    name="user:user-deletion",
    response_model=UserDeletionResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete_blog(
    user_id: str,
    current_user: UserBaseSchema = Security(get_current_user, scopes=[cookie_scopes_keys[5]]),
    user_repo: UserCRUDRepository = Depends(get_crud(repo_type=UserCRUDRepository, collection_name="users")),
) -> UserDeletionResponseSchema:
    if not current_user:
        raise await http_exc_400_bad_request()
    try:
        db_user = await user_repo.read_user_by_id(id=user_id)
    except Exception:
        raise await http_exc_401_unauthorized_request()
    try:
        is_user_deleted = await user_repo.delete_user_by_id(id=db_user["id"])  # type: ignore
    except Exception:
        raise await http_exc_400_bad_request()
    return UserDeletionResponseSchema(is_user_deleted=is_user_deleted)
