from datetime import datetime

from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from src.repository.crud.base import BaseCRUDRepository
from src.repository.serializers.blog import serialize_blog
from src.schema.blog import BlogBaseSchema


class BlogCRUDRepository(BaseCRUDRepository):
    def __init__(self, collection_name) -> None:
        super().__init__(collection_name)

    async def create_blog(self, blog_data: dict[str, str]) -> dict[str, str | datetime | ObjectId | None]:
        jsonified_blog_data = jsonable_encoder(obj=BlogBaseSchema(**blog_data))  # type: ignore
        registered_blog = await self.collection.insert_one(jsonified_blog_data)  # type: ignore
        db_blog = await self.collection.find_one({"_id": registered_blog.inserted_id})  # type: ignore
        return serialize_blog(blog=db_blog)

    async def read_all(self) -> list[dict[str, str | datetime | ObjectId | None]]:
        db_blogs = await self.collection.find({"$query": {}, "$orderby": {"createdAt": -1}}).to_list(25)  # type: ignore
        jsonified_blogs = list()
        for blog in db_blogs:
            jsonified_blogs.append(serialize_blog(blog=blog))
        return jsonified_blogs

    async def read_blog_by_id(self, id: str) -> dict[str, str | datetime | ObjectId | None]:
        db_blog = await self.collection.find_one({"_id": id})  # type: ignore
        print(db_blog)
        if not db_blog:
            raise Exception(f"Blog with ID `{id}` is not found!")
        return serialize_blog(blog=db_blog)

    async def delete_blog_by_id(self, id: str) -> bool:
        db_blog = await self.collection.find_one({"_id": jsonable_encoder(obj=id)})  # type: ignore
        if not db_blog:
            raise Exception(f"Blog with ID `{id}` is not found!")

        deleted_blog = await self.collection.delete_one({"_id": db_blog["_id"]})  # type: ignore
        if not deleted_blog:
            raise Exception(f"Blog deletion failed!")
        return True
