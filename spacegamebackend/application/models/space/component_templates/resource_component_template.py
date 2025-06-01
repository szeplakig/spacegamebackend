from collections.abc import Hashable

from spacegamebackend.application.models.space.components.resource_component import (
    EnergyComponent,
    MineralsComponent,
    ResourceComponent,
)
from spacegamebackend.domain.models.resource.resource_types import ResourceType
from spacegamebackend.domain.models.space.component import Component
from spacegamebackend.domain.models.space.component_template import (
    ComponentTemplate,
)
from spacegamebackend.domain.models.space.seeder import Seeder
from spacegamebackend.utils.generate_gamma_value import generate_gamma_value


class ResourceComponentTemplate(ComponentTemplate):
    def __init__(
        self,
        *,
        title: str,
        min_value: int,
        max_value: int,
        resource_type: ResourceType,
        component_class: type[ResourceComponent],
    ) -> None:
        super().__init__(title=title)
        self.min_value = min_value
        self.max_value = max_value
        self.resource_type = resource_type
        self.component_class = component_class

    def generate_resource_value(self) -> int:
        return generate_gamma_value((self.min_value + self.max_value) / 4, self.min_value)

    def generate_component(self, *, seeder: Seeder, differ: Hashable | None) -> Component:
        seeder.seed(differ=(differ, self.category, "generate_component"))
        return self.component_class(
            title=self.title,
            resource_type=self.resource_type,
            value=self.generate_resource_value(),
        )


class EnergyComponentTemplate(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Energy slots",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.ENERGY,
            component_class=EnergyComponent,
        )


class MineralsComponentTemplate(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Mineral slots",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.MINERALS,
            component_class=MineralsComponent,
        )


class AlloyComponentTemplate(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Alloy slots",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.ALLOYS,
            component_class=ResourceComponent,
        )


class AntimatterComponentTemplate(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Antimatter slots",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.ANTIMATTER,
            component_class=ResourceComponent,
        )


class ResearchComponentTemplate(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Research slots",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.RESEARCH,
            component_class=ResourceComponent,
        )
