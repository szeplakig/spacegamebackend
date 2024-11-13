from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from spacegamebackend.schemas.structures.structure_type import StructureType
from spacegamebackend.service.dependencies.structure_dependencies import (
    get__build_structure_handler_dependency,
    get__get_strucutres_handler_dependency,
)
from spacegamebackend.service.dependencies.user_dependencies import (
    AccessTokenV1,
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

    return router
