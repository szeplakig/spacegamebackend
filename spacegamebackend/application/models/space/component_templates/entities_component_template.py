import random
from collections.abc import Hashable
from dataclasses import dataclass

from spacegamebackend.application.models.space.components.entities_component import (
    EntitiesComponent,
)
from spacegamebackend.domain.models.space.component import Component
from spacegamebackend.domain.models.space.component_template import (
    ComponentTemplate,
)
from spacegamebackend.domain.models.space.entity_template import EntityTemplate
from spacegamebackend.domain.models.space.seeder import Seeder
from spacegamebackend.utils.generate_gamma_value import generate_gamma_value


@dataclass
class WeightedEntityTemplate:
    entity_template: EntityTemplate
    weight: float = 1


class EntitiesComponentTemplate(ComponentTemplate):
    def __init__(
        self,
        *,
        title: str,
        weighted_entity_templates: list[WeightedEntityTemplate],
        min_entities: int,
        max_entities: int,
    ) -> None:
        super().__init__(title=title)
        self.weighted_entity_templates = weighted_entity_templates
        self.min_entities = min_entities
        self.max_entities = max_entities
        self.entity_templates = [wet.entity_template for wet in self.weighted_entity_templates]
        self.weights = [wet.weight for wet in self.weighted_entity_templates]

    def generate_component(self, *, seeder: Seeder, differ: Hashable | None) -> Component:
        seeder.seed(differ=(differ, self.title, "generate_component"))
        amount = min(
            max(
                generate_gamma_value((self.min_entities + self.max_entities) / 4, self.min_entities),
                self.min_entities,
            ),
            self.max_entities,
        )

        entities = [
            entity_template.generate_entity(seeder=seeder, differ=(i, differ))
            for i, entity_template in enumerate(random.choices(self.entity_templates, weights=self.weights, k=amount))
        ]
        return EntitiesComponent(
            title=self.title,
            entities=entities,
        )
