from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from pyotp import random_base32
from pyotp.totp import TOTP

from src.api.dependency.crud import get_crud
from src.repository.crud.user import UserCRUDRepository
from src.schema.email_verification import EmailVerificationResponse
from src.schema.otp import (
    OTPDataDisableFeatureSchema,
    OTPDataGenerationSchema,
    OTPDataVerificationSchema,
    OTPDisableFeatureResponseSchema,
    OTPGenerationResponseSchema,
    OTPRequestSchema,
    OTPValidationResponseSchema,
    OTPVerificationResponseSchema,
)
from src.schema.user import UserCreateSchema, UserLoginSchema, UserResponseSchema
from src.services.security.auth.email_verification import EmailService
from src.services.security.auth.token.registration import (
    generate_registration_token,
    generate_url_token,
    verify_registration_token,
)

router = APIRouter(prefix="/auth")


@router.post(
    path="/registration",
    tags=["User Authentication"],
    description="auth:user-registration",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    request: Request,
    payload: UserCreateSchema,
    user_repo: UserCRUDRepository = Depends(get_crud(repo_type=UserCRUDRepository, collection_name="users")),
) -> UserResponseSchema:
    jsonified_user_data = jsonable_encoder(obj=payload)

    if await user_repo.is_username_taken(username=jsonified_user_data["username"]):
        username = jsonified_user_data["username"]
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The username `{username}` is alreay taken!")

    if await user_repo.is_email_taken(email=jsonified_user_data["email"]):
        email = jsonified_user_data["email"]
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"The email `{email}` is alreay taken!")

    if not await user_repo.is_password_matched(
        password=jsonified_user_data["password"], repeated_password=jsonified_user_data["repeatedPassword"]
    ):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Your password doesn't match!")

    try:
        registration_token, verification_code = generate_registration_token()
        jsonified_user_data["emailVerificationCode"] = verification_code
        new_user = await user_repo.create(user_data=jsonified_user_data)
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
    return UserResponseSchema(**new_user)  # type: ignore


@router.get(
    path="/user-email-verification/{token}",
    tags=["User Authentication"],
    description="auth:user-verification-via-email",
    response_model=EmailVerificationResponse,
    status_code=status.HTTP_200_OK,
)
async def verify_user_email(
    token: str,
    user_repo: UserCRUDRepository = Depends(get_crud(repo_type=UserCRUDRepository, collection_name="users")),
) -> EmailVerificationResponse:
    verification_code = verify_registration_token(token=token)
    try:
        db_user = await user_repo.read_user_in_email_verification(verification_code=verification_code)
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid verification code or account already verified"
        )
    return EmailVerificationResponse(
        status="verification successful" if db_user["is_verified"] else "verification failed",
        **db_user,  # type: ignore
    )


@router.post(
    path="/login",
    tags=["User Authentication"],
    description="auth:user-login",
    response_model=UserResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def login_user(
    payload: UserLoginSchema,
    user_repo: UserCRUDRepository = Depends(get_crud(repo_type=UserCRUDRepository, collection_name="users")),
) -> UserResponseSchema:
    jsonified_user_data = jsonable_encoder(obj=payload)
    try:
        db_user = await user_repo.read_user_in_login(user_data=jsonified_user_data)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect credentials!")
    return UserResponseSchema(**db_user)  # type: ignore


@router.post(
    path="/otp/generate",
    tags=["2FA"],
    description="auth:user-2fa-generator",
    response_model=OTPGenerationResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def generate_otp(
    payload: OTPRequestSchema,
    user_repo: UserCRUDRepository = Depends(get_crud(repo_type=UserCRUDRepository, collection_name="users")),
) -> OTPGenerationResponseSchema:
    otp_base32 = random_base32()
    jsonified_otp_data = jsonable_encoder(
        obj=OTPDataGenerationSchema(
            user_id=payload.user_id,
            otp_base32=otp_base32,
            otp_auth_url=TOTP(otp_base32).provisioning_uri(name="welcome@pala.tech", issuer_name="Pala Blog"),
        )
    )
    if not ObjectId.is_valid(payload.user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with ID `{payload.user_id}` doesn't exist!"
        )
    try:
        updated_user = await user_repo.update_user_with_otp_details(otp_data=jsonified_otp_data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID `{payload.user_id}`is not found!"
        )
    return OTPGenerationResponseSchema(user_id=updated_user["id"], **updated_user)  # type: ignore


@router.post(
    path="/otp/verify",
    tags=["2FA"],
    description="auth:user-2fa-verification",
    response_model=OTPVerificationResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def verify_otp(
    payload: OTPRequestSchema,
    user_repo: UserCRUDRepository = Depends(get_crud(repo_type=UserCRUDRepository, collection_name="users")),
) -> OTPVerificationResponseSchema:
    jsonified_otp_data = jsonable_encoder(
        obj=OTPDataVerificationSchema(user_id=payload.user_id, is_otp_enabled=True, is_otp_verified=True)
    )
    db_user = await user_repo.read_user_by_id(id=jsonified_otp_data["userId"])
    totp = TOTP(db_user.get("otp_base32"))  # type: ignore
    if not totp.verify(otp=payload.code):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="OTP code for 2FA authentication  is wrong! Try again"
        )
    updated_user = await user_repo.update_user_with_otp_details(otp_data=jsonified_otp_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID `{payload.user_id}`is not found!"
        )
    return OTPVerificationResponseSchema(
        user_id=updated_user["id"],  # type: ignore
        is_otp_enabled=updated_user["is_otp_enabled"],  # type: ignore
        is_otp_verified=updated_user["is_otp_verified"],  # type: ignore
        verified_2fa_user=UserResponseSchema(**updated_user),  # type: ignore
    )


@router.post(
    path="/otp/validate",
    tags=["2FA"],
    description="auth:user-2fa-validation",
    response_model=OTPValidationResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def validate_otp(
    payload: OTPRequestSchema,
    user_repo: UserCRUDRepository = Depends(get_crud(repo_type=UserCRUDRepository, collection_name="users")),
) -> OTPValidationResponseSchema:
    jsonified_otp_data = jsonable_encoder(obj=payload)
    db_user = await user_repo.read_user_by_id(id=jsonified_otp_data["userId"])
    if not db_user.get("is_otp_verified"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="OTP must be verified via Authenticator!")
    totp = TOTP(db_user.get("otp_base32"))  # type: ignore
    if not totp.verify(otp=payload.code, valid_window=1):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="OTP code for 2FA authentication is wrong! Try again"
        )
    return OTPValidationResponseSchema(user_id=db_user["id"], is_otp_valid=True)  # type: ignore


@router.post(
    path="/otp/disable",
    tags=["2FA"],
    description="auth:user-disable-2fa",
    response_model=OTPDisableFeatureResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def disable_otp(
    payload: OTPRequestSchema,
    user_repo: UserCRUDRepository = Depends(get_crud(repo_type=UserCRUDRepository, collection_name="users")),
) -> OTPDisableFeatureResponseSchema:
    jsonified_otp_data = jsonable_encoder(
        obj=OTPDataDisableFeatureSchema(user_id=payload.user_id, is_otp_enabled=False)
    )
    updated_user = await user_repo.update_user_with_otp_details(otp_data=jsonified_otp_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID `{payload.user_id}`is not found!"
        )
    return OTPDisableFeatureResponseSchema(
        user_id=updated_user["id"],  # type: ignore
        is_otp_enabled=updated_user["is_otp_enabled"],  # type: ignore
        verified_2fa_user=UserResponseSchema(**updated_user),  # type: ignore
    )
