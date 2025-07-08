from fastapi import APIRouter, Depends

from spacegamebackend.domain.models.research.research_type import ResearchType
from spacegamebackend.service.dependencies.research_dependencies import (
    get__get_research_forest_handler_dependency,
    get__get_researches_handler_dependency,
    get__upgrade_research_handler_dependency,
)
from spacegamebackend.service.dependencies.user_dependencies import (
    AccessTokenV1,
    validate_access_token,
)
from spacegamebackend.service.handlers.get_research_forest import (
    GetResearchForestHandler,
    ResearchForestResponse,
)
from spacegamebackend.service.handlers.get_researches_handle import GetResearchesHandler
from spacegamebackend.service.handlers.upgrade_research_handler import (
    UpgradeResearchHandler,
)


def create_research_router() -> APIRouter:
    router = APIRouter(
        tags=["research"],
    )

    @router.get("/v1/research/forest")
    def get_forest(
        access_token: AccessTokenV1 = Depends(validate_access_token),
        handler: GetResearchForestHandler = Depends(get__get_research_forest_handler_dependency),
    ) -> ResearchForestResponse | None:
        return handler.handle(user_id=access_token.user_id)

    @router.get("/v1/research")
    def get_research(
        access_token: AccessTokenV1 = Depends(validate_access_token),
        handler: GetResearchesHandler = Depends(get__get_researches_handler_dependency),
    ) -> dict[ResearchType, int]:
        return handler.handle(user_id=access_token.user_id)

    @router.put("/v1/research/{research_type}")
    def upgrade_research(
        research_type: ResearchType,
        access_token: AccessTokenV1 = Depends(validate_access_token),
        handler: UpgradeResearchHandler = Depends(get__upgrade_research_handler_dependency),
    ) -> None:
        return handler.handle(user_id=access_token.user_id, research_type=research_type)

    return router
