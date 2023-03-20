from datetime import datetime

from pydantic import constr, EmailStr, Field

from src.schema.base import BaseSchema, PyObjectId
from src.services.security.password.manager import pwd_manager


class UserBaseSchema(BaseSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: constr(strip_whitespace=True, min_length=3, to_lower=True) = Field(...)  # type: ignore
    email: EmailStr = Field(...)
    hashed_password: str = Field(...)
    hashed_salt: str = Field(...)
    is_verified: bool = Field(default=False)
    is_logged_in: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default=None)

    class Config:
        orm_mode: bool = True
        schema_extra: dict[str, dict[str, str | bool | datetime | None]] = {
            "example": {
                "username": "janedoe",
                "email": "jdoe@example.com",
                "hashedPassword": "$2b$12$9CjFLHufR2gPeiP7BpXTKuSGNpHdxJz8rHussxO/Pyedk.jeRx9QC",
                "hashedSalt": "$argon2id$v=19$m=65536,t=3,p=4$YixFSAnBGCPknFOKsRaiFA$CrwSLYToy7/LYVJdHUtY3aEO5Gy5STVDzRH5iMzq34k",
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


class UserResponseSchema(BaseSchema):
    id: PyObjectId
    username: constr(strip_whitespace=True, min_length=3, to_lower=True)  # type: ignore
    email: EmailStr
    hashed_password: str
    hashed_salt: str
    is_verified: bool
    is_logged_in: bool
    created_at: datetime
    updated_at: datetime | None
