from typing import Any

from pydantic import BaseModel

from spacegamebackend.application.models.evaluator import (
    StructureBuildRequirementEvaluator,
)
from spacegamebackend.domain.models.eval_result import EvalResult
from spacegamebackend.domain.models.research.user_research_repository import (
    UserResearchRepository,
)
from spacegamebackend.domain.models.resource.user_resource_repository import (
    UserResourcesRepository,
)
from spacegamebackend.domain.models.structure.structure_template import (
    StructureTemplate,
)
from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.domain.models.structure.user_structure_repository import (
    UserStructureRepository,
)
from spacegamebackend.domain.models.user_data_hub import UserDataHub


class GetStructuresRequest(BaseModel):
    x: int
    y: int
    entity_id: str


class GetStructuresResponse(BaseModel):
    structure_templates: list[Any]  # Items that can be built
    built_structures: list[Any]  # Items already built
    other_templates: dict[StructureType, str | None]  # Items that can't be built


class GetStructuresHandler:
    def __init__(
        self,
        *,
        user_resources_repository: UserResourcesRepository,
        user_research_repository: UserResearchRepository,
        user_structure_repository: UserStructureRepository,
    ) -> None:
        self.user_resources_repository = user_resources_repository
        self.user_research_repository = user_research_repository
        self.user_structure_repository = user_structure_repository

    def handle(self, request: GetStructuresRequest, user_id: str) -> GetStructuresResponse:
        built_structures = self.user_structure_repository.get_user_structures(
            user_id=user_id,
            entity_id=request.entity_id,
        )
        matching_templates, other_templates = self.get_matching_building_templates(
            user_id=user_id,
            entity_id=request.entity_id,
            x=request.x,
            y=request.y,
        )
        return GetStructuresResponse(
            built_structures=[
                {
                    **StructureTemplate.get_structure_template(structure.structure_type).to_dict(),
                    **structure.to_dict(),
                }
                for structure in built_structures
            ],
            structure_templates=[template.to_dict() for template in matching_templates],
            other_templates={k: v.detail for k, v in other_templates.items()},
        )

    def get_matching_building_templates(
        self,
        user_id: str,
        entity_id: str,
        x: int,
        y: int,
    ) -> tuple[list[StructureTemplate], dict[StructureType, EvalResult]]:
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
        matching_templates = []
        other_templates = {}
        for template in StructureTemplate.get_structure_templates():
            if not (
                result := evaluator.evaluate_build(
                    structure_template=template,
                    with_resources=True,
                )
            ):
                other_templates[template.structure_type] = result
                continue

            matching_templates.append(template)

        return matching_templates, other_templates
