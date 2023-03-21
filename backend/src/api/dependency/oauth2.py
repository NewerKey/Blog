from src.services.security.auth.oauth2.bearer_cookie import OAuth2PasswordBearerWithCookie
from src.services.security.auth.oauth2.scopes import cookie_scopes


def get_oauth2() -> OAuth2PasswordBearerWithCookie:
    return OAuth2PasswordBearerWithCookie(token_url="api/auth/login", scopes=cookie_scopes)
