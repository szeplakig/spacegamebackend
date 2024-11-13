from collections import Counter
from uuid import uuid4

from fastapi import HTTPException
from pydantic import BaseModel

from spacegamebackend.repositories.user_data_hub import UserDataHub
from spacegamebackend.repositories.user_research_repository import (
    UserResearchRepository,
)
from spacegamebackend.repositories.user_resource_repository import (
    UserResourcesRepository,
)
from spacegamebackend.repositories.user_structure_repository import (
    UserStructureRepository,
)
from spacegamebackend.schemas.space.components.entities_component import (
    EntitiesComponent,
)
from spacegamebackend.schemas.space.components.resource_component import (
    ResourceComponent,
)
from spacegamebackend.schemas.space.entity import Entity
from spacegamebackend.schemas.space.entity_templates.solar_system_template import (
    SolarSystemTemplate,
)
from spacegamebackend.schemas.space.seeder import CoordinateSeeder
from spacegamebackend.schemas.structures.structure import Structure, StructureStatus
from spacegamebackend.schemas.structures.structure_type import StructureType
from spacegamebackend.service.handlers.get_structures_handler import (
    ResourceProductionComponent,
    ResourceRequirement,
    StructureRequirementEvaluator,
    StructureTemplate,
)


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
        seeder = CoordinateSeeder(x=request.x, y=request.y)
        solar_system = SolarSystemTemplate().generate_entity(seeder=seeder, differ=None)
        entity = find_entity(solar_system, request.entity_id)
        if not entity:
            raise HTTPException(status_code=404, detail="Entity not found")
        structure_template = StructureTemplate.structure_templates[request.structure_type]

        user_data_hub = UserDataHub(
            user_id=user_id,
            user_resources_repository=self.user_resources_repository,
            user_research_repository=self.user_research_repository,
            user_structure_repository=self.user_structure_repository,
        )

        # check we have enough resources
        self.validate_structure_resources(
            user_data_hub,
            structure_template=structure_template,
            user_id=user_id,
            entity_id=entity.entity_id,
        )

        user_structures = self.user_structure_repository.get_user_structures(
            user_id=user_id, entity_id=request.entity_id
        )
        self.validate_resource_slots(entity, structure_template, user_structures)

        self.handle_resource_changes(user_id, structure_template, user_data_hub)

        self.create_structure(request, user_id, entity, structure_template)

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
        for res_req in structure_template.build_components.get_components_of_type(ResourceRequirement):
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

    def validate_resource_slots(
        self,
        entity: Entity,
        structure_template: StructureTemplate,
        user_structures: list[Structure],
    ) -> None:
        future_resource_usages = sum(
            (Counter(structure.structure_template.get_resource_type_usages()) for structure in user_structures),
            Counter(structure_template.get_resource_type_usages()),
        )

        resource_slots = Counter(
            {
                component.resource_type: component.value
                for component in entity.components
                if isinstance(component, ResourceComponent)
            }
        )
        print(
            resource_slots,
            future_resource_usages,
            resource_slots > future_resource_usages,
        )
        if future_resource_usages > resource_slots:
            raise HTTPException(
                status_code=400,
                detail="Not enough resources to build structure",
            )

    def validate_structure_resources(
        self,
        user_data_hub: UserDataHub,
        structure_template: StructureTemplate,
        user_id: str,
        entity_id: str,
    ) -> None:
        resource_requirements = structure_template.build_components.get_components_of_type(ResourceRequirement)
        evaluator = StructureRequirementEvaluator(user_data_hub=user_data_hub, user_id=user_id, entity_id=entity_id)
        if not evaluator.evaluate(resource_requirements):
            raise HTTPException(
                status_code=400,
                detail="Not enough resources to build structure",
            )


def find_entity(root_entity: Entity, entity_id: str) -> Entity | None:
    # TODO: studid solution to find entity by id
    if root_entity.entity_id == entity_id:
        return root_entity
    for component in root_entity.components:
        if isinstance(component, EntitiesComponent):
            for entity in component.entities:
                found_entity = find_entity(entity, entity_id)
                if found_entity:
                    return found_entity
    return None
