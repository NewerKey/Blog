from enum import Enum


class OAuth2BearerCookieScopes(Enum):
    READ_CURRENT_USER: str = "Read all information related to the current user account."  # type: ignore
    UPDATE_CURRENT_USER: str = "Update all information related to the current user account."  # type: ignore
    DELETE_CURRENT_USER: str = "Delete all current user account."  # type: ignore
    WRITE_BLOGS: str = "Write new blogs for the current user account."  # type: ignore
    UPDATE_BLOGS: str = "Update new blogs for the current user account."  # type: ignore
    DELETE_BLOGS: str = "Delete new blogs for the current user account."  # type: ignore
    READ_PREMIUM_BLOGS: str = "Read premium blogs after user account has paid the respective subscription."  # type: ignore
    PAYMENT_TRANSACTION: str = "Carry out transactions for purchasing subscription or a single blog"  # type: ignore


def get_cookie_scopes_dict() -> dict[str, str]:
    scopes: dict[str, str] = dict()
    for data in OAuth2BearerCookieScopes:
        scopes[str(data.name).lower()] = data.value
    return scopes


cookie_scopes = get_cookie_scopes_dict()


def get_cookie_scopes_keys() -> list[str]:
    return [key for key in cookie_scopes.keys()]


cookie_scopes_keys = get_cookie_scopes_keys()
