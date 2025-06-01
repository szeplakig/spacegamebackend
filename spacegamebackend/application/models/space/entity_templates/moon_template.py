from collections.abc import Hashable

from spacegamebackend.application.models.space.component_templates.resource_component_template import (
    EnergyComponentTemplate,
    MineralsComponentTemplate,
)
from spacegamebackend.application.models.space.component_templates.structure_slot_component_template import (
    Tier0SlotComponentTemplate,
)
from spacegamebackend.application.models.space.entitites.moon import Moon
from spacegamebackend.domain.models.space.entity import Entity
from spacegamebackend.domain.models.space.entity_template import EntityTemplate
from spacegamebackend.domain.models.space.seeder import Seeder


class MoonTemplate(EntityTemplate):
    def __init__(self) -> None:
        super().__init__(
            component_templates=[
                Tier0SlotComponentTemplate(
                    min_slots=0,
                    max_slots=2,
                ),
                EnergyComponentTemplate(min_value=0, max_value=10),
                MineralsComponentTemplate(min_value=0, max_value=10),
            ],
        )

    def generate_entity(self, *, seeder: Seeder, differ: Hashable | None) -> Entity:
        seeder.seed(differ=(differ, self.category, "generate_entity"))
        return Moon(
            entity_id=self.get_entity_id(seeder=seeder, differ=differ),
            components=self.generate_components(seeder=seeder, differ=differ),
        )
