from collections.abc import Hashable

from spacegamebackend.schemas.space.component_templates.resource_component_template import (
    AntimatterComponentTemplate,
    EnergyComponentTemplate,
    ResearchPointsComponentTemplate,
)
from spacegamebackend.schemas.space.component_templates.structures_component_template import (
    OrbitalStructuresComponentTemplate,
)
from spacegamebackend.schemas.space.entitites.star import Star
from spacegamebackend.schemas.space.entity import Entity
from spacegamebackend.schemas.space.entity_template import EntityTemplate
from spacegamebackend.schemas.space.seeder import Seeder


class StarTemplate(EntityTemplate):
    def __init__(self) -> None:
        super().__init__(
            component_templates=[
                EnergyComponentTemplate(min_value=10, max_value=200),
                ResearchPointsComponentTemplate(min_value=0, max_value=20),
                AntimatterComponentTemplate(min_value=0, max_value=5),
                OrbitalStructuresComponentTemplate(
                    min_structure_slots=0,
                    max_structure_slots=200,
                ),
            ],
        )

    def generate_entity(self, *, seeder: Seeder, differ: Hashable | None) -> Entity:
        seeder.seed(differ=(differ, self.category, "entity"))
        return Star(
            entity_id=self.get_entity_id(seeder=seeder, differ=differ),
            components=self.generate_components(seeder=seeder, differ=differ),
        )
