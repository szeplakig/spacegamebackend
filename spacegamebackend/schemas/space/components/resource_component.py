from spacegamebackend.schemas.component_system.component import Component
from spacegamebackend.schemas.resource.types import ResourceType


class ResourceComponent(Component):
    def __init__(self, *, title: str, resource_type: ResourceType, value: int) -> None:
        super().__init__(title=title)
        self.resource_type = resource_type
        self.value = value

    def to_dict(self) -> dict:
        return {
            "type": "resource",
            "resource_type": self.resource_type,
            "category": self.category,
            "title": self.title,
            "value": self.value,
        }


class EnergyComponent(ResourceComponent):
    def __init__(self, *, title: str, value: int, resource_type: ResourceType) -> None:
        super().__init__(title=title, resource_type=resource_type, value=value)


class MineralsComponent(ResourceComponent):
    def __init__(self, *, title: str, value: int, resource_type: ResourceType) -> None:
        super().__init__(title=title, resource_type=resource_type, value=value)


class AlloyComponent(ResourceComponent):
    def __init__(self, *, title: str, value: int, resource_type: ResourceType) -> None:
        super().__init__(title=title, resource_type=resource_type, value=value)


class FoodComponent(ResourceComponent):
    def __init__(self, *, title: str, value: int, resource_type: ResourceType) -> None:
        super().__init__(title=title, resource_type=resource_type, value=value)


class AntimatterComponent(ResourceComponent):
    def __init__(self, *, title: str, value: int, resource_type: ResourceType) -> None:
        super().__init__(title=title, resource_type=resource_type, value=value)


class ResearchPointsComponent(ResourceComponent):
    def __init__(self, *, title: str, value: int, resource_type: ResourceType) -> None:
        super().__init__(title=title, resource_type=resource_type, value=value)


class PopulationComponent(ResourceComponent):
    def __init__(self, *, title: str, value: int, resource_type: ResourceType) -> None:
        super().__init__(title=title, resource_type=resource_type, value=value)


class AuthorityComponent(ResourceComponent):
    def __init__(self, *, title: str, value: int, resource_type: ResourceType) -> None:
        super().__init__(title=title, resource_type=resource_type, value=value)
