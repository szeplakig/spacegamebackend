from datetime import datetime

import jwt
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from spacegamebackend.domain.models.user.user_repository import UserRepository
from spacegamebackend.service.dependencies.user_dependencies import (
    SECRET_KEY,
    AccessTokenV1,
)


class LoginUserRequest(BaseModel):
    email: str
    password: str


class LoginUserResponse(BaseModel):
    id: str
    email: str
    created_at: datetime
    access_token: str


class LoginUserHandler:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def handle(self, login_request: LoginUserRequest) -> LoginUserResponse | None:
        user = self.user_repository.login_user(email=login_request.email, password=login_request.password)
        return (
            LoginUserResponse(
                id=user.id,
                email=user.email,
                created_at=user.created_at,
                access_token=jwt.encode(
                    jsonable_encoder(AccessTokenV1(user_id=user.id).model_dump()),
                    SECRET_KEY,
                    algorithm="HS256",
                ),
            )
            if user
            else None
        )
