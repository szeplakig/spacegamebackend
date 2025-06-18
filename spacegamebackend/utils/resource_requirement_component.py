from dataclasses import dataclass

from spacegamebackend.domain.models.resource.resource_types import ResourceType
from spacegamebackend.utils.requirement_component import RequirementComponent
from spacegamebackend.utils.sortable_component import ComponentKey


class ResourceRequirement(RequirementComponent):
    @dataclass(slots=True, frozen=True)
    class Key(ComponentKey):
        resource_type: ResourceType

    def __init__(
        self,
        *,
        title: str,
        resource_type: ResourceType,
        value: int,
        scaling_factor: float,
        level: int = 1,
    ) -> None:
        super().__init__(title=title, level=level)
        self.resource_type = resource_type
        self.value = value
        self.scaling_factor = scaling_factor

    def get_scaled_value(self) -> int:
        scaled_value = self.value + self.value * (self.scaling_factor ** (self.level - 1))
        magnitude = 10 ** int(len(str(int(abs(scaled_value)))) - 2)
        nice_value = round(scaled_value / magnitude) * magnitude
        return int(nice_value)

    def to_dict(self) -> dict:
        return {
            "type": "resource_requirement",
            "category": self.category,
            "title": self.title,
            "resource_type": self.resource_type,
            "value": self.get_scaled_value(),
            "scaling_factor": self.scaling_factor,
            "level": self.level,
        }

    def scale(self, level: int) -> "ResourceRequirement":
        return ResourceRequirement(
            title=self.title,
            resource_type=self.resource_type,
            value=self.value,
            scaling_factor=self.scaling_factor,
            level=level,
        )

    def hash_key(self) -> Key:
        return self.Key(
            self.resource_type,
        )

    def __repr__(self) -> str:
        return f"{self.title} ({self.resource_type.name}): {self.get_scaled_value()} at level {self.level}"


class MineralCost(ResourceRequirement):
    def __init__(self, *, value: int, scaling_factor: float = 1.3) -> None:
        super().__init__(
            title="Mineral Cost",
            resource_type=ResourceType.MINERALS,
            value=value,
            scaling_factor=scaling_factor,
        )


class EnergyCost(ResourceRequirement):
    def __init__(self, *, value: int, scaling_factor: float = 1.3) -> None:
        super().__init__(
            title="Energy Cost",
            resource_type=ResourceType.ENERGY,
            value=value,
            scaling_factor=scaling_factor,
        )


class AlloysCost(ResourceRequirement):
    def __init__(self, *, value: int, scaling_factor: float = 1.3) -> None:
        super().__init__(
            title="Alloy Cost",
            resource_type=ResourceType.ALLOYS,
            value=value,
            scaling_factor=scaling_factor,
        )


class AntimatterCost(ResourceRequirement):
    def __init__(self, *, value: int, scaling_factor: float = 1.3) -> None:
        super().__init__(
            title="Antimatter Cost",
            resource_type=ResourceType.ANTIMATTER,
            value=value,
            scaling_factor=scaling_factor,
        )


class ResearchCost(ResourceRequirement):
    def __init__(self, *, value: int, scaling_factor: float = 1.3) -> None:
        super().__init__(
            title="Research Cost",
            resource_type=ResourceType.RESEARCH,
            value=value,
            scaling_factor=scaling_factor,
        )


class AuthorityCost(ResourceRequirement):
    def __init__(self, *, value: int, scaling_factor: float = 1.3) -> None:
        super().__init__(
            title="Authority Cost",
            resource_type=ResourceType.AUTHORITY,
            value=value,
            scaling_factor=scaling_factor,
        )
