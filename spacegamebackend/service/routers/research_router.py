from fastapi import APIRouter, Depends

from spacegamebackend.service.dependencies.research_dependencies import (
    get__get_research_forest_handler_dependency,
)
from spacegamebackend.service.dependencies.user_dependencies import (
    AccessTokenV1,
    validate_access_token,
)
from spacegamebackend.service.handlers.get_research_forest import (
    GetResearchForestHandler,
    ResearchForestResponse,
)


def create_research_router() -> APIRouter:
    router = APIRouter(
        tags=["research"],
    )

    @router.get("/v1/research/forest")
    def get_forest(
        access_token: AccessTokenV1 = Depends(validate_access_token),
        handler: GetResearchForestHandler = Depends(get__get_research_forest_handler_dependency),
    ) -> ResearchForestResponse:
        """
        Get the research forest.
        This endpoint returns the research forest, which is a tree structure of all available research types.
        """
        # Placeholder for actual implementation
        return handler.handle(user_id=access_token.user_id)

    return router
