from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger


@asynccontextmanager
async def event_manager(app: FastAPI):
    logger.info(f"Welcome to Pala Blog Application version {app.version} -- Starting . . .")
    logger.info(f"Pala Blog Application version {app.version} -- Application Successfully Started!")
    yield
    logger.info(f"Pala Blog Application version {app.version} -- Shutting Down . . .")
    logger.info(
        f"Thank you for using Pala Blog Application version {app.version} -- Application Successfully Shutdown!"
    )
