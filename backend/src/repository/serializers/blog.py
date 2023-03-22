from datetime import datetime

from bson import ObjectId


def serialize_blog(blog: dict) -> dict[str, str | datetime | ObjectId | None]:
    return {
        "id": str(blog["_id"]),
        "title": blog["title"],
        "body": blog["body"],
        "author_name": blog["authorName"],
        "author_id": blog["authorId"],
        "created_at": blog["createdAt"],
        "updated_at": blog["updatedAt"],
    }
