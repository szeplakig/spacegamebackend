from abc import ABC
from dataclasses import dataclass

from spacegamebackend.domain.models.resource.resource_types import ResourceType
from spacegamebackend.utils.component_store import ComponentStore
from spacegamebackend.utils.sortable_component import ComponentKey, SortableComponent


class ResourceCapacityComponent(SortableComponent, ABC):
    @dataclass(frozen=True, slots=True)
    class Key(ComponentKey):
        value: int
        resource_type: ResourceType

    def __init__(self, *, title: str, value: int, resource_type: ResourceType, level: int = 1) -> None:
        self.title = title
        self.category = self.__class__.__qualname__
        self.resource_type = resource_type
        self.level = level
        self.value = value

    def hash_key(self) -> ComponentKey:
        return self.Key(value=self.value, resource_type=self.resource_type)

    def get_scaled_value(self) -> int:
        scaled_value = self.value + self.value * (1.15 ** (self.level - 1))
        magnitude = 10 ** int(len(str(int(abs(scaled_value)))) - 2)
        nice_value = round(scaled_value / magnitude) * magnitude
        return int(nice_value)

    def to_dict(self, *, level: int = 1) -> dict:
        return {
            "category": self.category,
            "title": self.title,
            "value": self.get_scaled_value(),
            "level": level,
        }

    def scale(self, *, level: int) -> "ResourceCapacityComponent":
        return self.__class__(
            value=self.value,
            level=level,
        )  # type: ignore[call-arg]


ResourceCapacityComponentStore = ComponentStore[ResourceCapacityComponent]


class EnergyCapacity(ResourceCapacityComponent):
    def __init__(self, *, value: int, level: int = 1) -> None:
        super().__init__(
            title="Energy Capacity",
            resource_type=ResourceType.ENERGY,
            value=value,
            level=level,
        )


class MineralsCapacity(ResourceCapacityComponent):
    def __init__(self, *, value: int, level: int = 1) -> None:
        super().__init__(
            title="Minerals Capacity",
            resource_type=ResourceType.MINERALS,
            value=value,
            level=level,
        )


class AlloysCapacity(ResourceCapacityComponent):
    def __init__(self, *, value: int, level: int = 1) -> None:
        super().__init__(
            title="Alloys Capacity",
            resource_type=ResourceType.ALLOYS,
            value=value,
            level=level,
        )


class AntimatterCapacity(ResourceCapacityComponent):
    def __init__(self, *, value: int, level: int = 1) -> None:
        super().__init__(
            title="Antimatter Capacity",
            resource_type=ResourceType.ANTIMATTER,
            value=value,
            level=level,
        )


class ResearchCapacity(ResourceCapacityComponent):
    def __init__(self, *, value: int, level: int = 1) -> None:
        super().__init__(
            title="Research Capacity",
            resource_type=ResourceType.RESEARCH,
            value=value,
            level=level,
        )


class AuthorityCapacity(ResourceCapacityComponent):
    def __init__(self, *, value: int, level: int = 1) -> None:
        super().__init__(
            title="Authority Capacity",
            resource_type=ResourceType.AUTHORITY,
            value=value,
            level=level,
        )
