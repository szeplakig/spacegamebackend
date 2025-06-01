from collections.abc import Hashable

from spacegamebackend.application.models.space.component_templates.entities_component_template import (
    EntitiesComponentTemplate,
    WeightedEntityTemplate,
)
from spacegamebackend.application.models.space.component_templates.resource_component_template import (
    ResearchComponentTemplate,
)
from spacegamebackend.application.models.space.entitites.solar_system import SolarSystem
from spacegamebackend.application.models.space.entity_templates.black_hole_template import (
    BlackHoleTemplate,
)
from spacegamebackend.application.models.space.entity_templates.planet_template import (
    PLANET_TEMPLATES,
)
from spacegamebackend.application.models.space.entity_templates.star_template import (
    StarTemplate,
)
from spacegamebackend.domain.models.space.entity import Entity
from spacegamebackend.domain.models.space.entity_template import EntityTemplate
from spacegamebackend.domain.models.space.seeder import Seeder


class SolarSystemTemplate(EntityTemplate):
    def __init__(self) -> None:
        super().__init__(
            component_templates=[
                ResearchComponentTemplate(min_value=0, max_value=100),
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
            ],
        )

    def generate_entity(self, *, seeder: Seeder, differ: Hashable | None) -> Entity:
        seeder.seed(differ=(differ, self.category, "generate_entity"))
        return SolarSystem(
            entity_id=self.get_entity_id(seeder=seeder, differ=differ),
            components=self.generate_components(seeder=seeder, differ=differ),
        )
