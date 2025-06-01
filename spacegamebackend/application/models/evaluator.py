from collections import Counter
from collections.abc import Callable, Sequence
from functools import partial
from typing import ClassVar

from spacegamebackend.application.models.space.components.resource_component import (
    ResourceComponent,
)
from spacegamebackend.application.models.space.components.structure_slot_component import (
    StructureSlotComponent,
)
from spacegamebackend.domain.models.eval_result import EvalResult
from spacegamebackend.domain.models.structure.structure import Structure
from spacegamebackend.domain.models.structure.structure_template import (
    StructureTemplate,
)
from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.domain.models.user_data_hub import UserDataHub
from spacegamebackend.service.handlers.entity_finder import (
    get_entity,
    get_entity_checked,
)
from spacegamebackend.utils.production_component import ProductionComponent
from spacegamebackend.utils.requirement_component import RequirementComponent
from spacegamebackend.utils.research_requirement_component import ResearchRequirement
from spacegamebackend.utils.resource_production_component import (
    ResourceProductionComponent,
)
from spacegamebackend.utils.resource_requirement_component import ResourceRequirement
from spacegamebackend.utils.structure_requirement_component import (
    StructurePrerequisite,
    Where,
)


class StructureBuildRequirementEvaluator:
    component_evaluators: ClassVar[
        dict[
            type[RequirementComponent | ProductionComponent],
            Callable[
                [
                    "StructureBuildRequirementEvaluator",
                    RequirementComponent | ProductionComponent,
                    Structure | None,
                ],
                EvalResult,
            ],
        ]
    ] = {}

    def __init__(
        self, user_data_hub: UserDataHub, user_id: str, entity_id: str, x: int, y: int
    ) -> None:
        self.user_data_hub = user_data_hub
        self.user_id = user_id
        self.entity_id = entity_id
        self.x = x
        self.y = y

    def evaluate_build(
        self,
        *,
        structure_template: StructureTemplate,
        with_resources: bool,
    ) -> EvalResult:
        evaluators: list[Callable[[], EvalResult]] = [
            self._evaluate_entity_exists,
            partial(
                self._evaluate_system_has_outpost, structure_template=structure_template
            ),
            partial(
                self._evaluate_components,
                structure_template.requirement_components.get_components(
                    exclude=({ResourceRequirement} if not with_resources else set())
                ),
            ),
            partial(
                self._evaluate_components,
                structure_template.production_components.get_components_of_type(
                    ResourceProductionComponent
                ),
            ),
            partial(
                self._evaluate_structure_slot_categories,
                structure_template=structure_template,
            ),
            partial(
                self._evaluate_structure_type_not_built_on_entity,
                structure_template=structure_template,
            ),
            (
                lambda: (
                    self._evaluate_entity_has_enough_resource_slots(
                        structure_template=structure_template
                    )
                    or self._evaluate_entity_has_enough_structure_slots(
                        structure_template=structure_template,
                    )
                )
            ),
        ]

        for evaluator in evaluators:
            if not (result := evaluator()):
                return result

        return EvalResult(True)

    def evaluate_upgrade(
        self,
        *,
        structure_to_upgrade: Structure,
        with_resources: bool,
    ) -> EvalResult:
        level = 1 if not structure_to_upgrade else structure_to_upgrade.level + 1
        evaluators: list[Callable[[], EvalResult]] = [
            self._evaluate_entity_exists,
            partial(
                self._evaluate_system_has_outpost,
                structure_template=structure_to_upgrade.structure_template,
            ),
            partial(
                self._evaluate_components,
                structure_to_upgrade.structure_template.requirement_components.get_components(
                    exclude=({ResourceRequirement} if not with_resources else set())
                ),
            ),
            partial(
                self._evaluate_components,
                structure_to_upgrade.structure_template.production_components.get_components_of_type(
                    ResourceProductionComponent
                ),
            ),
            partial(
                self._evaluate_structure_slot_categories,
                structure_template=structure_to_upgrade.structure_template,
            ),
            partial(
                self._evaluate_entity_has_enough_resource_slots,
                structure_template=structure_to_upgrade.structure_template,
            ),
        ]

        for evaluator in evaluators:
            if not (result := evaluator()):
                return result

        return EvalResult(True)

    def _evaluate_system_has_outpost(
        self,
        structure_template: StructureTemplate,
    ) -> EvalResult:
        has_outpost = self.user_data_hub.has_structure(
            entity_id=self.entity_id, structure_type=StructureType.OUTPOST
        )
        if has_outpost and structure_template.structure_type is StructureType.OUTPOST:
            return EvalResult(False, "Already has an outpost in the solar system")
        # If the structure is an outpost, we don't need to check for existing outposts
        if structure_template.structure_type is StructureType.OUTPOST:
            return EvalResult(True)
        return EvalResult(False, "No outpost in the solar system")

    def _evaluate_structure_slot_categories(
        self, structure_template: StructureTemplate
    ) -> EvalResult:
        # Check if entity has the required slot categories
        entity = get_entity_checked(x=self.x, y=self.y, entity_id=self.entity_id)
        if not (
            entity.entity_slot_categories & structure_template.entity_slot_categories
        ):
            return EvalResult(
                False, "Entity does not have the required slot categories"
            )
        return EvalResult(True)

    def _evaluate_entity_exists(self) -> EvalResult:
        # Check if the entity exists
        if not get_entity(x=self.x, y=self.y, entity_id=self.entity_id):
            return EvalResult(False, "Entity not found")
        return EvalResult(True)

    def _evaluate_structure_type_not_built_on_entity(
        self, structure_template: StructureTemplate
    ) -> EvalResult:
        # Check if the user already has a structure of the same type
        if any(
            structure.structure_type == structure_template.structure_type
            for structure in self.user_data_hub.get_structures(entity_id=self.entity_id)
        ):
            return EvalResult(False, "Structure already exists")
        return EvalResult(True)

    def _evaluate_entity_has_enough_resource_slots(
        self,
        structure_template: StructureTemplate,
    ) -> EvalResult:
        # Check if the the entity has enough resource slots to build the structure
        structure_resource_usages = Counter(
            structure_template.get_resource_type_usages(level=1)
        )
        if not structure_resource_usages:
            return EvalResult(True)

        entity = get_entity_checked(x=self.x, y=self.y, entity_id=self.entity_id)
        current_resource_usages = sum(
            (
                Counter(
                    structure.structure_template.get_resource_type_usages(
                        structure.level
                    )
                )
                for structure in self.user_data_hub.get_structures(
                    entity_id=self.entity_id
                )
            ),
            Counter(),
        )

        resource_slots = Counter(
            {
                component.resource_type: component.value
                for component in entity.components
                if isinstance(component, ResourceComponent) and component.value > 0
            }
        )

        remaining_resource_slots = resource_slots - current_resource_usages
        for resource, usage in structure_resource_usages.items():
            if remaining_resource_slots[resource] < usage:
                return EvalResult(False, f"Not enough resource slots for {resource}")
        return EvalResult(True)

    def _evaluate_entity_has_enough_structure_slots(
        self,
        structure_template: StructureTemplate,
    ) -> EvalResult:
        entity = get_entity_checked(x=self.x, y=self.y, entity_id=self.entity_id)
        structure_slots_available = 0
        for component in entity.components:
            if (
                isinstance(component, StructureSlotComponent)
                and structure_template.structure_type
                in component.allowed_structure_types
            ):
                structure_slots_available += component.structure_slots
                break

        if structure_slots_available < 1:
            return EvalResult(False, "Not enough building slots")

        current_resource_usages = sum(
            (
                (
                    1
                    if structure.structure_type is structure_template.structure_type
                    else 0
                )
                for structure in self.user_data_hub.get_structures(
                    entity_id=self.entity_id
                )
            ),
        )
        if current_resource_usages >= structure_slots_available:
            return EvalResult(False, "Not enough building slots")

        return EvalResult(True)

    def _evaluate_components(
        self,
        components: Sequence[RequirementComponent | ProductionComponent],
        structure: Structure | None = None,
    ) -> EvalResult:
        return sum(
            (
                self._evaluate_component(component, structure)
                for component in components
            ),
            EvalResult(True),
        )

    def _evaluate_component(
        self,
        component: RequirementComponent | ProductionComponent,
        structure: Structure | None = None,
    ) -> EvalResult:
        for component_type, evaluator in self.component_evaluators.items():
            if isinstance(component, component_type) or issubclass(
                component_type, type(component)
            ):
                return evaluator(self, component, structure)
        raise ValueError(f"No evaluator found for component type {type(component)}")

    @classmethod
    def register_evaluator(
        cls, component_type: type[RequirementComponent | ProductionComponent]
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            cls.component_evaluators[component_type] = func
            return func

        return decorator


@StructureBuildRequirementEvaluator.register_evaluator(ResearchRequirement)
def evaluate_research_requirement(
    evaluator: "StructureBuildRequirementEvaluator",
    component: ResearchRequirement,
    structure: Structure | None = None,
) -> EvalResult:
    research = evaluator.user_data_hub.get_research()
    level = 1 if not structure else structure.level + 1
    if research.get(component.research_type, 0) >= component.get_scaled_value(level):
        return EvalResult(True)
    return EvalResult(
        False,
        (
            f"Missing research {component.research_type} amount {component.get_scaled_value(level=level)}"
        ),
    )


@StructureBuildRequirementEvaluator.register_evaluator(ResourceRequirement)
def evaluate_resource_requirement(
    evaluator: "StructureBuildRequirementEvaluator",
    component: ResourceRequirement,
    structure: Structure | None = None,
) -> EvalResult:
    resources = evaluator.user_data_hub.get_resources()
    level = 1 if not structure else structure.level + 1
    if resources.get_resource(
        component.resource_type
    ).current_amount() >= component.get_scaled_value(level=level):
        return EvalResult(True)
    return EvalResult(
        False,
        (
            f"Missing ({component.get_scaled_value(level=level) - resources.get_resource(
        component.resource_type
    ).amount}) {component.resource_type}"
        ),
    )


@StructureBuildRequirementEvaluator.register_evaluator(StructurePrerequisite)
def evaluate_structure_prerequisite(
    evaluator: "StructureBuildRequirementEvaluator",
    component: StructurePrerequisite,
    structure: Structure | None = None,
) -> EvalResult:
    if component.where is Where.GLOBAL:
        structures = evaluator.user_data_hub.get_all_structures()
    elif component.where is Where.LOCAL:
        structures = evaluator.user_data_hub.get_structures(
            entity_id=evaluator.entity_id
        )
    else:
        raise ValueError(f"Invalid where value {component}")
    level = 1 if not structure else structure.level + 1
    if any(
        structure.structure_type == component.structure_type
        and structure.level >= component.level + level
        for structure in structures
    ):
        return EvalResult(True)
    return EvalResult(
        False,
        f"Missing structure {component.structure_type} level {component.level}",
    )


@StructureBuildRequirementEvaluator.register_evaluator(ResourceProductionComponent)
def evaluate_resource_production_component(
    evaluator: "StructureBuildRequirementEvaluator",
    component: ResourceProductionComponent,
    structure: Structure | None = None,
) -> EvalResult:
    user_resources = evaluator.user_data_hub.get_resources()
    user_resources.update_resources()
    level = 1 if not structure else structure.level + 1
    if (
        user_resources.get_resource(component.resource_type).change
        + component.get_scaled_value(level=level)
        >= 0
    ):
        return EvalResult(True)
    return EvalResult(
        False,
        (
            f"{component.resource_type} production would go below 0 for {component.resource_type} by "
            f"{user_resources.get_resource(component.resource_type).change + component.get_scaled_value(level=level)}"
        ),
    )
