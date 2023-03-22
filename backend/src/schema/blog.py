from datetime import datetime

from pydantic import constr, Field

from src.schema.base import BaseSchema, PyObjectId


class BlogBaseSchema(BaseSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: constr(min_length=1, max_length=128) = Field(...)  # type: ignore
    body: constr(min_length=1, max_length=4096) = Field(...)  # type: ignore
    author_name: str = Field(...)
    author_id: str = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default=None)

    class Config:
        orm_mode: bool = True
        schema_extra: dict[str, dict[str, str | datetime | None]] = {
            "example": {
                "id": "641a3679c14b677b622db74d",
                "title": "Blog Title",
                "body": "Blog Body",
                "authorName": "johndoe",
                "authorId": "13243679c14b677b62132401",
                "created_at": "2023-03-19T14:47:27.468396",
                "updated_at": None,
            }
        }


class BlogCreateSchema(BaseSchema):
    title: constr(min_length=1, max_length=128) = Field(...)  # type: ignore
    body: constr(min_length=1, max_length=4096) = Field(...)  # type: ignore

    class Config:
        orm_mode: bool = True
        schema_extra: dict[str, dict[str, str]] = {
            "example": {
                "title": "Blog Title",
                "body": "Blog Body",
            }
        }


class BlogResponseSchema(BaseSchema):
    id: PyObjectId
    title: constr(min_length=1, max_length=128)  # type: ignore
    body: constr(min_length=1, max_length=4096)  # type: ignore
    author_name: str
    author_id: str
    created_at: datetime
    updated_at: datetime | None


class BlogDeletionResponseSchema(BaseSchema):
    is_blog_deleted: bool


class BlogsResponseSchema(BaseSchema):
    blogs: list[BlogResponseSchema]
