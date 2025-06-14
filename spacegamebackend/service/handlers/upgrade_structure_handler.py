from fastapi import HTTPException

from spacegamebackend.application.models.evaluator import (
    StructureBuildRequirementEvaluator,
)
from spacegamebackend.domain.models.research.user_research_repository import (
    UserResearchRepository,
)
from spacegamebackend.domain.models.resource.user_resource_repository import (
    UserResourcesRepository,
)
from spacegamebackend.domain.models.structure.structure_template import (
    StructureTemplate,
)
from spacegamebackend.domain.models.structure.user_structure_repository import (
    UserStructureRepository,
)
from spacegamebackend.domain.models.user_data_hub import UserDataHub
from spacegamebackend.utils.resource_production_component import (
    ResourceProductionComponent,
)
from spacegamebackend.utils.resource_requirement_component import ResourceRequirement


class UpgradeStructureHandler:
    def __init__(
        self,
        user_resources_repository: UserResourcesRepository,
        user_research_repository: UserResearchRepository,
        user_structure_repository: UserStructureRepository,
    ) -> None:
        self.user_resources_repository = user_resources_repository
        self.user_research_repository = user_research_repository
        self.user_structure_repository = user_structure_repository

    def handle(
        self,
        x: int,
        y: int,
        entity_id: str,
        user_id: str,
        structure_id: str,
    ) -> None:
        user_data_hub = UserDataHub(
            user_id=user_id,
            user_resources_repository=self.user_resources_repository,
            user_research_repository=self.user_research_repository,
            user_structure_repository=self.user_structure_repository,
        )
        evaluator = StructureBuildRequirementEvaluator(
            user_data_hub=user_data_hub,
            user_id=user_id,
            entity_id=entity_id,
            x=x,
            y=y,
        )
        structure = user_data_hub.get_structure(structure_id)
        if not (
            result := evaluator.evaluate_upgrade(
                structure_to_upgrade=structure,
                with_resources=True,
            )
        ):
            raise HTTPException(status_code=400, detail=result.detail)

        self.handle_resource_changes(
            user_data_hub,
            user_id,
            structure.structure_template,
            level=structure.level + 1,
        )

        self.upgrade_structure(user_data_hub, structure_id)

    def handle_resource_changes(
        self,
        user_data_hub: UserDataHub,
        user_id: str,
        structure_template: StructureTemplate,
        level: int,
    ) -> None:
        current_resources = user_data_hub.get_resources()
        current_resources.update_resources()
        for res_req in structure_template.requirement_components.get_components_of_type(ResourceRequirement):
            cur = current_resources.get_resource(res_req.resource_type)
            current_resources.set_resource(
                res_req.resource_type,
                cur.amount - res_req.scale(level=level).get_scaled_value(),
                cur.change,
            )
        for res_prod in structure_template.production_components.get_components_of_type(ResourceProductionComponent):
            cur = current_resources.get_resource(res_prod.resource_type)
            current_resources.set_resource(
                res_prod.resource_type,
                cur.amount,
                cur.change + res_prod.get_scaled_value(level),
            )
        self.user_resources_repository.set_user_resources(user_id=user_id, resources=current_resources)

    def upgrade_structure(self, user_data_hub: UserDataHub, structure_id: str) -> None:
        user_data_hub.upgrade_structure(structure_id=structure_id)
