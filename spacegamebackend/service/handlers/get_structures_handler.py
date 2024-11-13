from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, ClassVar

from pydantic import BaseModel

from spacegamebackend.repositories.user_data_hub import UserDataHub
from spacegamebackend.repositories.user_research_repository import (
    UserResearchRepository,
)
from spacegamebackend.repositories.user_resource_repository import (
    UserResourcesRepository,
)
from spacegamebackend.repositories.user_structure_repository import (
    UserStructureRepository,
)
from spacegamebackend.schemas.research.research_type import ResearchType
from spacegamebackend.schemas.resource.types import ResourceType
from spacegamebackend.schemas.structures.structure import Structure
from spacegamebackend.schemas.structures.structure_type import StructureType


class ComponentKey:
    pass


class SortableComponent(ABC):
    @abstractmethod
    def hash_key(self) -> ComponentKey:
        pass


# Requirement components
class StructureRequirementComponent(SortableComponent, ABC):
    """Base class for components that represent requirements for building a structure.
    This can include resource costs, research requirements, or other prerequisites."""

    def __init__(self, *, title: str) -> None:
        self.title = title
        self.category = self.__class__.__qualname__

    @abstractmethod
    def to_dict(self, *, level: int = 1) -> dict:
        pass


class StructureRequirementEvaluator:
    component_evaluators: ClassVar[
        dict[type[StructureRequirementComponent], Callable]
    ] = {}

    def __init__(
        self, user_data_hub: UserDataHub, user_id: str, entity_id: str
    ) -> None:
        self.user_data_hub = user_data_hub
        self.user_id = user_id
        self.entity_id = entity_id

    def evaluate(self, components: Sequence[StructureRequirementComponent]) -> bool:
        return all(self.evaluate_component(component) for component in components)

    def evaluate_component(self, component: StructureRequirementComponent) -> bool:
        evaluator = self.component_evaluators[type(component)]
        return evaluator(self, component)

    @classmethod
    def register_evaluator(
        cls, component_type: type[StructureRequirementComponent]
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            cls.component_evaluators[component_type] = func
            return func

        return decorator


class ResearchRequirement(StructureRequirementComponent):
    @dataclass(slots=True, frozen=True)
    class Key(ComponentKey):
        research_type: ResearchType
        level: int

    def __init__(self, *, title: str, research_type: ResearchType, level: int) -> None:
        super().__init__(title=title)
        self.research_type = research_type
        self.level = level

    def to_dict(self, *, level: int = 1) -> dict:
        return {
            "type": "research_requirement",
            "category": self.category,
            "title": self.title,
            "research_type": self.research_type,
            "level": self.level,
        }

    def hash_key(self) -> Key:
        return self.Key(self.research_type, self.level)


class ResourceRequirement(StructureRequirementComponent):
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
    ) -> None:
        super().__init__(title=title)
        self.resource_type = resource_type
        self.value = value
        self.scaling_factor = scaling_factor

    def get_scaled_value(self, level: int) -> int:
        # Scale the input value
        scaled_value = self.value * (self.scaling_factor**level)

        # Find the order of magnitude (power of 10)
        magnitude = 10 ** int(len(str(int(scaled_value))) - 1)

        # Round to the nearest "nice" value
        nice_value = round(scaled_value / magnitude) * magnitude

        return int(nice_value)

    def to_dict(self, *, level: int = 1) -> dict:
        return {
            "type": "resource_requirement",
            "category": self.category,
            "title": self.title,
            "resource_type": self.resource_type,
            "value": self.get_scaled_value(level),
        }

    def hash_key(self) -> Key:
        return self.Key(
            self.resource_type,
        )


class StructurePrerequisite(StructureRequirementComponent):
    @dataclass(slots=True, frozen=True)
    class Key(ComponentKey):
        structure_type: StructureType
        level: int

    def __init__(
        self, *, title: str, structure_type: StructureType, level: int
    ) -> None:
        super().__init__(title=title)
        self.structure_type = structure_type
        self.level = level

    def to_dict(self, *, level: int = 1) -> dict:
        return {
            "type": "structure_prerequisite",
            "category": self.category,
            "title": self.title,
            "structure_type": self.structure_type,
            "level": self.level,
        }

    def hash_key(self) -> Key:
        return self.Key(self.structure_type, self.level)


@StructureRequirementEvaluator.register_evaluator(ResearchRequirement)
def evaluate_research_requirement(
    evaluator: "StructureRequirementEvaluator", component: "ResearchRequirement"
) -> bool:
    research = evaluator.user_data_hub.get_research()
    return research.get(component.research_type, 0) >= component.level


@StructureRequirementEvaluator.register_evaluator(ResourceRequirement)
def evaluate_resource_requirement(
    evaluator: "StructureRequirementEvaluator", component: "ResourceRequirement"
) -> bool:
    resources = evaluator.user_data_hub.get_resources()
    return resources.get_resource(
        component.resource_type
    ).amount >= component.get_scaled_value(level=1)


@StructureRequirementEvaluator.register_evaluator(StructurePrerequisite)
def evaluate_structure_prerequisite(
    evaluator: "StructureRequirementEvaluator", component: "StructurePrerequisite"
) -> bool:
    structures = evaluator.user_data_hub.get_all_structures()
    return any(
        structure.structure_type == component.structure_type
        and structure.level >= component.level
        for structure in structures
    )


class StructureProductionComponent(SortableComponent, ABC):
    """Any component that takes efect while the structure is built and working.
    So upkeep, generation of resources or any other effect that happens over time."""

    def __init__(self, *, title: str) -> None:
        self.title = title
        self.category = self.__class__.__qualname__

    @abstractmethod
    def to_dict(self, *, level: int = 1) -> dict:
        pass


class ResourceProductionComponent(StructureProductionComponent):
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
        scaling_factor: float,
    ) -> None:
        super().__init__(title=title)
        self.resource_type = resource_type
        self.slot_usage = slot_usage
        self.value = value
        self.scaling_factor = scaling_factor

    def get_scaled_value(self, level: int) -> int:
        value = self.value * (self.scaling_factor ** (level - 1))
        return int(round(value))

    def to_dict(self, *, level: int = 1) -> dict:
        return {
            "type": "resource_production",
            "category": self.category,
            "title": self.title,
            "resource_type": self.resource_type,
            "slot_usage": self.slot_usage,
            "value": self.value,
            "scaling_factor": self.scaling_factor,
        }

    def hash_key(self) -> Key:
        return self.Key(self.resource_type, self.slot_usage)


class EnergyUpkeep(ResourceProductionComponent):
    def __init__(self, *, value: int, scaling_factor: float) -> None:
        super().__init__(
            title="Energy Upkeep",
            resource_type=ResourceType.ENERGY,
            slot_usage=0,
            value=value,
            scaling_factor=scaling_factor,
        )


class ComponentStore[C: SortableComponent]:
    def __init__(self, components: list[C]) -> None:
        self.components: dict[ComponentKey, C] = {
            component.hash_key(): component for component in components
        }

    def add_component(self, component: C) -> None:
        self.components[component.hash_key()] = component

    def get_components_of_type[T](self, component_type: type[T]) -> list[T]:
        return [
            component
            for component in self.components.values()
            if isinstance(component, component_type)
        ]

    def get_components[T](self, exlude: set[type[T]] | None = None) -> list[C]:
        exlude = exlude or set()
        return [
            component
            for component in self.components.values()
            if type(component) not in exlude
        ]

    def has_component(self, component: C) -> bool:
        return component.hash_key() in self.components

    def has_components(self, components: list[C]) -> bool:
        return all(self.has_component(component) for component in components)


StructureRequirementComponentStore = ComponentStore[StructureRequirementComponent]
StructureProductionComponentStore = ComponentStore[StructureProductionComponent]


class StructureTemplate:
    structure_templates: ClassVar[dict[StructureType, "StructureTemplate"]] = {}

    def __init__(
        self,
        *,
        structure_type: StructureType,
        title: str,
        description: str,
        build_components: list[StructureRequirementComponent],
        production_components: list[StructureProductionComponent],
    ) -> None:
        self.category = self.__class__.__qualname__
        self.structure_type = structure_type
        self.title = title
        self.description = description
        self.build_components: StructureRequirementComponentStore = (
            StructureRequirementComponentStore(build_components)
        )
        self.production_components: StructureProductionComponentStore = (
            StructureProductionComponentStore(production_components)
        )
        StructureTemplate.structure_templates[structure_type] = self

    def to_dict(self, *, level: int = 1) -> dict:
        return {
            "category": self.category,
            "structure_type": self.structure_type,
            "title": self.title,
            "description": self.description,
            "production_components": [
                component.to_dict(level=level)
                for component in self.production_components.components.values()
            ],
            "build_components": [
                component.to_dict(level=level)
                for component in self.build_components.components.values()
            ],
        }

    def get_resource_type_usages(
        self,
    ) -> dict[ResourceType, int]:
        usages: dict[ResourceType, int] = defaultdict(int)
        for component in self.production_components.get_components_of_type(
            ResourceProductionComponent
        ):
            usages[component.resource_type] += component.slot_usage
        return usages


class MineralExtractor(StructureTemplate):
    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.MINERAL_EXTRACTOR,
            title="Mineral Extractor",
            description="Extracts minerals from the planet's crust using basic mining techniques.",
            production_components=[
                ResourceProductionComponent(
                    title="Mineral Production",
                    resource_type=ResourceType.MINERALS,
                    slot_usage=1,
                    value=10,
                    scaling_factor=1.1,
                ),
                EnergyUpkeep(
                    value=-2,
                    scaling_factor=1.05,
                ),
            ],
            build_components=[
                ResourceRequirement(
                    title="Mineral Cost",
                    resource_type=ResourceType.MINERALS,
                    value=100,
                    scaling_factor=1.1,
                ),
                # Available from the start, so no research requirement
            ],
        )


class SolarPanelArray(StructureTemplate):
    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.SOLAR_PANEL_ARRAY,
            title="Solar Panel Array",
            description="Generates energy by converting sunlight into electricity.",
            production_components=[
                ResourceProductionComponent(
                    title="Energy Production",
                    resource_type=ResourceType.ENERGY,
                    slot_usage=1,
                    value=15,
                    scaling_factor=1.1,
                ),
            ],
            build_components=[
                ResourceRequirement(
                    title="Mineral Cost",
                    resource_type=ResourceType.MINERALS,
                    value=80,
                    scaling_factor=1.1,
                )
                # Available from the start
            ],
        )


class HydroponicsFarm(StructureTemplate):
    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.HYDROPONICS_FARM,
            title="Hydroponics Farm",
            description="Grows food in a controlled environment without soil.",
            production_components=[
                ResourceProductionComponent(
                    title="Food Production",
                    resource_type=ResourceType.FOOD,
                    slot_usage=1,
                    value=12,
                    scaling_factor=1.1,
                ),
                EnergyUpkeep(
                    value=-3,
                    scaling_factor=1.05,
                ),
            ],
            build_components=[
                ResourceRequirement(
                    title="Mineral Cost",
                    resource_type=ResourceType.MINERALS,
                    value=90,
                    scaling_factor=1.1,
                ),
                # Available from the start
            ],
        )


class HabitatModule(StructureTemplate):
    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.HABITAT_MODULE,
            title="Habitat Module",
            description="Provides basic living space for your population.",
            production_components=[
                ResourceProductionComponent(
                    title="Population Capacity Increase",
                    resource_type=ResourceType.POPULATION,
                    slot_usage=1,
                    value=5,
                    scaling_factor=1.05,
                ),
                EnergyUpkeep(
                    value=-2,
                    scaling_factor=1.05,
                ),
            ],
            build_components=[
                ResourceRequirement(
                    title="Mineral Cost",
                    resource_type=ResourceType.MINERALS,
                    value=100,
                    scaling_factor=1.1,
                ),
                # Available from the start
            ],
        )


class GetStructuresRequest(BaseModel):
    x: int
    y: int
    entity_id: str


class GetStructuresResponse(BaseModel):
    structure_templates: list[Any]  # Items that can be built
    built_structures: list[Any]  # Items already built


ALL_STRUCTURE_TEMPLATES: list[StructureTemplate] = [
    MineralExtractor(),
    SolarPanelArray(),
    HydroponicsFarm(),
    HabitatModule(),
]


class GetStructuresHandler:
    def __init__(
        self,
        *,
        user_resources_repository: UserResourcesRepository,
        user_research_repository: UserResearchRepository,
        user_structure_repository: UserStructureRepository,
    ) -> None:
        self.user_resources_repository = user_resources_repository
        self.user_research_repository = user_research_repository
        self.user_structure_repository = user_structure_repository

    def handle(
        self, request: GetStructuresRequest, user_id: str
    ) -> GetStructuresResponse:
        built_structures = self.user_structure_repository.get_user_structures(
            user_id=user_id, entity_id=request.entity_id
        )
        matching_templates = self.get_matching_building_templates(
            user_id=user_id,
            entity_id=request.entity_id,
            structures=built_structures,
        )

        return GetStructuresResponse(
            built_structures=[structure.to_dict() for structure in built_structures],
            structure_templates=[template.to_dict() for template in matching_templates],
        )

    def get_matching_building_templates(
        self,
        user_id: str,
        entity_id: str,
        structures: list[Structure],
    ) -> list[StructureTemplate]:
        user_data_hub = UserDataHub(
            user_id=user_id,
            user_resources_repository=self.user_resources_repository,
            user_research_repository=self.user_research_repository,
            user_structure_repository=self.user_structure_repository,
        )
        research_levels = self.user_research_repository.get_user_research(
            user_id=user_id
        )
        resources = self.user_resources_repository.get_user_resources(user_id=user_id)
        evaluator = StructureRequirementEvaluator(
            user_data_hub=user_data_hub, user_id=user_id, entity_id=entity_id
        )
        matching_templates = []
        for template in ALL_STRUCTURE_TEMPLATES:
            if not evaluator.evaluate(
                template.build_components.get_components(exlude={ResourceRequirement})
            ):
                continue

            matching_templates.append(template)

        return matching_templates
