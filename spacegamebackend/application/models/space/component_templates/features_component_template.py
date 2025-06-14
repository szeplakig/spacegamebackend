import random
from collections.abc import Hashable
from dataclasses import dataclass

from spacegamebackend.application.models.space.components.features_component import (
    FeaturesComponent,
)
from spacegamebackend.domain.models.space.component import Component
from spacegamebackend.domain.models.space.component_template import (
    ComponentTemplate,
)
from spacegamebackend.domain.models.space.seeder import Seeder
from spacegamebackend.utils.generate_gamma_value import generate_gamma_value


@dataclass
class WeightedComponentTemplate:
    component_template: ComponentTemplate
    weight: float = 1


class FeaturesComponentTemplate(ComponentTemplate):
    def __init__(
        self,
        *,
        title: str,
        weighted_component_templates: list[WeightedComponentTemplate],
        min_components: int,
        max_components: int,
    ) -> None:
        super().__init__(
            title=title,
        )
        self.component_templates = [wet.component_template for wet in weighted_component_templates]
        self.weights = [wet.weight for wet in weighted_component_templates]
        self.min_components = min_components
        self.max_components = max_components

    def generate_component(self, *, seeder: Seeder, differ: Hashable | None) -> Component:
        seeder.seed(differ=(differ, self.title, "generate_component"))
        amount = min(
            max(
                generate_gamma_value((self.min_components + self.max_components) / 4, self.min_components),
                self.min_components,
            ),
            self.max_components,
        )

        components = [
            component_template.generate_component(seeder=seeder, differ=(i, differ))
            for i, component_template in enumerate(
                random.choices(self.component_templates, weights=self.weights, k=amount)
            )
        ]
        return FeaturesComponent(
            title=self.title,
            components=components,
        )
