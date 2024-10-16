from fastapi import APIRouter, Depends, Query

from spacegamebackend.service.dependencies.handler_dependencies import (
    get__get_system_handler_dependency,
)
from spacegamebackend.service.dependencies.user_dependencies import (
    AccessTokenV1,
    validate_access_token,
)
from spacegamebackend.service.handlers.get_system_handler import (
    GetSystemHandler,
    SystemRequest,
    SystemResponse,
)


def create_system_router() -> APIRouter:
    router = APIRouter()

    @router.get(
        "/v1/systems",
        response_model=SystemResponse,
        tags=["systems"],
    )
    def get_system(
        system_request: SystemRequest = Query(...),
        access_token: AccessTokenV1 = Depends(validate_access_token),
        handler: GetSystemHandler = Depends(get__get_system_handler_dependency),
    ) -> SystemResponse | None:
        print(access_token)
        return handler.handle(system_request)

    return router
