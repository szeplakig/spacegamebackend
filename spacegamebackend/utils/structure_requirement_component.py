from dataclasses import dataclass
from enum import StrEnum, auto
from math import floor

from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.utils.requirement_component import RequirementComponent
from spacegamebackend.utils.sortable_component import ComponentKey


class StructureLocationSelector(StrEnum):
    LOCAL = auto()
    GLOBAL = auto()


class StructureRequirement(RequirementComponent):
    @dataclass(slots=True, frozen=True)
    class Key(ComponentKey):
        structure_type: StructureType
        required_structure_level: int
        structure_location_selector: StructureLocationSelector

    def __init__(
        self,
        *,
        title: str,
        structure_type: StructureType,
        required_structure_level: int,
        structure_location_selector: StructureLocationSelector,
        structure_level_scaling: float = 1,
        level: int = 1,
    ) -> None:
        super().__init__(title=title, level=level)
        self.structure_type = structure_type
        self.required_structure_level = required_structure_level
        self.structure_location_selector = structure_location_selector
        self.structure_level_scaling = structure_level_scaling

    def get_scaled_value(self) -> int:
        return self.required_structure_level + floor(self.structure_level_scaling * (self.level - 1))

    def to_dict(self) -> dict:
        return {
            "type": "structure_prerequisite",
            "category": self.category,
            "title": self.title,
            "structure_type": self.structure_type,
            "required_structure_level": self.get_scaled_value(),
            "structure_location_selector": self.structure_location_selector,
            "required_structure_level_scaling": self.structure_level_scaling,
            "level": self.level,
        }

    def scale(self, level: int) -> "StructureRequirement":
        return StructureRequirement(
            title=self.title,
            structure_type=self.structure_type,
            required_structure_level=self.required_structure_level,
            structure_location_selector=self.structure_location_selector,
            structure_level_scaling=self.structure_level_scaling,
            level=level,
        )

    def hash_key(self) -> Key:
        return self.Key(
            self.structure_type,
            self.required_structure_level,
            self.structure_location_selector,
        )
