from decouple import config

from src.config.settings.base_settings import AppSettings
from src.config.settings.environment import AppEnvironment


class AppDevelopmentSettings(AppSettings):
    VERSION = config("API_VERSION", cast=str)  # type: ignore
    DESCRIPTION: str = f"[Development Settings] API Application {VERSION} with FastAPI, Docker, and MongoDB."
    DEBUG: bool = config("IS_DEBUG", cast=bool)  # type: ignore
    ENVIRONMENT: AppEnvironment = AppEnvironment.DEVELOPMENT


class AppTestSettings(AppSettings):
    VERSION = config("API_VERSION", cast=str)  # type: ignore
    DESCRIPTION: str = f"[Test Settings] API Application {VERSION} with FastAPI, Docker, and MongoDB."
    DEBUG: bool = config("IS_DEBUG", cast=bool)  # type: ignore
    ENVIRONMENT: AppEnvironment = AppEnvironment.TESTING


class AppProductionSettings(AppSettings):
    ENVIRONMENT: AppEnvironment = AppEnvironment.PRODUCTION
