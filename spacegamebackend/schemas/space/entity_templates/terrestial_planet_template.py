from collections.abc import Hashable

from spacegamebackend.schemas.space.component_templates.energy_component_template import (
    EnergyComponentTemplate,
)
from spacegamebackend.schemas.space.component_templates.entities_component_template import (
    EntitiesComponentTemplate,
)
from spacegamebackend.schemas.space.component_templates.minerals_component_template import (
    MineralsComponentTemplate,
)
from spacegamebackend.schemas.space.component_templates.structures_component_template import (
    StructuresComponentTemplate,
)
from spacegamebackend.schemas.space.entitites.terrestial_planet import TerrestialPlanet
from spacegamebackend.schemas.space.entity import Entity
from spacegamebackend.schemas.space.entity_template import EntityTemplate
from spacegamebackend.schemas.space.entity_templates.moon_template import MoonTemplate
from spacegamebackend.schemas.space.seeder import Seeder
from spacegamebackend.schemas.structure_slot_type import StructureSlotType


class TerrestialPlanetTemplate(EntityTemplate):
    def __init__(self) -> None:
        super().__init__(
            component_templates=[
                EnergyComponentTemplate(min_value=2, max_value=5),
                MineralsComponentTemplate(min_value=10, max_value=20),
                EntitiesComponentTemplate(
                    title="Moons",
                    entity_templates=[MoonTemplate()],
                    min_entities=0,
                    max_entities=5,
                    falloff_factor=0.5,
                ),
                StructuresComponentTemplate(
                    title="Orbital Structures",
                    min_structure_slots=10,
                    max_structure_slots=30,
                    structure_type=StructureSlotType.ORBITAL,
                ),
                StructuresComponentTemplate(
                    title="Ground Structures",
                    min_structure_slots=5,
                    max_structure_slots=15,
                    structure_type=StructureSlotType.GROUND,
                ),
            ],
        )

    def generate_entity(self, *, seeder: Seeder, differ: Hashable | None) -> Entity:
        seeder.seed(differ=(differ, self.category, "entity"))
        return TerrestialPlanet(
            entity_id=self.get_entity_id(seeder=seeder, differ=differ),
            components=self.generate_components(seeder=seeder, differ=differ),
        )