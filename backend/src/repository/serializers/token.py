def serialize_token(token: dict) -> dict[str, str | None]:
    return {"token_type": token["type"], "token": token["token"]}
