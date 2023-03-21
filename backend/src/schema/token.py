from pydantic import Field

from src.schema.base import BaseSchema


class TokenBaseSchema(BaseSchema):
    token_type: str | None = Field(default=None)
    token: str | None = Field(default=None)
