from datetime import datetime, timedelta

import pytz  # type: ignore
from fastapi import status
from fastapi.exceptions import HTTPException
from jose import jwt as jose_jwt, JWTError as JoseJWTError
from pydantic import ValidationError

from src.config.manager import settings
from src.schema.token import TokenDataSchema, TokenDetailSchema, TokenRetrievedSchema
from src.services.security.auth.oauth2.scopes import cookie_scopes


class TokenManager:
    def __init__(self) -> None:
        pass

    def __generate_token(self, *, token_data: dict[str, str], expiry_delta: timedelta | None = None) -> str:
        to_encode = token_data.copy()

        if expiry_delta:
            expired_at = datetime.utcnow() + expiry_delta
        else:
            expired_at = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN)

        to_encode.update(TokenDataSchema(exp=expired_at, sub=settings.JWT_SUBJECT, scopes=cookie_scopes).dict())
        return jose_jwt.encode(
            claims=to_encode, key=settings.JWT_SECRET_KEY.get_secret_value(), algorithm=settings.JWT_ALGORITHM
        )

    def generate_token(self, username: str, is_refresh: bool = False) -> str:
        if not username:
            raise Exception(f"Invalid username!")

        return self.__generate_token(
            token_data=TokenDetailSchema(username=username).dict(),
            expiry_delta=timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRES_IN if not is_refresh else settings.REFRESH_TOKEN_EXPIRES_IN
            ),
        )

    def retrieve_token_details(self, token: str) -> dict:
        try:
            token_data = jose_jwt.decode(
                token=token, key=settings.JWT_SECRET_KEY.get_secret_value(), algorithms=[settings.JWT_ALGORITHM]
            )
            retrieved_data = TokenRetrievedSchema(
                username=token_data["username"],
                exp=token_data["exp"],
                sub=token_data["sub"],
                scopes=token_data["scopes"],
            )
            if retrieved_data.exp < datetime.now(tz=pytz.UTC):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        except JoseJWTError as decode_error:
            raise ValueError("Unable to decode JWT Token") from decode_error

        except ValidationError as validation_error:
            raise ValueError("Invalid payload in token") from validation_error

        return retrieved_data.dict()


def get_token_manager() -> TokenManager:
    return TokenManager()


token_manager = get_token_manager()
