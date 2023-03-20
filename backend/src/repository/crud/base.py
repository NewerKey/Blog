from pymongo.collection import Collection

from src.repository.database import db_manager


class BaseCRUDRepository:
    def __init__(self, collection_name) -> None:
        self.collection: Collection = db_manager.get_collection(collection_name=collection_name)
