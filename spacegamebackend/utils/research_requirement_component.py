from dataclasses import dataclass

from spacegamebackend.domain.models.research.research_type import ResearchType
from spacegamebackend.utils.requirement_component import RequirementComponent
from spacegamebackend.utils.sortable_component import ComponentKey


class ResearchRequirement(RequirementComponent):
    @dataclass(slots=True, frozen=True)
    class Key(ComponentKey):
        research_type: ResearchType
        research_level: int

    def __init__(self, *, title: str, research_type: ResearchType, level: int) -> None:
        super().__init__(title=title)
        self.research_type = research_type
        self.level = level

    def get_scaled_value(self, level: int) -> int:
        return self.level * level

    def to_dict(self, *, level: int = 1) -> dict:
        return {
            "type": "research_requirement",
            "category": self.category,
            "title": self.title,
            "research_type": self.research_type,
            "research_level": self.get_scaled_value(level),
        }

    def hash_key(self) -> Key:
        return self.Key(self.research_type, self.level)
