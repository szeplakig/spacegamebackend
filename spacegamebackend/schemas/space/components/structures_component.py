from spacegamebackend.schemas.component_system.component import Component


class StructuresComponent(Component):
    def __init__(self, *, title: str, structure_slots: int) -> None:
        super().__init__(title=title)
        self.structure_slots = structure_slots

    def to_dict(self) -> dict:
        return {
            "type": "structures",
            "category": self.category,
            "title": self.title,
            "structure_slots": self.structure_slots,
        }
