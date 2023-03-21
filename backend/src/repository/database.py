from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import CollectionInvalid
from pymongo.mongo_client import MongoClient

from src.config.manager import settings


class DBManager:
    def __init__(self, is_atlas: bool = False) -> None:
        self.is_atlas: bool = is_atlas
        self.name: str = "blogcluster1"
        self.uri: str = settings.MONGODB_ATLAS_URI if is_atlas else settings.MONGODB_URI
        self.client: MongoClient = self.__connect_client()
        self.db: Database = self.__create_db()

    def __connect_client(self) -> MongoClient:
        return AsyncIOMotorClient(self.uri)

    def __create_db(self) -> Database:
        if not self.is_atlas:
            return self.client.test
        return self.client[self.name]

    async def create_collections(self, collection_names: list[str]) -> None:
        for collection_name in collection_names:
            try:
                await self.db.create_collection(name=collection_name)  # type: ignore
            except CollectionInvalid:
                logger.info(f"Collection with the name `{collection_name}` already exists!")
                pass

    async def drop_collections(self, collection_names: list[str]) -> None:
        if not self.is_atlas:
            for collection_name in collection_names:
                if self.db[collection_name] is not None:
                    try:
                        await self.db.drop_collection(name_or_collection=collection_name)  # type: ignore
                    except Exception as err:
                        print(err)
                        raise Exception(f"Collection with the name `{collection_name}` never exists!")
        raise Exception("Dropping collections in Atlas is forbidden. Continue without dropping collections.")

    def get_collection(self, collection_name: str) -> Collection:
        return self.db[collection_name]  # type: ignore

    async def drop_db(self) -> None:
        if not self.is_atlas:
            try:
                await self.client.drop_database(name_or_database=self.name)  # type: ignore
            except Exception as err:
                print(err)
                raise Exception(f"The name of the database is either not a string or a None type!")
        raise Exception("Dropping database in Atlas is forbidden. Continue without dropping database.")


def get_db(is_atlas: bool = False) -> DBManager:
    return DBManager(is_atlas=is_atlas)


db_manager = get_db(is_atlas=False)
