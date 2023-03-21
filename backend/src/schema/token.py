from datetime import datetime

from src.schema.base import BaseSchema


class TokenResponseSchema(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenDetailSchema(BaseSchema):
    username: str


class TokenRetrievedSchema(BaseSchema):
    username: str
    exp: datetime
    sub: str
    scopes: dict[str, str]


class TokenDataSchema(BaseSchema):
    exp: datetime
    sub: str
    scopes: dict[str, str]
