from collections.abc import Hashable

from spacegamebackend.schemas.space.component_templates.resource_component_template import EnergyComponentTemplate
from spacegamebackend.schemas.space.entitites.black_hole import BlackHole
from spacegamebackend.schemas.space.entity import Entity
from spacegamebackend.schemas.space.entity_template import EntityTemplate
from spacegamebackend.schemas.space.seeder import Seeder


class BlackHoleTemplate(EntityTemplate):
    def __init__(self) -> None:
        super().__init__(
            component_templates=[
                EnergyComponentTemplate(min_value=200, max_value=500),
            ],
        )

    def generate_entity(self, *, seeder: Seeder, differ: Hashable | None) -> Entity:
        seeder.seed(differ=(differ, self.category, "entity"))
        return BlackHole(
            entity_id=self.get_entity_id(seeder=seeder, differ=differ),
            components=self.generate_components(seeder=seeder, differ=differ),
        )
