from fastapi import APIRouter, Body, Depends, Response

from spacegamebackend.service.dependencies.handler_dependencies import (
    get__login_user_handler_dependency,
    get__register_user_handler_dependency,
)
from spacegamebackend.service.handlers.get_login_handler import (
    LoginUserHandler,
    LoginUserRequest,
    LoginUserResponse,
)
from spacegamebackend.service.handlers.get_register_handler import (
    RegisterUserHandler,
    RegisterUserRequest,
    RegisterUserResponse,
)


def create_user_router() -> APIRouter:
    router = APIRouter()

    @router.post(
        "/v1/users/register",
        response_model=RegisterUserResponse,
        tags=["users"],
    )
    def register_user(
        response: Response,
        user_request: RegisterUserRequest = Body(...),
        handler: RegisterUserHandler = Depends(get__register_user_handler_dependency),
    ) -> RegisterUserResponse:
        register_user_response = handler.handle(user_request)
        response.set_cookie(
            key="access_token",
            value=register_user_response.access_token,
        )
        return register_user_response

    @router.post(
        "/v1/users/login",
        response_model=LoginUserResponse,
        tags=["users"],
    )
    def login_user(
        response: Response,
        login_user_request: LoginUserRequest = Body(...),
        handler: LoginUserHandler = Depends(get__login_user_handler_dependency),
    ) -> LoginUserResponse | None:
        login_user_response = handler.handle(login_user_request)
        if not login_user_response:
            return None
        response.set_cookie(
            key="access_token",
            value=login_user_response.access_token,
        )
        return login_user_response

    return router
