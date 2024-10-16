from collections.abc import Hashable

from spacegamebackend.schemas.space.component import Component
from spacegamebackend.schemas.space.component_template import ComponentTemplate
from spacegamebackend.schemas.space.components.structures_component import StructuresComponent
from spacegamebackend.schemas.space.seeder import Seeder
from spacegamebackend.schemas.structure_slot_type import StructureSlotType
from spacegamebackend.utils import falloff_distribution


class StructuresComponentTemplate(ComponentTemplate):
    def __init__(
        self,
        *,
        title: str,
        min_structure_slots: int,
        max_structure_slots: int,
        structure_type: StructureSlotType,
    ) -> None:
        super().__init__(title=title)
        self.min_structure_slots = min_structure_slots
        self.max_structure_slots = max_structure_slots
        self.structure_type = structure_type

    def generate_component(self, *, seeder: Seeder, differ: Hashable | None) -> Component:
        seeder.seed(differ=(differ, self.category, "structures_component"))
        return StructuresComponent(
            title=self.title,
            structure_slots=falloff_distribution(self.min_structure_slots, self.max_structure_slots, 0.75),
            structure_type=self.structure_type,
        )
