from datetime import datetime
from typing import Literal

from pydantic import constr, EmailStr, Field

from src.schema.base import BaseSchema, PyObjectId


class UserBaseSchema(BaseSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: constr(strip_whitespace=True, min_length=3, to_lower=True) = Field(...)  # type: ignore
    email: EmailStr = Field(...)
    hashed_password: str = Field(...)
    hashed_salt: str = Field(...)
    email_verification_code: str | None = Field(default=None)
    is_otp_enabled: bool = Field(default=False)
    is_otp_verified: bool = Field(default=False)
    otp_base32: str | None = Field(default=None)
    otp_auth_url: str | None = Field(default=None)
    is_verified: bool = Field(default=False)
    is_logged_in: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default=None)

    class Config:
        orm_mode: bool = True
        schema_extra: dict[str, dict[str, str | bool | datetime | None]] = {
            "example": {
                "id": "641a3679c14b677b622db74d",
                "username": "janedoe",
                "email": "jdoe@example.com",
                "hashedPassword": "$2b$12$9CjFLHufR2gPeiP7BpXTKuSGNpHdxJz8rHussxO/Pyedk.jeRx9QC",
                "hashedSalt": "$argon2id$v=19$m=65536,t=3,p=4$YixFSAnBGCPknFOKsRaiFA$CrwSLYToy7/LYVJdHUtY3aEO5Gy5STVDzRH5iMzq34k",
                "emailVerificationCode": "12354qtrq3t2gwegibhwetuh39458zhhgearo98tzhwo98EISHZFP8923wtv4zcq3vc2cwx",
                "isOtpEnabled": False,
                "isOtpVerified": False,
                "otpBase32": None,
                "otpAuthUrl": None,
                "isVerified": False,
                "isLoggedIn": False,
                "created_at": "2023-03-19T14:47:27.468396",
                "updated_at": None,
            }
        }


class UserCreateSchema(BaseSchema):
    username: constr(strip_whitespace=True, min_length=3, to_lower=True) = Field(...)  # type: ignore
    email: EmailStr = Field(...)
    password: constr(min_length=8) = Field(...)  # type: ignore
    repeated_password: constr(min_length=8)  # type: ignore

    class Config:
        schema_extra: dict[str, dict[str, str]] = {
            "example": {
                "username": "janedoe",
                "email": "jdoe@example.com",
                "password": "super-secret!",
                "repeatedPassword": "super-secret!",
            }
        }


class UserLoginSchema(BaseSchema):
    username: constr(strip_whitespace=True, min_length=3, to_lower=True) = Field(...)  # type: ignore
    email: EmailStr = Field(...)
    password: constr(min_length=8) = Field(...)  # type: ignore

    class Config:
        schema_extra: dict[str, dict[str, str]] = {
            "example": {"username": "janedoe", "email": "jdoe@example.com", "password": "super-secret!"}
        }


class UserRegistrationResponseSchema(BaseSchema):
    registration_status: Literal["success", "failed"]
    message: Literal[
        "Registration successful, please verify your email address.",
        "Registration failed, please check your credentials!",
    ]


class UserLogoutResponseSchema(BaseSchema):
    is_logged_in: bool
    is_otp_verified: bool


class UserResponseSchema(BaseSchema):
    id: PyObjectId
    username: constr(strip_whitespace=True, min_length=3, to_lower=True)  # type: ignore
    email: EmailStr
    hashed_password: str
    hashed_salt: str
    email_verification_code: str | None
    is_otp_enabled: bool
    is_otp_verified: bool
    otp_base32: str | None
    otp_auth_url: str | None
    is_verified: bool
    is_logged_in: bool
    created_at: datetime
    updated_at: datetime | None


class UserDeletionResponseSchema(BaseSchema):
    is_user_deleted: bool
