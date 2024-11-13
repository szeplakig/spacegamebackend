from collections.abc import Hashable

from spacegamebackend.schemas.space.component_templates.resource_component_template import (
    EnergyComponentTemplate,
    MineralsComponentTemplate,
)
from spacegamebackend.schemas.space.component_templates.structures_component_template import (
    OrbitalStructuresComponentTemplate,
    SurfaceStructuresComponentTemplate,
)
from spacegamebackend.schemas.space.entitites.moon import Moon
from spacegamebackend.schemas.space.entity import Entity
from spacegamebackend.schemas.space.entity_template import EntityTemplate
from spacegamebackend.schemas.space.seeder import Seeder


class MoonTemplate(EntityTemplate):
    def __init__(self) -> None:
        super().__init__(
            component_templates=[
                EnergyComponentTemplate(min_value=0, max_value=2),
                MineralsComponentTemplate(min_value=0, max_value=5),
                OrbitalStructuresComponentTemplate(
                    min_structure_slots=0,
                    max_structure_slots=2,
                ),
                SurfaceStructuresComponentTemplate(
                    min_structure_slots=0,
                    max_structure_slots=10,
                ),
            ],
        )

    def generate_entity(self, *, seeder: Seeder, differ: Hashable | None) -> Entity:
        seeder.seed(differ=(differ, self.category, "entity"))
        return Moon(
            entity_id=self.get_entity_id(seeder=seeder, differ=differ),
            components=self.generate_components(seeder=seeder, differ=differ),
        )
