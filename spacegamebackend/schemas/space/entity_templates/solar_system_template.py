from collections.abc import Hashable

from spacegamebackend.schemas.space.component_templates.entities_component_template import (
    EntitiesComponentTemplate,
)
from spacegamebackend.schemas.space.component_templates.structures_component_template import StructuresComponentTemplate
from spacegamebackend.schemas.space.entitites.solar_system import SolarSystem
from spacegamebackend.schemas.space.entity import Entity
from spacegamebackend.schemas.space.entity_template import EntityTemplate
from spacegamebackend.schemas.space.entity_templates.star_template import StarTemplate
from spacegamebackend.schemas.space.entity_templates.terrestial_planet_template import (
    TerrestialPlanetTemplate,
)
from spacegamebackend.schemas.space.seeder import Seeder
from spacegamebackend.schemas.structure_slot_type import StructureSlotType


class SolarSystemTemplate(EntityTemplate):
    def __init__(self) -> None:
        super().__init__(
            component_templates=[
                EntitiesComponentTemplate(
                    title="Primary Entities",
                    entity_templates=[StarTemplate()],
                    min_entities=1,
                    max_entities=3,
                    falloff_factor=0.5,
                ),
                EntitiesComponentTemplate(
                    title="Secondary Entities",
                    entity_templates=[TerrestialPlanetTemplate()],
                    min_entities=0,
                    max_entities=10,
                    falloff_factor=0.5,
                ),
                StructuresComponentTemplate(
                    title="Deep Space Structures",
                    min_structure_slots=10,
                    max_structure_slots=30,
                    structure_type=StructureSlotType.DEEP_SPACE,
                ),
            ],
        )
        self.primary_entity_templates: list[EntityTemplate] = [
            StarTemplate(),
        ]
        self.secondary_entity_templates: list[EntityTemplate] = [
            TerrestialPlanetTemplate(),
        ]

    def generate_entity(self, *, seeder: Seeder, differ: Hashable | None) -> Entity:
        seeder.seed(differ=(differ, self.category, "entity"))
        return SolarSystem(
            entity_id=self.get_entity_id(seeder=seeder, differ=differ),
            components=self.generate_components(seeder=seeder, differ=differ),
        )
