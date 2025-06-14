from dataclasses import dataclass

from spacegamebackend.domain.models.research.research_type import ResearchType
from spacegamebackend.utils.requirement_component import RequirementComponent
from spacegamebackend.utils.sortable_component import ComponentKey


class ResearchRequirement(RequirementComponent):
    @dataclass(slots=True, frozen=True)
    class Key(ComponentKey):
        research_type: ResearchType
        required_research_level: int

    def __init__(
        self,
        *,
        title: str,
        research_type: ResearchType,
        required_research_level: int,
        research_level_scaling: int = 1,
        level: int = 1,
    ) -> None:
        super().__init__(title=title)
        self.research_type = research_type
        self.required_research_level = required_research_level
        self.research_level_scaling = research_level_scaling
        self.level = level

    def get_scaled_value(self) -> int:
        return self.required_research_level + self.level * self.research_level_scaling

    def to_dict(self) -> dict:
        return {
            "type": "research_requirement",
            "category": self.category,
            "title": self.title,
            "research_type": self.research_type,
            "required_research_level": self.get_scaled_value(),
            "research_level_scaling": self.research_level_scaling,
            "level": self.level,
        }

    def hash_key(self) -> Key:
        return self.Key(self.research_type, self.required_research_level)

    def scale(self, level: int) -> "ResearchRequirement":
        return ResearchRequirement(
            title=self.title,
            research_type=self.research_type,
            required_research_level=self.required_research_level,
            level=level,
        )
