from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from spacegamebackend.domain.models.research.user_research_repository import (
    UserResearchRepository,
)
from spacegamebackend.domain.models.resource.user_resource_repository import (
    UserResourcesRepository,
)
from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.domain.models.structure.user_structure_repository import (
    UserStructureRepository,
)
from spacegamebackend.domain.models.user_data_hub import UserDataHub
from spacegamebackend.service.dependencies.structure_dependencies import (
    get__build_structure_handler_dependency,
    get__get_strucutres_handler_dependency,
    get__upgrade_structure_handler_dependency,
)
from spacegamebackend.service.dependencies.user_dependencies import (
    AccessTokenV1,
    user_research_repository_dependency,
    user_resources_repository_dependency,
    user_structure_repository_dependency,
    validate_access_token,
)
from spacegamebackend.service.handlers.build_structure_handler import (
    BuildStructureHandler,
    BuildStructureRequest,
    BuildStructureResponse,
)
from spacegamebackend.service.handlers.get_structures_handler import (
    GetStructuresHandler,
    GetStructuresRequest,
    GetStructuresResponse,
)
from spacegamebackend.service.handlers.upgrade_structure_handler import (
    UpgradeStructureHandler,
)


class CoordianteData(BaseModel):
    x: int
    y: int


def create_structures_router() -> APIRouter:
    router = APIRouter()

    @router.get(
        "/v1/entity/{entity_id}/structures",
        response_model=GetStructuresResponse,
        tags=["structures"],
    )
    def get_structures(
        entity_id: str,
        coordinate_data: CoordianteData = Query(...),
        access_token: AccessTokenV1 = Depends(validate_access_token),
        handler: GetStructuresHandler = Depends(get__get_strucutres_handler_dependency),
    ) -> GetStructuresResponse:
        return handler.handle(
            request=GetStructuresRequest(
                x=coordinate_data.x,
                y=coordinate_data.y,
                entity_id=entity_id,
            ),
            user_id=access_token.user_id,
        )

    @router.post(
        "/v1/entity/{entity_id}/structures/{structure_type}",
        response_model=BuildStructureResponse,
        tags=["structures"],
    )
    def build_structure(
        entity_id: str,
        structure_type: StructureType,
        coordinate_data: CoordianteData = Query(...),
        access_token: AccessTokenV1 = Depends(validate_access_token),
        handler: BuildStructureHandler = Depends(get__build_structure_handler_dependency),
    ) -> BuildStructureResponse:
        return handler.handle(
            request=BuildStructureRequest(
                x=coordinate_data.x,
                y=coordinate_data.y,
                entity_id=entity_id,
                structure_type=structure_type,
            ),
            user_id=access_token.user_id,
        )

    @router.put(
        "/v1/entity/{entity_id}/structures/{structure_id}",
        tags=["structures"],
    )
    def upgrade_structure(
        entity_id: str,
        structure_id: str,
        coordinate_data: CoordianteData = Query(...),
        access_token: AccessTokenV1 = Depends(validate_access_token),
        handler: UpgradeStructureHandler = Depends(get__upgrade_structure_handler_dependency),
    ) -> None:
        handler.handle(
            x=coordinate_data.x,
            y=coordinate_data.y,
            entity_id=entity_id,
            user_id=access_token.user_id,
            structure_id=structure_id,
        )

    @router.delete(
        "/v1/structures/{structure_id}",
        tags=["structures"],
    )
    def delete_structure(
        structure_id: str,
        access_token: AccessTokenV1 = Depends(validate_access_token),
        user_resources_repository: UserResourcesRepository = Depends(user_resources_repository_dependency),
        user_research_repository: UserResearchRepository = Depends(user_research_repository_dependency),
        user_structure_repository: UserStructureRepository = Depends(user_structure_repository_dependency),
    ) -> None:
        user_data_hub = UserDataHub(
            user_id=access_token.user_id,
            user_resources_repository=user_resources_repository,
            user_research_repository=user_research_repository,
            user_structure_repository=user_structure_repository,
        )
        user_data_hub.delete_structure(structure_id=structure_id)

    return router
