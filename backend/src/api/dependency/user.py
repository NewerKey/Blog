from datetime import datetime

from bson import ObjectId
from fastapi import Depends
from fastapi.security import SecurityScopes
from jose import JWTError as JoseJWTError
from pydantic import EmailStr, ValidationError

from src.api.dependency.crud import get_crud
from src.api.dependency.oauth2 import get_oauth2
from src.repository.crud.user import UserCRUDRepository
from src.schema.token import TokenRetrievedSchema
from src.schema.user import UserBaseSchema
from src.services.exceptions.http.exc_401 import http_exc_401_invalid_credentials_request
from src.services.security.auth.jwt.token import token_manager


async def get_current_user(
    security_scopes: SecurityScopes,
    user_repo: UserCRUDRepository = Depends(
        dependency=get_crud(repo_type=UserCRUDRepository, collection_name="users")
    ),
    token: str = Depends(get_oauth2()),
) -> UserBaseSchema:
    if security_scopes.scopes:
        authenticate_value = f"Bearer scope='{security_scopes.scope_str}'"
    else:
        authenticate_value = "Bearer"
    try:
        token_data = token_manager.retrieve_token_details(token=token)
        if not token_data:
            raise await http_exc_401_invalid_credentials_request(authenticate_value=authenticate_value)
        retrieved_data = TokenRetrievedSchema(
            username=token_data["username"], exp=token_data["exp"], sub=token_data["sub"], scopes=token_data["scopes"]
        )
    except (JoseJWTError, ValidationError):
        raise await http_exc_401_invalid_credentials_request(authenticate_value=authenticate_value)
    current_user = await user_repo.read_user_by_username(username=retrieved_data.username)
    for scope in security_scopes.scopes:
        if not retrieved_data.scopes.get(scope):
            raise await http_exc_401_invalid_credentials_request(authenticate_value=authenticate_value)
    return UserBaseSchema(_id=current_user["id"], **current_user)  # type: ignore
