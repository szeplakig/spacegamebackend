from typing import TYPE_CHECKING

from spacegamebackend.domain.models.structure.structure_status import StructureStatus
from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.utils.int_to_roman import int_to_roman

if TYPE_CHECKING:
    from spacegamebackend.domain.models.structure.structure_template import (
        StructureTemplate,
    )


class Structure:
    def __init__(
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
                component.scale(level=self.level + 1).to_dict()
                for component in self.structure_template.production_components.get_components()
            ],
            "requirement_components": [
                component.scale(level=self.level + 1).to_dict()
                for component in self.structure_template.requirement_components.get_components()
            ],
        }
