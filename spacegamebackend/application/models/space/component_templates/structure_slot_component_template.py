import random
from collections.abc import Hashable

from spacegamebackend.application.models.space.components.structure_slot_component import (
    StructureSlotComponent,
)
from spacegamebackend.domain.models.space.component import Component
from spacegamebackend.domain.models.space.component_template import ComponentTemplate
from spacegamebackend.domain.models.space.seeder import Seeder
from spacegamebackend.domain.models.structure.structure_type import StructureType


class StructureSlotComponentTemplate(ComponentTemplate):
    def __init__(
        self,
        *,
        title: str,
        min_slots: int,
        max_slots: int,
        allowed_structure_types: set[StructureType],
    ) -> None:
        super().__init__(title=title)
        self.min_slots = min_slots
        self.max_slots = max_slots
        self.allowed_structure_types = allowed_structure_types

    def generate_component(self, *, seeder: Seeder, differ: Hashable | None) -> Component:
        seeder.seed(differ=(differ, self.category, "generate_component"))
        return StructureSlotComponent(
            title=self.title,
            structure_slots=random.randint(self.min_slots, self.max_slots),
            allowed_structure_types=self.allowed_structure_types,
        )


class OutpostStructureSlotComponentTemplate(StructureSlotComponentTemplate):
    def __init__(self) -> None:
        super().__init__(
            title="Outpost slot",
            min_slots=1,
            max_slots=1,
            allowed_structure_types={
                StructureType.OUTPOST,
                StructureType.STARTER_OUTPOST,
            },
        )


class OrbitalGovernmentCenterStructureSlotComponentTemplate(StructureSlotComponentTemplate):
    def __init__(self) -> None:
        super().__init__(
            title="Orbital Government Center slot",
            min_slots=1,
            max_slots=1,
            allowed_structure_types={StructureType.ORBITAL_GOVERNMENT_CENTER},
        )


class Tier0SlotComponentTemplate(StructureSlotComponentTemplate):
    def __init__(self, min_slots: int, max_slots: int) -> None:
        super().__init__(
            title="Tier 0 slots",
            min_slots=min_slots,
            max_slots=max_slots,
            allowed_structure_types=StructureType.tier_0(),
        )
