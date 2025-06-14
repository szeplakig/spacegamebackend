from collections import defaultdict
from typing import ClassVar

from spacegamebackend.domain.models.resource.resource_types import ResourceType
from spacegamebackend.domain.models.space.entity_slot_category import EntitySlotCategory
from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.utils.production_component import (
    ProductionComponent,
    ProductionComponentStore,
)
from spacegamebackend.utils.requirement_component import (
    RequirementComponent,
    RequirementComponentStore,
)
from spacegamebackend.utils.resource_capacity_component import (
    ResourceCapacityComponent,
    ResourceCapacityComponentStore,
)
from spacegamebackend.utils.resource_production_component import (
    ResourceProductionComponent,
)


class StructureTemplate:
    structure_templates: ClassVar[dict[StructureType, "StructureTemplate"]] = {}

    def __init__(  # noqa: PLR0913
        self,
        *,
        structure_type: StructureType,
        title: str,
        description: str,
        tier: int,
        entity_slot_categories: set[EntitySlotCategory],
        requirement_components: list[RequirementComponent],
        production_components: list[ProductionComponent],
        capacity_components: list[ResourceCapacityComponent],
        level: int = 1,
    ) -> None:
        self.category = self.__class__.__qualname__
        self.structure_type = structure_type
        self.title = title
        self.description = description
        self.tier = tier
        self.entity_slot_categories = entity_slot_categories
        self.requirement_components: RequirementComponentStore = RequirementComponentStore(requirement_components)
        self.production_components: ProductionComponentStore = ProductionComponentStore(production_components)
        self.capacity_components: ResourceCapacityComponentStore = ResourceCapacityComponentStore(capacity_components)
        self.level = level

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "structure_type": self.structure_type,
            "title": self.title,
            "description": self.description,
            "tier": self.tier,
            "entity_slot_categories": list(self.entity_slot_categories),
            "production_components": [
                component.to_dict(level=self.level) for component in self.production_components.components.values()
            ],
            "requirement_components": [
                component.to_dict() for component in self.requirement_components.components.values()
            ],
            "capacity_components": [
                component.to_dict(level=self.level) for component in self.capacity_components.components.values()
            ],
            "level": self.level,
        }

    def get_resource_type_usages(
        self,
        level: int,
    ) -> dict[ResourceType, int]:
        usages: dict[ResourceType, int] = defaultdict(int)
        for component in self.production_components.get_components_of_type(ResourceProductionComponent):
            if component.slot_usage > 0:
                usages[component.resource_type] += component.slot_usage * level
        return usages

    def scale(self, *, level: int) -> "StructureTemplate":
        """Scale the structure template to a given level."""
        return StructureTemplate(
            structure_type=self.structure_type,
            title=self.title,
            description=self.description,
            tier=self.tier,
            entity_slot_categories=self.entity_slot_categories,
            requirement_components=[
                component.scale(level=level) for component in self.requirement_components.components.values()
            ],
            production_components=[
                component.scale(level=level) for component in self.production_components.components.values()
            ],
            capacity_components=[
                component.scale(level=level) for component in self.capacity_components.components.values()
            ],
            level=level,
        )

    @classmethod
    def register_structure_template[ST: type](cls, structure_template_class: ST) -> ST:
        structure_template = structure_template_class()
        cls.structure_templates[structure_template.structure_type] = structure_template
        return structure_template_class
