from collections.abc import Hashable

from spacegamebackend.schemas.component_system.component import Component
from spacegamebackend.schemas.component_system.component_template import ComponentTemplate
from spacegamebackend.schemas.resource.types import ResourceType
from spacegamebackend.schemas.space.components.resource_component import (
    EnergyComponent,
    MineralsComponent,
    ResourceComponent,
)
from spacegamebackend.schemas.space.seeder import Seeder
from spacegamebackend.utils import generate_pareto_integer


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
        return generate_pareto_integer(min_value=self.min_value, max_value=self.max_value)

    def generate_component(self, *, seeder: Seeder, differ: Hashable | None) -> Component:
        seeder.seed(differ=(differ, self.category, "component"))
        return self.component_class(
            title=self.title,
            resource_type=self.resource_type,
            value=self.generate_resource_value(),
        )


class EnergyComponentTemplate(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Energy",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.ENERGY,
            component_class=EnergyComponent,
        )


class MineralsComponentTemplate(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Minerals",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.MINERALS,
            component_class=MineralsComponent,
        )


class AlloyComponentTemplate(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Alloys",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.ALLOYS,
            component_class=ResourceComponent,
        )


class FoodComponentTemplate(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Food",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.FOOD,
            component_class=ResourceComponent,
        )


class AntimatterComponentTemplate(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Antimatter",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.ANTIMATTER,
            component_class=ResourceComponent,
        )


class ResearchPointsComponentTemplate(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Research Points",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.RESEARCH,
            component_class=ResourceComponent,
        )


class PopulationComponentTemplate(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Population",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.POPULATION,
            component_class=ResourceComponent,
        )


class AuthorityComponentTemplate(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Authority",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.AUTHORITY,
            component_class=ResourceComponent,
        )
