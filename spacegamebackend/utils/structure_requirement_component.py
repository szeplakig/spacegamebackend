from dataclasses import dataclass
from enum import StrEnum, auto

from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.utils.requirement_component import RequirementComponent
from spacegamebackend.utils.sortable_component import ComponentKey


class Where(StrEnum):
    LOCAL = auto()
    GLOBAL = auto()


class StructurePrerequisite(RequirementComponent):
    @dataclass(slots=True, frozen=True)
    class Key(ComponentKey):
        structure_type: StructureType
        level: int
        where: Where

    def __init__(self, *, title: str, structure_type: StructureType, level: int, where: Where) -> None:
        super().__init__(title=title)
        self.structure_type = structure_type
        self.level = level
        self.where = where

    def to_dict(self, *, level: int = 1) -> dict:
        return {
            "type": "structure_prerequisite",
            "category": self.category,
            "title": self.title,
            "structure_type": self.structure_type,
            "level": self.level * level,
            "where": self.where,
        }

    def hash_key(self) -> Key:
        return self.Key(self.structure_type, self.level, self.where)
