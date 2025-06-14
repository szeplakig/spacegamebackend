from collections.abc import Hashable

from spacegamebackend.application.models.space.component_templates.resource_component_template import (
    AntimatterComponentTemplate,
    EnergyComponentTemplate,
    ResearchComponentTemplate,
)
from spacegamebackend.application.models.space.entitites.nebula import Nebula
from spacegamebackend.domain.models.space.entity import Entity
from spacegamebackend.domain.models.space.entity_template import EntityTemplate
from spacegamebackend.domain.models.space.seeder import Seeder


class NebulaTemplate(EntityTemplate):
    def __init__(self) -> None:
        super().__init__(
            component_templates=[
                ResearchComponentTemplate(min_value=30, max_value=100),
                EnergyComponentTemplate(min_value=20, max_value=150),
                AntimatterComponentTemplate(min_value=0, max_value=10),
            ],
        )

    def generate_entity(self, *, seeder: Seeder, differ: Hashable | None) -> Entity:
        seeder.seed(differ=(differ, self.category, "generate_entity"))
        return Nebula(
            entity_id=self.get_entity_id(seeder=seeder, differ=differ),
            components=self.generate_components(seeder=seeder, differ=differ),
        )
