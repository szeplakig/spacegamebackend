from typing import ClassVar

from spacegamebackend.domain.models.research.research_type import ResearchType
from spacegamebackend.utils.production_component import (
    ProductionComponent,
    ProductionComponentStore,
)
from spacegamebackend.utils.requirement_component import (
    RequirementComponent,
    RequirementComponentStore,
)


class ResearchTemplate:
    research_options: ClassVar[dict[ResearchType, "ResearchTemplate"]] = {}

    def __init__(  # noqa: PLR0913
        self,
        *,
        research_type: ResearchType,
        title: str,
        description: str,
        tier: int,
        requirement_components: list[RequirementComponent],
        production_components: list[ProductionComponent],
    ) -> None:
        ResearchTemplate.research_options[research_type] = self
        self.category = self.__class__.__qualname__
        self.research_type = research_type
        self.title = title
        self.description = description
        self.tier = tier
        self.requirement_components: RequirementComponentStore = RequirementComponentStore(requirement_components)
        self.production_components: ProductionComponentStore = ProductionComponentStore(production_components)

    def to_dict(self, *, level: int = 1) -> dict:
        return {
            "category": self.category,
            "research_type": self.research_type,
            "title": self.title,
            "description": self.description,
            "tier": self.tier,
            "production_components": [
                component.to_dict(level=level) for component in self.production_components.components.values()
            ],
            "requirement_components": [
                component.to_dict(level=level) for component in self.requirement_components.components.values()
            ],
        }
