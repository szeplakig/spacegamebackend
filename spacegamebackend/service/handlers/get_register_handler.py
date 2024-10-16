from datetime import datetime

import jwt
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from spacegamebackend.repositories.user_repository import UserRepository
from spacegamebackend.service.dependencies.user_dependencies import (
    SECRET_KEY,
    AccessTokenV1,
)


class RegisterUserRequest(BaseModel):
    email: str
    password: str


class RegisterUserResponse(BaseModel):
    id: str
    email: str
    created_at: datetime
    access_token: str


class RegisterUserHandler:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def handle(self, user_request: RegisterUserRequest) -> RegisterUserResponse:
        user = self.user_repository.register_user(email=user_request.email, password=user_request.password)
        return RegisterUserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at,
            access_token=jwt.encode(
                jsonable_encoder(AccessTokenV1(user_id=user.id).model_dump()),
                SECRET_KEY,
                algorithm="HS256",
            ),
        )
