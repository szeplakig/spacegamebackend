from collections.abc import Hashable

from spacegamebackend.schemas.space.component_templates.energy_component_template import (
    EnergyComponentTemplate,
)
from spacegamebackend.schemas.space.component_templates.minerals_component_template import (
    MineralsComponentTemplate,
)
from spacegamebackend.schemas.space.component_templates.rare_elements_component_template import (
    RareElementsComponentTemplate,
)
from spacegamebackend.schemas.space.component_templates.structures_component_template import StructuresComponentTemplate
from spacegamebackend.schemas.space.entitites.star import Star
from spacegamebackend.schemas.space.entity import Entity
from spacegamebackend.schemas.space.entity_template import EntityTemplate
from spacegamebackend.schemas.space.seeder import Seeder
from spacegamebackend.schemas.structure_slot_type import StructureSlotType


class StarTemplate(EntityTemplate):
    def __init__(self) -> None:
        super().__init__(
            component_templates=[
                EnergyComponentTemplate(min_value=10, max_value=50),
                MineralsComponentTemplate(min_value=50, max_value=100),
                RareElementsComponentTemplate(min_value=1, max_value=5),
                StructuresComponentTemplate(
                    title="Orbital Structures",
                    min_structure_slots=0,
                    max_structure_slots=200,
                    structure_type=StructureSlotType.ORBITAL,
                ),
            ],
        )

    def generate_entity(self, *, seeder: Seeder, differ: Hashable | None) -> Entity:
        seeder.seed(differ=(differ, self.category, "entity"))
        return Star(
            entity_id=self.get_entity_id(seeder=seeder, differ=differ),
            components=self.generate_components(seeder=seeder, differ=differ),
        )
