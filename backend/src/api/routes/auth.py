from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder

from src.api.dependency.crud import get_crud
from src.repository.crud.user import UserCRUDRepository
from src.schema.user import UserCreateSchema, UserResponseSchema

router = APIRouter(prefix="/auth", tags=["User Routes"])


@router.post(
    path="/registration",
    description="auth:register-user",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_info: UserCreateSchema,
    user_repo: UserCRUDRepository = Depends(get_crud(repo_type=UserCRUDRepository, collection_name="users")),
) -> UserResponseSchema:
    user_data = jsonable_encoder(obj=user_info)

    if await user_repo.is_username_taken(username=user_data["username"]):
        username = user_data["username"]
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The username `{username}` is alreay taken!")

    if await user_repo.is_email_taken(email=user_data["email"]):
        email = user_data["email"]
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The email `{email}` is alreay taken!")

    if not await user_repo.is_password_matched(
        password=user_data["password"], repeated_password=user_data["repeatedPassword"]
    ):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Your password doesn't match!")

    new_user = await user_repo.create(user_data=user_data)
    return UserResponseSchema(
        id=new_user["id"],  # type: ignore
        username=new_user["username"],
        email=new_user["email"],  # type: ignore
        hashed_password=new_user["hashed_password"],  # type: ignore
        hashed_salt=new_user["hashed_salt"],  # type: ignore
        is_verified=new_user["is_verified"],  # type: ignore
        is_logged_in=new_user["is_logged_in"],  # type: ignore
        created_at=new_user["created_at"],  # type: ignore
        updated_at=new_user["updated_at"],  # type: ignore
    )
