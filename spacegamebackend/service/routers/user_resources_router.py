from fastapi import APIRouter, Depends

from spacegamebackend.service.dependencies.handler_dependencies import (
    get__get_user_resources_handler_dependency,
    get__time_warp_handler_dependency,
)
from spacegamebackend.service.dependencies.user_dependencies import (
    AccessTokenV1,
    validate_access_token,
)
from spacegamebackend.service.handlers.get_user_resource_handler import (
    GetUserResourcesHandler,
    UserResourcesResponse,
)
from spacegamebackend.service.handlers.time_warp_handler import TimeWarpHandler


def create_user_resources_router() -> APIRouter:
    router = APIRouter()

    @router.get(
        "/v1/resources",
        response_model=UserResourcesResponse,
        tags=["users", "resources"],
    )
    def get_user_resources(
        access_token: AccessTokenV1 = Depends(validate_access_token),
        handler: GetUserResourcesHandler = Depends(get__get_user_resources_handler_dependency),
    ) -> UserResourcesResponse:
        return handler.handle(user_id=access_token.user_id)

    @router.post(
        "/v1/time-warp/{seconds}",
        tags=["users", "resources"],
    )
    def time_warp(
        seconds: int,
        access_token: AccessTokenV1 = Depends(validate_access_token),
        handler: TimeWarpHandler = Depends(get__time_warp_handler_dependency),
    ) -> None:
        return handler.handle(user_id=access_token.user_id, seconds=seconds)

    return router
