from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from src.api.endpoints import router as api_router
from src.config.events import event_manager
from src.config.manager import settings


def initialize_application() -> FastAPI:
    app = FastAPI(lifespan=event_manager, **settings.set_backend_app_attributes)  # type: ignore
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
        allow_origins=settings.ORIGINS,
        allow_methods=settings.METHODS,
        allow_headers=settings.HEADERS,
    )
    app.include_router(router=api_router, prefix=settings.API_PREFIX)
    return app


app: FastAPI = initialize_application()

if __name__ == "__main__":
    run(
        app="main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        workers=settings.SERVER_WORKERS,
        log_level=settings.LOGGING_LEVEL,
    )
