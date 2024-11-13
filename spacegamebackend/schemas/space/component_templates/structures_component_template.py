from collections.abc import Hashable

from spacegamebackend.schemas.component_system.component import Component
from spacegamebackend.schemas.component_system.component_template import (
    ComponentTemplate,
)
from spacegamebackend.schemas.space.components.structures_component import (
    StructuresComponent,
)
from spacegamebackend.schemas.space.seeder import Seeder
from spacegamebackend.utils import generate_pareto_integer


class StructuresComponentTemplate(ComponentTemplate):
    def __init__(
        self,
        *,
        title: str,
        min_structure_slots: int,
        max_structure_slots: int,
    ) -> None:
        super().__init__(title=title)
        self.min_structure_slots = min_structure_slots
        self.max_structure_slots = max_structure_slots

    def generate_component(self, *, seeder: Seeder, differ: Hashable | None) -> Component:
        seeder.seed(differ=(differ, self.category, "structures_component"))
        return StructuresComponent(
            title=self.title,
            structure_slots=generate_pareto_integer(
                min_value=self.min_structure_slots, max_value=self.max_structure_slots
            ),
        )


class SurfaceStructuresComponentTemplate(StructuresComponentTemplate):
    def __init__(self, *, min_structure_slots: int, max_structure_slots: int) -> None:
        super().__init__(
            title="Surface Structure",
            min_structure_slots=min_structure_slots,
            max_structure_slots=max_structure_slots,
        )


class OrbitalStructuresComponentTemplate(StructuresComponentTemplate):
    def __init__(self, *, min_structure_slots: int, max_structure_slots: int) -> None:
        super().__init__(
            title="Orbital Structure",
            min_structure_slots=min_structure_slots,
            max_structure_slots=max_structure_slots,
        )


class DeepSpaceStructuresComponentTemplate(StructuresComponentTemplate):
    def __init__(self, *, min_structure_slots: int, max_structure_slots: int) -> None:
        super().__init__(
            title="Deep Space Structure",
            min_structure_slots=min_structure_slots,
            max_structure_slots=max_structure_slots,
        )
