from collections.abc import Hashable

from spacegamebackend.application.models.space.component_templates.resource_component_template import (
    AntimatterComponentTemplate,
    EnergyComponentTemplate,
    ResearchComponentTemplate,
)
from spacegamebackend.application.models.space.component_templates.structure_slot_component_template import (
    StructureSlotaComponentTemplate,
)
from spacegamebackend.application.models.space.entitites.star import Star
from spacegamebackend.domain.models.space.entity import Entity
from spacegamebackend.domain.models.space.entity_template import EntityTemplate
from spacegamebackend.domain.models.space.seeder import Seeder


class StarTemplate(EntityTemplate):
    def __init__(self) -> None:
        super().__init__(
            component_templates=[
                StructureSlotaComponentTemplate(
                    min_slots=1,
                    max_slots=10,
                ),
                EnergyComponentTemplate(min_value=10, max_value=200),
                ResearchComponentTemplate(min_value=0, max_value=50),
                AntimatterComponentTemplate(min_value=0, max_value=10),
            ],
        )

    def generate_entity(self, *, seeder: Seeder, differ: Hashable | None) -> Entity:
        seeder.seed(differ=(differ, self.category, "generate_entity"))
        return Star(
            entity_id=self.get_entity_id(seeder=seeder, differ=differ),
            components=self.generate_components(seeder=seeder, differ=differ),
        )
