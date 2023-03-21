from loguru import logger

from src.repository.collections import collection_names
from src.repository.database import db_manager


async def drop_collections() -> None:
    logger.info("Database Collections --- Deleting . . .")
    try:
        await db_manager.drop_collections(collection_names=collection_names)
    except Exception:
        pass
    logger.info(f"{len(collection_names)} Database Collections --- Successfully Deleted!")


async def create_collections() -> None:
    if db_manager.is_atlas:
        logger.info("MongoDB Atlas Database Collections --- Creating . . .")
    else:
        logger.info("Local MongoDB Database Collections --- Creating . . .")
    try:
        await db_manager.create_collections(collection_names=collection_names)
    except Exception:
        pass
    else:
        logger.info(f"Successfully Created Collections: \n")
        for idx in range(len(collection_names)):
            logger.info(f"  • Collection {idx + 1}: {collection_names[idx]}")


async def drop_db() -> None:
    logger.info(f"Local MongoDB Database --- Deleting . . .")
    try:
        await db_manager.drop_db()

    except Exception:
        pass
    logger.info(f"Local MongoDB Database `{db_manager.name}` --- Successfully Deleted!")


async def startup_db_event_manager() -> None:
    logger.info("Connection to Asynchronous MongoDB Client via Motor --- Establishing . . .\n")
    logger.info(f"MongoDB Client --- {db_manager.client}\n")
    logger.info("Connection to Asynchronous MongoDB Client via Motor --- Successfully Established!")
    if db_manager.is_atlas:
        logger.info(f"MongoDB Atlas Database --- Accessing . . .\n")
        logger.info(f"MongoDB Atlas Database --- {db_manager.db}\n")
        logger.info(f"MongoDB Atlas Database --- Successfully Accessed!")
    else:
        logger.info(f"Local MongoDB Database --- Creating . . .\n")
        logger.info(f"Local MongoDB Database --- {db_manager.db}\n")
        logger.info(f"Local MongoDB Database --- Successfully Created!")
        await drop_collections()
    await create_collections()


async def shutdown_db_event_manager() -> None:
    if not db_manager.is_atlas:
        await drop_db()
