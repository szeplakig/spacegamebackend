from typing import ClassVar

from spacegamebackend.domain.models.research.research_type import ResearchType
from spacegamebackend.utils.requirement_component import (
    RequirementComponent,
    RequirementComponentStore,
)
from spacegamebackend.utils.research_requirement_component import ResearchRequirement


class ResearchTemplate:
    research_templates: ClassVar[dict[ResearchType, type["ResearchTemplate"]]] = {}
    research_type: ResearchType

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
        cls.research_templates[research_template_class.research_type] = research_template_class  # type: ignore[attr-defined]
        return research_template_class

    @classmethod
    def get_research_template(cls, research_type: ResearchType) -> "ResearchTemplate":
        return cls.research_templates[research_type]()  # type: ignore[return-value,call-arg]

    def to_research_requirement(
        self, required_research_level: int, research_level_scaling: float
    ) -> RequirementComponent:
        return ResearchRequirement(
            title=self.title,
            research_type=self.research_type,
            required_research_level=required_research_level,
            research_level_scaling=research_level_scaling,
            level=self.level,
        )
