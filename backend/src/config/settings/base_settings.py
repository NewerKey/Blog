from logging import INFO
from pathlib import Path

from decouple import config
from pydantic import BaseConfig, BaseSettings, EmailStr, SecretStr


class AppSettings(BaseSettings):
    TITLE: str = "Pala Bog Application"
    VERSION: str = config("API_VERSION", cast=str)  # type: ignore
    TIMEZONE: str = "UTC"
    DESCRIPTION: str = (
        f"API Version {VERSION} -- Production Settings -- Backend Application with FastAPI, Docker, and MongoDB."
    )
    DEBUG: bool = False
    SERVER_HOST: str = config("BACKEND_SERVER_HOST", cast=str)  # type: ignore
    SERVER_PORT: int = config("BACKEND_SERVER_PORT", cast=int)  # type: ignore
    SERVER_WORKERS: int = config("BACKEND_SERVER_WORKERS", cast=int)  # type: ignore
    IS_ALLOWED_CREDENTIALS: bool = config("IS_ALLOWED_CREDENTIALS", cast=bool)  # type: ignore
    ORIGINS: list[str] = [config("ORIGIN", cast=str)]  # type: ignore
    METHODS: list[str] = [config("METHOD", cast=str)]  # type: ignore
    HEADERS: list[str] = [config("HEADER", cast=str)]  # type: ignore

    # Default FastAPI
    API_PREFIX: str = "/api"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    OPENAPI_PREFIX: str = ""

    # Logging
    LOGGING_LEVEL: int = INFO
    LOGGERS: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    # DB
    MONGODB_ATLAS_URI: str = config("MONGODB_ATLAS_URI", cast=str)  # type: ignore
    MONGODB_URI: str = config("MONGODB_URI", cast=str)  # type: ignore

    # Web App Security
    JWT_TOKEN_PREFIX: str = config("JWT_TOKEN_PREFIX", cast=str)  # type: ignore
    JWT_SECRET_KEY: SecretStr = SecretStr(config("JWT_SECRET_KEY", cast=str))  # type: ignore
    JWT_SUBJECT: str = config("JWT_SUBJECT", cast=str)  # type: ignore
    JWT_ALGORITHM: str = config("JWT_ALGORITHM", cast=str)  # type: ignore
    ACCESS_TOKEN_EXPIRES_IN: float = config("ACCESS_TOKEN_EXPIRES_IN", cast=float)  # type: ignore
    REFRESH_TOKEN_EXPIRES_IN: float = config("REFRESH_TOKEN_EXPIRES_IN", cast=float)  # type: ignore

    # Password Security
    BCRYPT_HASHING_ALGORITHM: str = config("BCRYPT_HASHING_ALGORITHM", cast=str)  # type: ignore
    ARGON2_HASHING_ALGORITHM: str = config("ARGON2_HASHING_ALGORITHM", cast=str)  # type: ignore
    SHA256_HASHING_ALGORITHM: str = config("SHA256_HASHING_ALGORITHM", cast=str)  # type: ignore
    SHA512_HASHING_ALGORITHM: str = config("SHA512_HASHING_ALGORITHM", cast=str)  # type: ignore
    HASHING_SALT: str = config("HASHING_SALT", cast=str)  # type: ignore
    PWD_ALGORITHM_LAYER_1: str = config("PWD_ALGORITHM_LAYER_1", cast=str)  # type: ignore
    PWD_ALGORITHM_LAYER_2: str = config("PWD_ALGORITHM_LAYER_2", cast=str)  # type: ignore

    # Authentication, Authorization, & Verification
    MAIL_USERNAME: str = config("MAIL_USERNAME", cast=str)  # type: ignore
    MAIL_PASSWORD: str = config("MAIL_PASSWORD", cast=str)  # type: ignore
    MAIL_FROM: EmailStr = config("MAIL_FROM", cast=str)  # type: ignore
    MAIL_PORT: str = config("MAIL_PORT", cast=str)  # type: ignore
    MAIL_SERVER: str = config("MAIL_SERVER", cast=str)  # type: ignore
    MAIL_FROM_NAME: str = config("MAIL_FROM_NAME", cast=str)  # type: ignore
    IS_MAIL_STARTTLS: bool = config("IS_MAIL_STARTTLS", cast=bool)  # type: ignore
    IS_MAIL_SSL_TLS: bool = config("IS_MAIL_SSL_TLS", cast=bool)  # type: ignore
    IS_MAIL_USE_CREDENTIALS: bool = config("IS_MAIL_USE_CREDENTIALS", cast=bool)  # type: ignore
    IS_MAIL_VALIDATE_CERTS: bool = config("IS_MAIL_VALIDATE_CERTS", cast=bool)  # type: ignore
    TEMPLATE_DIR = Path(__file__).resolve() / Path("backend") / Path(config("TEMPLATE_DIR_NAME", cast=str))  # type: ignore

    class Config(BaseConfig):
        case_sensitive: bool = True
        env_file: str = f"{str(Path(__file__).resolve())}/.env"
        validate_assignment: bool = True

    @property
    def set_backend_app_attributes(self) -> dict[str, str | bool | None]:
        """
        Re-assign all attributes in the `FastAPI` instance.
        """
        return {
            "title": self.TITLE,
            "version": self.VERSION,
            "debug": self.DEBUG,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "api_prefix": self.API_PREFIX,
        }
