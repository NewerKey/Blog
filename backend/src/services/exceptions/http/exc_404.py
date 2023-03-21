from fastapi import status
from fastapi.exceptions import HTTPException

from src.services.messages.exceptions.http.exc_details import (
    http_404_email_details,
    http_404_id_details,
    http_404_name_details,
    http_404_username_details,
)


async def http_exc_404_email_not_found_request(email: str) -> Exception:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=http_404_email_details(email=email),
    )


async def http_exc_404_id_not_found_request(id: int) -> Exception:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=http_404_id_details(id=id),
    )


async def http_exc_404_username_not_found_request(username: str) -> Exception:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=http_404_username_details(username=username),
    )


async def http_exc_404_name_not_found_request(name: str) -> Exception:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=http_404_name_details(name=name))
