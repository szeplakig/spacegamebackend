from collections.abc import Hashable

from spacegamebackend.application.models.space.component_templates.resource_component_template import (
    ResearchComponentTemplate,
)
from spacegamebackend.application.models.space.component_templates.structure_slot_component_template import (
    StructureSlotaComponentTemplate,
)
from spacegamebackend.application.models.space.entitites.void import Void
from spacegamebackend.domain.models.space.entity import Entity
from spacegamebackend.domain.models.space.entity_template import EntityTemplate
from spacegamebackend.domain.models.space.seeder import Seeder


class VoidTemplate(EntityTemplate):
    def __init__(self) -> None:
        super().__init__(
            component_templates=[
                ResearchComponentTemplate(min_value=5, max_value=20),
                StructureSlotaComponentTemplate(
                    min_slots=1,
                    max_slots=5,
                ),
            ],
        )

    def generate_entity(self, *, seeder: Seeder, differ: Hashable | None) -> Entity:
        seeder.seed(differ=(differ, self.category, "generate_entity"))
        return Void(
            entity_id=self.get_entity_id(seeder=seeder, differ=differ),
            components=self.generate_components(seeder=seeder, differ=differ),
        )
