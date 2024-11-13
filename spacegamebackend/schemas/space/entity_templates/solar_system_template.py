from collections.abc import Hashable

from spacegamebackend.schemas.space.component_templates.entities_component_template import (
    EntitiesComponentTemplate,
    WeightedEntityTemplate,
)
from spacegamebackend.schemas.space.component_templates.structures_component_template import (
    DeepSpaceStructuresComponentTemplate,
)
from spacegamebackend.schemas.space.entitites.solar_system import SolarSystem
from spacegamebackend.schemas.space.entity import Entity
from spacegamebackend.schemas.space.entity_template import EntityTemplate
from spacegamebackend.schemas.space.entity_templates.black_hole_template import (
    BlackHoleTemplate,
)
from spacegamebackend.schemas.space.entity_templates.planet_template import (
    PLANET_TEMPLATES,
)
from spacegamebackend.schemas.space.entity_templates.star_template import StarTemplate
from spacegamebackend.schemas.space.seeder import Seeder


class SolarSystemTemplate(EntityTemplate):
    def __init__(self) -> None:
        super().__init__(
            component_templates=[
                EntitiesComponentTemplate(
                    title="Primary Entities",
                    weighted_entity_templates=[
                        WeightedEntityTemplate(weight=100, entity_template=StarTemplate()),
                        WeightedEntityTemplate(weight=1, entity_template=BlackHoleTemplate()),
                    ],
                    min_entities=1,
                    max_entities=5,
                ),
                EntitiesComponentTemplate(
                    title="Secondary Entities",
                    weighted_entity_templates=[
                        WeightedEntityTemplate(weight=1, entity_template=template) for template in PLANET_TEMPLATES
                    ],
                    min_entities=1,
                    max_entities=10,
                ),
                DeepSpaceStructuresComponentTemplate(
                    min_structure_slots=0,
                    max_structure_slots=30,
                ),
            ],
        )

    def generate_entity(self, *, seeder: Seeder, differ: Hashable | None) -> Entity:
        seeder.seed(differ=(differ, self.category, "entity"))
        return SolarSystem(
            entity_id=self.get_entity_id(seeder=seeder, differ=differ),
            components=self.generate_components(seeder=seeder, differ=differ),
        )
