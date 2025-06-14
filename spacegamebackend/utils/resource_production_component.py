from dataclasses import dataclass

from spacegamebackend.domain.models.resource.resource_types import ResourceType
from spacegamebackend.utils.production_component import ProductionComponent
from spacegamebackend.utils.sortable_component import ComponentKey


class ResourceProductionComponent(ProductionComponent):
    @dataclass(slots=True, frozen=True)
    class Key(ComponentKey):
        resource_type: ResourceType
        slot_usage: int

    def __init__(
        self,
        *,
        title: str,
        resource_type: ResourceType,
        slot_usage: int,
        value: int,
        scaling_factor: float = 1,
        level: int = 1,
    ) -> None:
        super().__init__(title=title, level=level)
        self.resource_type = resource_type
        self.slot_usage = slot_usage
        self.value = value
        self.scaling_factor = scaling_factor

    def get_scaled_value(self, level: int) -> int:
        scaled_value = self.value * (self.scaling_factor ** (level - 1))
        magnitude = 10 ** int(len(str(int(abs(scaled_value)))) - 1)
        nice_value = round(scaled_value / magnitude) * magnitude
        return int(nice_value)

    def to_dict(self, *, level: int = 1) -> dict:
        return {
            "type": "resource_production",
            "category": self.category,
            "title": self.title,
            "resource_type": self.resource_type,
            "slot_usage": self.slot_usage,
            "value": self.value,
            "scaling_factor": self.scaling_factor,
            "level": level,
        }

    def hash_key(self) -> Key:
        return self.Key(self.resource_type, self.slot_usage)

    def scale(self, *, level: int) -> "ResourceProductionComponent":
        return ResourceProductionComponent(
            title=self.title,
            resource_type=self.resource_type,
            slot_usage=self.slot_usage * level,
            value=self.get_scaled_value(level),
            scaling_factor=self.scaling_factor,
            level=level,
        )


class EnergyProduction(ResourceProductionComponent):
    def __init__(self, *, value: int, slot_usage: int = 1, scaling_factor: float = 1) -> None:
        super().__init__(
            title="Energy Production",
            resource_type=ResourceType.ENERGY,
            slot_usage=slot_usage,
            value=value if value > 0 else -value,
            scaling_factor=scaling_factor,
        )


class MineralsProduction(ResourceProductionComponent):
    def __init__(self, *, value: int, slot_usage: int = 1, scaling_factor: float = 1) -> None:
        super().__init__(
            title="Minerals Production",
            resource_type=ResourceType.MINERALS,
            slot_usage=slot_usage,
            value=value if value > 0 else -value,
            scaling_factor=scaling_factor,
        )


class AlloysProduction(ResourceProductionComponent):
    def __init__(self, *, value: int, slot_usage: int = 0, scaling_factor: float = 1) -> None:
        super().__init__(
            title="Alloys Production",
            resource_type=ResourceType.ALLOYS,
            slot_usage=slot_usage,
            value=value if value > 0 else -value,
            scaling_factor=scaling_factor,
        )


class ResearchProduction(ResourceProductionComponent):
    def __init__(self, *, value: int, slot_usage: int = 1, scaling_factor: float = 1) -> None:
        super().__init__(
            title="Research Production",
            resource_type=ResourceType.RESEARCH,
            slot_usage=slot_usage,
            value=value if value > 0 else -value,
            scaling_factor=scaling_factor,
        )


class AntimatterProduction(ResourceProductionComponent):
    def __init__(self, *, value: int, slot_usage: int = 1, scaling_factor: float = 1) -> None:
        super().__init__(
            title="Antimatter Production",
            resource_type=ResourceType.ANTIMATTER,
            slot_usage=slot_usage,
            value=value if value > 0 else -value,
            scaling_factor=scaling_factor,
        )


class AuthorityProduction(ResourceProductionComponent):
    def __init__(self, *, value: int, slot_usage: int = 0, scaling_factor: float = 1) -> None:
        super().__init__(
            title="Authority Production",
            resource_type=ResourceType.AUTHORITY,
            slot_usage=slot_usage,
            value=value if value > 0 else -value,
            scaling_factor=scaling_factor,
        )


class EnergyUpkeep(ResourceProductionComponent):
    def __init__(self, *, value: int, slot_usage: int = 0, scaling_factor: float = 1) -> None:
        super().__init__(
            title="Energy Upkeep",
            resource_type=ResourceType.ENERGY,
            slot_usage=slot_usage,
            value=value if value < 0 else -value,
            scaling_factor=scaling_factor,
        )


class AuthorityUpkeep(ResourceProductionComponent):
    def __init__(self, *, value: int, slot_usage: int = 0, scaling_factor: float = 1) -> None:
        super().__init__(
            title="Authority Upkeep",
            resource_type=ResourceType.AUTHORITY,
            slot_usage=slot_usage,
            value=value if value < 0 else -value,
            scaling_factor=scaling_factor,
        )


class MineralsUpkeep(ResourceProductionComponent):
    def __init__(self, *, value: int, slot_usage: int = 0, scaling_factor: float = 1) -> None:
        super().__init__(
            title="Minerals Upkeep",
            resource_type=ResourceType.MINERALS,
            slot_usage=slot_usage,
            value=value if value < 0 else -value,
            scaling_factor=scaling_factor,
        )
