from enum import StrEnum, auto
from typing import TYPE_CHECKING

from spacegamebackend.schemas.structures.structure_type import StructureType

if TYPE_CHECKING:
    from spacegamebackend.service.handlers.get_structures_handler import (
        StructureTemplate,
    )


class StructureStatus(StrEnum):
    P100 = auto()
    P90 = auto()
    P80 = auto()
    P70 = auto()
    P60 = auto()
    P50 = auto()
    P40 = auto()
    P30 = auto()
    P20 = auto()
    P10 = auto()
    P0 = auto()


def int_to_roman(level: int) -> str:
    roman_numerals = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]

    result = []
    for value, numeral in roman_numerals:
        while level >= value:
            result.append(numeral)
            level -= value

    return "".join(result)


class Structure:
    def __init__(  # noqa: PLR0913
        self,
        *,
        structure_id: str,
        entity_id: str,
        structure_type: StructureType,
        level: int,
        structure_status: StructureStatus,
        structure_template: "StructureTemplate",
    ) -> None:
        self.category = self.__class__.__qualname__
        self.structure_id = structure_id
        self.entity_id = entity_id
        self.structure_type = structure_type
        self.level = level
        self.structure_status = structure_status
        self.structure_template = structure_template

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "title": self.structure_template.title + " " + int_to_roman(self.level),
            "structure_id": self.structure_id,
            "entity_id": self.entity_id,
            "structure_type": self.structure_type,
            "structure_status": self.structure_status,
            "level": self.level,
            "production_components": [
                component.to_dict(level=self.level)
                for component in self.structure_template.production_components.get_components()
            ],
            "upgrade_components": [
                component.to_dict(level=self.level + 1)
                for component in self.structure_template.build_components.get_components()
            ],
        }
