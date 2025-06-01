from collections.abc import Hashable

from spacegamebackend.application.models.space.component_templates.resource_component_template import (
    AntimatterComponentTemplate,
    EnergyComponentTemplate,
)
from spacegamebackend.application.models.space.entitites.black_hole import BlackHole
from spacegamebackend.domain.models.space.entity import Entity
from spacegamebackend.domain.models.space.entity_template import EntityTemplate
from spacegamebackend.domain.models.space.seeder import Seeder


class BlackHoleTemplate(EntityTemplate):
    def __init__(self) -> None:
        super().__init__(
            component_templates=[
                EnergyComponentTemplate(min_value=0, max_value=500),
                AntimatterComponentTemplate(min_value=0, max_value=20),
            ],
        )

    def generate_entity(self, *, seeder: Seeder, differ: Hashable | None) -> Entity:
        seeder.seed(differ=(differ, self.category, "generate_entity"))
        return BlackHole(
            entity_id=self.get_entity_id(seeder=seeder, differ=differ),
            components=self.generate_components(seeder=seeder, differ=differ),
        )
