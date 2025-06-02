from uuid import uuid4

from fastapi import HTTPException
from pydantic import BaseModel

from spacegamebackend.application.models.evaluator import (
    StructureBuildRequirementEvaluator,
)
from spacegamebackend.domain.models.research.user_research_repository import (
    UserResearchRepository,
)
from spacegamebackend.domain.models.resource.user_resource_repository import (
    UserResourcesRepository,
)
from spacegamebackend.domain.models.space.entity import Entity
from spacegamebackend.domain.models.structure.structure import Structure
from spacegamebackend.domain.models.structure.structure_status import StructureStatus
from spacegamebackend.domain.models.structure.structure_template import StructureTemplate
from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.domain.models.structure.user_structure_repository import (
    UserStructureRepository,
)
from spacegamebackend.domain.models.user_data_hub import UserDataHub
from spacegamebackend.service.handlers.entity_finder import get_entity
from spacegamebackend.utils.resource_production_component import ResourceProductionComponent
from spacegamebackend.utils.resource_requirement_component import ResourceRequirement


class BuildStructureRequest(BaseModel):
    x: int
    y: int
    entity_id: str
    structure_type: StructureType


class BuildStructureResponse(BaseModel):
    pass


class BuildStructureHandler:
    def __init__(
        self,
        user_resources_repository: UserResourcesRepository,
        user_research_repository: UserResearchRepository,
        user_structure_repository: UserStructureRepository,
    ) -> None:
        self.user_resources_repository = user_resources_repository
        self.user_research_repository = user_research_repository
        self.user_structure_repository = user_structure_repository

    def handle(self, request: BuildStructureRequest, user_id: str) -> BuildStructureResponse:
        entity = get_entity(x=request.x, y=request.y, entity_id=request.entity_id)
        if not entity:
            raise HTTPException(
                status_code=404,
                detail="Entity not found",
            )
        structure_template = StructureTemplate.structure_templates[request.structure_type]
        user_data_hub = UserDataHub(
            user_id=user_id,
            user_resources_repository=self.user_resources_repository,
            user_research_repository=self.user_research_repository,
            user_structure_repository=self.user_structure_repository,
        )
        evaluator = StructureBuildRequirementEvaluator(
            user_data_hub=user_data_hub,
            user_id=user_id,
            entity_id=request.entity_id,
            x=request.x,
            y=request.y,
        )
        if not (
            result := evaluator.evaluate_build(
                structure_template=structure_template,
                with_resources=True,
            )
        ):
            raise HTTPException(status_code=400, detail=result.detail)

        self.handle_resource_changes(user_id, structure_template, user_data_hub)

        self.create_structure(
            request,
            user_id,
            entity,
            structure_template,
        )

        return BuildStructureResponse()

    def create_structure(
        self,
        request: BuildStructureRequest,
        user_id: str,
        entity: Entity,
        structure_template: StructureTemplate,
    ) -> None:
        self.user_structure_repository.add_user_structure(
            user_id=user_id,
            entity_id=request.entity_id,
            x=request.x,
            y=request.y,
            structure=Structure(
                structure_id=uuid4().hex,
                entity_id=entity.entity_id,
                structure_type=request.structure_type,
                level=1,
                structure_status=StructureStatus.P100,
                structure_template=structure_template,
            ),
        )

    def handle_resource_changes(
        self,
        user_id: str,
        structure_template: StructureTemplate,
        user_data_hub: UserDataHub,
    ) -> None:
        current_resources = user_data_hub.get_resources()
        current_resources.update_resources()
        for res_req in structure_template.requirement_components.get_components_of_type(ResourceRequirement):
            cur = current_resources.get_resource(res_req.resource_type)
            current_resources.set_resource(
                res_req.resource_type,
                cur.amount - res_req.value,
                cur.change,
            )
        for res_prod in structure_template.production_components.get_components_of_type(ResourceProductionComponent):
            cur = current_resources.get_resource(res_prod.resource_type)
            current_resources.set_resource(
                res_prod.resource_type,
                cur.amount,
                cur.change + res_prod.value,
            )
        self.user_resources_repository.set_user_resources(user_id=user_id, resources=current_resources)
