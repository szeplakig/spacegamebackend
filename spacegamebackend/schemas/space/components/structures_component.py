from spacegamebackend.schemas.space.component import Component
from spacegamebackend.schemas.structure_slot_type import StructureSlotType


class StructuresComponent(Component):
    def __init__(self, *, title: str, structure_slots: int, structure_type: StructureSlotType) -> None:
        super().__init__(title=title)
        self.structure_slots = structure_slots
        self.structure_type = structure_type

    def to_dict(self) -> dict:
        return {
            "type": "structures",
            "category": self.category,
            "title": self.title,
            "structure_slots": self.structure_slots,
            "structure_type": self.structure_type,
        }
