import jwt
from fastapi import Cookie, HTTPException
from pydantic import BaseModel
from starlette import status

from spacegamebackend.infra.sqlite_user_repository import SqliteUserRepository
from spacegamebackend.repositories.user_repository import UserRepository

SECRET_KEY = "development"  # noqa: S105


class AccessTokenV1(BaseModel):
    user_id: str


def validate_access_token(access_token: str = Cookie(...)) -> AccessTokenV1:
    try:
        return AccessTokenV1.model_validate(jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"]))
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        ) from e


def user_repository_dependency() -> UserRepository:
    return SqliteUserRepository()
