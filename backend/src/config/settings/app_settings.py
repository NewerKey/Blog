from decouple import config

from src.config.settings.base_settings import AppSettings
from src.config.settings.environment import AppEnvironment


class AppDevelopmentSettings(AppSettings):
    API_VERSION = config("API_VERSION", cast=str)  # type: ignore
    DESCRIPTION: str = (
        f"API Version {API_VERSION} -- Development Settings -- Backend Application with FastAPI, Docker, and PyTorch."
    )
    DEBUG: bool = config("IS_DEBUG", cast=bool)  # type: ignore
    ENVIRONMENT: AppEnvironment = AppEnvironment.DEVELOPMENT


class AppTestSettings(AppSettings):
    API_VERSION = config("API_VERSION", cast=str)  # type: ignore
    DESCRIPTION: str = (
        f"API Version {API_VERSION} -- Test Settings -- Backend Application with FastAPI, Docker, and PyTorch."
    )
    DEBUG: bool = config("IS_DEBUG", cast=bool)  # type: ignore
    ENVIRONMENT: AppEnvironment = AppEnvironment.TESTING


class AppProductionSettings(AppSettings):
    ENVIRONMENT: AppEnvironment = AppEnvironment.PRODUCTION
