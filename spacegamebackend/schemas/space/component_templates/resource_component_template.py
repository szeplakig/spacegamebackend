import random
from collections.abc import Hashable

from spacegamebackend.schemas.space.component import Component
from spacegamebackend.schemas.space.component_template import ComponentTemplate
from spacegamebackend.schemas.space.components.resource_component import ResourceComponent
from spacegamebackend.schemas.space.seeder import Seeder


class ResourceComponentTemplate(ComponentTemplate):
    def __init__(
        self, *, title: str, min_value: float, max_value: float, component_class: type[ResourceComponent]
    ) -> None:
        super().__init__(title=title)
        self.min_value = min_value
        self.max_value = max_value
        self.component_class = component_class

    def generate_resource_value(self) -> float:
        return round(random.uniform(self.min_value, self.max_value), 2)

    def generate_component(self, *, seeder: Seeder, differ: Hashable | None) -> Component:
        seeder.seed(differ=(differ, self.category, "component"))
        return self.component_class(
            title=self.title,
            value=self.generate_resource_value(),
        )
