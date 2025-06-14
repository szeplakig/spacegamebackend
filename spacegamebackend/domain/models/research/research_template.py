from typing import ClassVar

from spacegamebackend.domain.models.research.research_type import ResearchType
from spacegamebackend.utils.requirement_component import (
    RequirementComponent,
    RequirementComponentStore,
)


class ResearchTemplate:
    research_templates: ClassVar[dict[ResearchType, "ResearchTemplate"]] = {}

    def __init__(
        self,
        *,
        research_type: ResearchType,
        title: str,
        description: str,
        tier: int,
        requirement_components: list[RequirementComponent],
        level: int = 1,
    ) -> None:
        self.category = self.__class__.__qualname__
        self.research_type = research_type
        self.title = title
        self.description = description
        self.tier = tier
        self.requirement_components: RequirementComponentStore = RequirementComponentStore(requirement_components)
        self.level = level

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "research_type": self.research_type,
            "title": self.title,
            "description": self.description,
            "tier": self.tier,
            "requirement_components": [
                component.to_dict() for component in self.requirement_components.components.values()
            ],
        }

    def scale(self, *, level: int) -> "ResearchTemplate":
        """Returns a new ResearchTemplate with scaled requirements."""
        return ResearchTemplate(
            research_type=self.research_type,
            title=self.title,
            description=self.description,
            tier=self.tier,
            requirement_components=[
                component.scale(level=level) for component in self.requirement_components.components.values()
            ],
            level=level,
        )

    @classmethod
    def register_research_template[ST: type](cls, research_template_class: ST) -> ST:
        research_template = research_template_class()
        cls.research_templates[research_template.research_type] = research_template
        return research_template_class
