from hashlib import sha256
from random import randbytes

from fastapi import Request


def generate_registration_token() -> tuple[bytes, str]:
    registration_token = randbytes(10)
    hashed_code = sha256()
    hashed_code.update(registration_token)
    return (registration_token, hashed_code.hexdigest())


def verify_registration_token(token: str) -> str:
    hashed_code = sha256()
    hashed_code.update(bytes.fromhex(token))
    return hashed_code.hexdigest()


def generate_url_token(request: Request, token: bytes) -> str:
    return f"{request.url.scheme}://{request.client.host}:{request.url.port}/api/auth/user-email-verification/{token.hex()}"  # type: ignore
