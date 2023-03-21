from typing import Literal

from src.schema.base import BaseSchema


class EmailVerificationResponse(BaseSchema):
    username: str
    status: Literal["verification successful", "verification failed"]
    is_verified: bool
    is_logged_in: bool
