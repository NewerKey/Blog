from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from src.repository.events import shutdown_db_event_manager, startup_db_event_manager


@asynccontextmanager
async def event_manager(app: FastAPI):
    logger.info(f"Welcome to Pala Blog Application version {app.version} -- Starting . . .")
    await startup_db_event_manager()
    logger.info(f"Pala Blog Application version {app.version} -- Application Successfully Started!")
    yield
    await shutdown_db_event_manager()
    logger.info(f"Pala Blog Application version {app.version} -- Shutting Down . . .")
    logger.info(
        f"Thank you for using Pala Blog Application version {app.version} -- Application Successfully Shutdown!"
    )
