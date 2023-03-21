from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr

from src.api.dependency.crud import get_crud
from src.repository.crud.user import UserCRUDRepository
from src.schema.token import TokenEmailVerificationResponse
from src.schema.user import UserCreateSchema, UserResponseSchema
from src.services.security.auth.email_verification import EmailService
from src.services.security.auth.token.registration import (
    generate_registration_token,
    generate_url_token,
    verify_registration_token,
)

router = APIRouter(prefix="/auth", tags=["User Routes"])


@router.post(
    path="/registration",
    description="auth:register-user",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    request: Request,
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

    try:
        registration_token, verification_code = generate_registration_token()
        user_data["emailVerificationCode"] = verification_code
        print(user_data)
        new_user = await user_repo.create(user_data=user_data)
        print(new_user)
        await EmailService(
            username=new_user["username"],  # type: ignore
            url=generate_url_token(request=request, token=registration_token),
            emails=[EmailStr(new_user["email"])],
        ).send_account_verification()
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="There was an error sending email"
        )
    return UserResponseSchema(
        id=new_user["id"],  # type: ignore
        username=new_user["username"],
        email=new_user["email"],  # type: ignore
        hashed_password=new_user["hashed_password"],  # type: ignore
        hashed_salt=new_user["hashed_salt"],  # type: ignore
        is_verified=new_user["is_verified"],  # type: ignore
        email_verification_code=new_user["email_verification_code"],  # type: ignore
        is_logged_in=new_user["is_logged_in"],  # type: ignore
        created_at=new_user["created_at"],  # type: ignore
        updated_at=new_user["updated_at"],  # type: ignore
    )


@router.get(
    path="/user-email-verification/{token}",
    description="auth:user-verification-via-email",
    response_model=TokenEmailVerificationResponse,
    status_code=status.HTTP_200_OK,
)
async def user_email_verification(
    token: str,
    user_repo: UserCRUDRepository = Depends(get_crud(repo_type=UserCRUDRepository, collection_name="users")),
) -> TokenEmailVerificationResponse:
    verification_code = verify_registration_token(token=token)
    try:
        db_user = await user_repo.read_user(id=None, verification_code=verification_code, is_logged_in=True)
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid verification code or account already verified"
        )
    return TokenEmailVerificationResponse(
        username=db_user["username"],  # type: ignore
        status="verification successful" if db_user["is_verified"] else "verification failed",
        is_verified=db_user["is_verified"],  # type: ignore
        is_logged_in=db_user["is_logged_in"],  # type: ignore
    )
