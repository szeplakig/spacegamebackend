from fastapi import Depends

from spacegamebackend.repositories.user_repository import UserRepository
from spacegamebackend.service.dependencies.user_dependencies import (
    user_repository_dependency,
)
from spacegamebackend.service.handlers.get_login_handler import LoginUserHandler
from spacegamebackend.service.handlers.get_register_handler import RegisterUserHandler
from spacegamebackend.service.handlers.get_system_handler import GetSystemHandler


def get__get_system_handler_dependency() -> GetSystemHandler:
    return GetSystemHandler()


def get__register_user_handler_dependency(
    user_repository: UserRepository = Depends(user_repository_dependency),
) -> RegisterUserHandler:
    return RegisterUserHandler(user_repository)


def get__login_user_handler_dependency(
    user_repository: UserRepository = Depends(user_repository_dependency),
) -> LoginUserHandler:
    return LoginUserHandler(user_repository)
