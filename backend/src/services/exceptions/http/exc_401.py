from fastapi import status
from fastapi.exceptions import HTTPException

from src.services.messages.exceptions.http.exc_details import http_401_unauthorized_details


async def http_exc_401_unauthorized_request() -> Exception:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=http_401_unauthorized_details(),
    )


async def http_exc_401_invalid_credentials_request(authenticate_value: str) -> Exception:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
