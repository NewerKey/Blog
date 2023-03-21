from fastapi import status
from fastapi.exceptions import HTTPException

from src.services.messages.exceptions.http.exc_details import http_403_forbidden_details


async def http_exc_403_forbidden_request() -> Exception:
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=http_403_forbidden_details(),
    )
