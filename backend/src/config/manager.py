from functools import lru_cache

from decouple import config

from src.config.settings.app_settings import AppDevelopmentSettings, AppProductionSettings, AppTestSettings
from src.config.settings.base_settings import AppSettings
from src.config.settings.environment import AppEnvironment


class AppSettingsFactory:
    def __init__(self, environment: str):
        self.environment = environment

    def __call__(self) -> AppSettings:
        if self.environment == AppEnvironment.DEVELOPMENT.value:
            return AppDevelopmentSettings()
        elif self.environment == AppEnvironment.TESTING.value:
            return AppTestSettings()
        return AppProductionSettings()


@lru_cache()
def get_settings() -> AppSettings:
    return AppSettingsFactory(environment=config("ENVIRONMENT", default="DEV", cast=str))()  # type: ignore


settings: AppSettings = get_settings()
