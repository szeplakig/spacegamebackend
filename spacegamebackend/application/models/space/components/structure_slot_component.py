from spacegamebackend.domain.models.space.component import Component
from spacegamebackend.domain.models.structure.structure_type import StructureType


class StructureSlotComponent(Component):
    def __init__(self, *, title: str, structure_slots: int, allowed_structure_types: set[StructureType]) -> None:
        super().__init__(title=title)
        self.structure_slots = structure_slots
        self.allowed_structure_types = allowed_structure_types

    def to_dict(self) -> dict:
        return {
            "type": "structure_slot",
            "title": self.title,
            "structure_slots": self.structure_slots,
            "allowed_structure_types": list(self.allowed_structure_types),
        }
