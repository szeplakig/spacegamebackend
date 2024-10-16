import random
from collections.abc import Hashable

from spacegamebackend.schemas.space.component import Component
from spacegamebackend.schemas.space.component_template import ComponentTemplate
from spacegamebackend.schemas.space.components.entities_component import EntitiesComponent
from spacegamebackend.schemas.space.entity_template import EntityTemplate
from spacegamebackend.schemas.space.seeder import Seeder
from spacegamebackend.utils import falloff_distribution


class EntitiesComponentTemplate(ComponentTemplate):
    def __init__(
        self,
        *,
        title: str,
        entity_templates: list[EntityTemplate],
        min_entities: int,
        max_entities: int,
        falloff_factor: float,
    ) -> None:
        super().__init__(title=title)
        self.entity_templates = entity_templates
        self.min_entities = min_entities
        self.max_entities = max_entities
        self.falloff_factor = falloff_factor

    def generate_component(self, *, seeder: Seeder, differ: Hashable | None) -> Component:
        seeder.seed(differ=(differ, self.category, "entities_component"))
        return EntitiesComponent(
            title=self.title,
            entities=[
                random.choice(self.entity_templates).generate_entity(seeder=seeder, differ=(i, differ))
                for i in range(falloff_distribution(self.min_entities, self.max_entities, self.falloff_factor))
            ],
        )
