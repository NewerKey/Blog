from typing import Literal

from pydantic import Field

from src.schema.base import BaseSchema


class TokenBaseSchema(BaseSchema):
    token_type: str | None = Field(default=None)
    token: str | None = Field(default=None)


class TokenEmailVerificationResponse(BaseSchema):
    username: str
    status: Literal["verification successful", "verification failed"]
    is_verified: bool
    is_logged_in: bool
