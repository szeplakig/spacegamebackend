from __future__ import annotations

from typing import TYPE_CHECKING

from spacegamebackend.domain.models.research.research_template import ResearchTemplate
from spacegamebackend.domain.models.research.research_type import ResearchType
from spacegamebackend.domain.models.space.entity_slot_category import EntitySlotCategory
from spacegamebackend.domain.models.structure.structure_template import (
    StructureTemplate,
)
from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.utils.resource_capacity_component import (
    AlloysCapacity,
    AuthorityCapacity,
    EnergyCapacity,
    MineralsCapacity,
)
from spacegamebackend.utils.resource_production_component import (
    AlloysProduction,
    AuthorityProduction,
    AuthorityUpkeep,
    EnergyProduction,
    EnergyUpkeep,
    MineralsProduction,
    MineralsUpkeep,
    ResearchProduction,
)
from spacegamebackend.utils.resource_requirement_component import (
    AuthorityCost,
    EnergyCost,
    MineralCost,
)
from spacegamebackend.utils.structure_requirement_component import (
    StructureLocationSelector,
    StructureRequirement,
)

if TYPE_CHECKING:
    from spacegamebackend.utils.requirement_component import RequirementComponent


def get_research_requirement(
    research_type: ResearchType,
    required_research_level: int,
    research_level_scaling: float,
) -> RequirementComponent:
    return ResearchTemplate.get_research_template(
        research_type
    ).to_research_requirement(
        required_research_level=required_research_level,
        research_level_scaling=research_level_scaling,
    )


def get_structure_requirement(
    structure_type: StructureType,
    required_structure_level: int,
    structure_level_scaling: float,
    required_structure_location_selector: StructureLocationSelector = StructureLocationSelector.GLOBAL,
) -> RequirementComponent:
    return StructureTemplate.get_structure_template(
        structure_type
    ).to_structure_requirement(
        required_structure_level=required_structure_level,
        structure_level_scaling=structure_level_scaling,
        required_structure_location_selector=required_structure_location_selector,
    )


@ResearchTemplate.register_research_template
class BasicResearchMethods(ResearchTemplate):
    research_type = ResearchType.BASIC_RESEARCH_METHODS

    def __init__(self) -> None:
        super().__init__(
            research_type=ResearchType.BASIC_RESEARCH_METHODS,
            title="Basic Research Methods",
            description="Research into basic research methods.",
            tier=0,
            requirement_components=[
                MineralCost(
                    value=100,
                ),
                EnergyCost(
                    value=50,
                ),
                StructureRequirement(
                    title="Research Lab",
                    structure_type=StructureType.RESEARCH_LAB,
                    structure_location_selector=StructureLocationSelector.GLOBAL,
                    required_structure_level=1,
                    structure_level_scaling=1,
                ),
            ],
        )


@ResearchTemplate.register_research_template
class SolarPower(ResearchTemplate):
    research_type = ResearchType.SOLAR_POWER

    def __init__(self) -> None:
        super().__init__(
            research_type=ResearchType.SOLAR_POWER,
            title="Solar Power",
            description="Research into solar technology.",
            tier=0,
            requirement_components=[
                MineralCost(
                    value=100,
                ),
                EnergyCost(
                    value=50,
                ),
                StructureRequirement(
                    title="Research Lab",
                    structure_type=StructureType.RESEARCH_LAB,
                    structure_location_selector=StructureLocationSelector.GLOBAL,
                    required_structure_level=1,
                    structure_level_scaling=1,
                ),
            ],
        )


@ResearchTemplate.register_research_template
class GeothermalPower(ResearchTemplate):
    research_type = ResearchType.GEOTHERMAL_POWER

    def __init__(self) -> None:
        super().__init__(
            research_type=ResearchType.GEOTHERMAL_POWER,
            title="Geothermal Power",
            description="Research into geothermal technology.",
            tier=0,
            requirement_components=[
                MineralCost(
                    value=100,
                ),
                EnergyCost(
                    value=50,
                ),
                StructureRequirement(
                    title="Research Lab",
                    structure_type=StructureType.RESEARCH_LAB,
                    structure_location_selector=StructureLocationSelector.GLOBAL,
                    required_structure_level=1,
                    structure_level_scaling=2,
                ),
            ],
        )


@ResearchTemplate.register_research_template
class StorageLogistics(ResearchTemplate):
    research_type = ResearchType.STORAGE_LOGISTICS

    def __init__(self) -> None:
        super().__init__(
            research_type=ResearchType.STORAGE_LOGISTICS,
            title="Storage Logistics",
            description="Research into storage logistics.",
            tier=0,
            requirement_components=[
                MineralCost(
                    value=100,
                ),
                EnergyCost(
                    value=50,
                ),
                get_structure_requirement(
                    structure_type=StructureType.RESEARCH_LAB,
                    required_structure_level=1,
                    structure_level_scaling=2,
                ),
            ],
        )


@ResearchTemplate.register_research_template
class AdvancedMiningTechniques(ResearchTemplate):
    research_type = ResearchType.ADVANCED_MINING_TECHNIQUES

    def __init__(self) -> None:
        super().__init__(
            research_type=ResearchType.ADVANCED_MINING_TECHNIQUES,
            title="Advanced Mining Techniques",
            description="Research into advanced mining techniques.",
            tier=0,
            requirement_components=[
                MineralCost(
                    value=100,
                ),
                EnergyCost(
                    value=50,
                ),
                get_structure_requirement(
                    structure_type=StructureType.RESEARCH_LAB,
                    required_structure_level=3,
                    structure_level_scaling=2,
                ),
            ],
        )


@ResearchTemplate.register_research_template
class MolecularRefinement(ResearchTemplate):
    research_type = ResearchType.MOLECULAR_REFINEMENT

    def __init__(self) -> None:
        super().__init__(
            research_type=ResearchType.MOLECULAR_REFINEMENT,
            title="Molecular Refinement",
            description="Research into molecular refinement.",
            tier=0,
            requirement_components=[
                MineralCost(
                    value=100,
                ),
                EnergyCost(
                    value=50,
                ),
                get_structure_requirement(
                    structure_type=StructureType.RESEARCH_LAB,
                    required_structure_level=1,
                    structure_level_scaling=2,
                ),
                get_research_requirement(
                    research_type=ResearchType.BASIC_RESEARCH_METHODS,
                    required_research_level=1,
                    research_level_scaling=2,
                ),
            ],
        )


@ResearchTemplate.register_research_template
class BureaucraticOptimization(ResearchTemplate):
    research_type = ResearchType.BUREAUCRATIC_OPTIMIZATION

    def __init__(self) -> None:
        super().__init__(
            research_type=ResearchType.BUREAUCRATIC_OPTIMIZATION,
            title="Bureaucratic Optimization",
            description="Research into bureaucratic optimization.",
            tier=0,
            requirement_components=[
                MineralCost(
                    value=100,
                ),
                EnergyCost(
                    value=50,
                ),
                get_structure_requirement(
                    structure_type=StructureType.RESEARCH_LAB,
                    required_structure_level=1,
                    structure_level_scaling=2,
                ),
                get_research_requirement(
                    research_type=ResearchType.BASIC_RESEARCH_METHODS,
                    required_research_level=1,
                    research_level_scaling=2,
                ),
            ],
        )


@ResearchTemplate.register_research_template
class FusionPower(ResearchTemplate):
    research_type = ResearchType.FUSION_POWER

    def __init__(self) -> None:
        super().__init__(
            research_type=ResearchType.FUSION_POWER,
            title="Fusion Power",
            description="Research into fusion technology.",
            tier=0,
            requirement_components=[
                MineralCost(
                    value=100,
                ),
                EnergyCost(
                    value=50,
                ),
                get_structure_requirement(
                    structure_type=StructureType.RESEARCH_LAB,
                    required_structure_level=1,
                    structure_level_scaling=2,
                ),
            ],
        )


@ResearchTemplate.register_research_template
class OrbitConstruction(ResearchTemplate):
    research_type = ResearchType.ORBITAL_CONSTRUCTION

    def __init__(self) -> None:
        super().__init__(
            research_type=ResearchType.ORBITAL_CONSTRUCTION,
            title="Orbital Construction",
            description="Research into orbital construction techniques.",
            tier=1,
            requirement_components=[
                MineralCost(
                    value=300,
                ),
                EnergyCost(
                    value=200,
                ),
                get_structure_requirement(
                    structure_type=StructureType.RESEARCH_LAB,
                    required_structure_level=10,
                    structure_level_scaling=2,
                ),
            ],
        )


@StructureTemplate.register_structure_template
class MiningFacility(StructureTemplate):
    structure_type = StructureType.MINING_FACILITY

    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.MINING_FACILITY,
            title="Mining Facility",
            description="Extracts minerals from the planet's crust using basic mining techniques.",
            tier=0,
            entity_slot_categories={EntitySlotCategory.SURFACE},
            production_components=[
                MineralsProduction(
                    slot_usage=1,
                    value=50,
                ),
                EnergyUpkeep(
                    value=10,
                ),
            ],
            requirement_components=[
                MineralCost(
                    value=100,
                ),
                EnergyCost(
                    value=50,
                ),
                AdvancedMiningTechniques().to_research_requirement(0, 1),
            ],
            capacity_components=[
                MineralsCapacity(value=100),
            ],
        )


@StructureTemplate.register_structure_template
class SolarFarm(StructureTemplate):
    structure_type = StructureType.SOLAR_FARM

    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.SOLAR_FARM,
            title="Solar Farm",
            description="Generates energy from sunlight.",
            tier=0,
            entity_slot_categories={EntitySlotCategory.SURFACE},
            production_components=[
                EnergyProduction(
                    value=40,
                    slot_usage=1,
                )
            ],
            requirement_components=[
                MineralCost(
                    value=100,
                ),
                EnergyCost(
                    value=100,
                ),
                SolarPower().to_research_requirement(0, 1),
            ],
            capacity_components=[],
        )


@StructureTemplate.register_structure_template
class ResearchLab(StructureTemplate):
    structure_type = StructureType.RESEARCH_LAB

    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.RESEARCH_LAB,
            title="Research Lab",
            description="A research lab to research new technologies.",
            tier=0,
            entity_slot_categories={EntitySlotCategory.SURFACE},
            production_components=[
                ResearchProduction(
                    value=10,
                    slot_usage=1,
                ),
                EnergyUpkeep(
                    value=10,
                ),
            ],
            requirement_components=[
                MineralCost(
                    value=100,
                ),
                EnergyCost(
                    value=50,
                ),
                get_research_requirement(
                    research_type=ResearchType.BASIC_RESEARCH_METHODS,
                    required_research_level=0,
                    research_level_scaling=0.5,
                ),
            ],
            capacity_components=[],
        )


@StructureTemplate.register_structure_template
class AlloyFoundry(StructureTemplate):
    structure_type = StructureType.ALLOY_FOUNDRY

    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.ALLOY_FOUNDRY,
            title="Alloy Foundry",
            description="Produces alloys from minerals.",
            tier=0,
            entity_slot_categories={EntitySlotCategory.SURFACE},
            production_components=[
                AlloysProduction(
                    value=10,
                ),
                MineralsUpkeep(
                    value=20,
                ),
                EnergyUpkeep(
                    value=10,
                ),
            ],
            requirement_components=[
                MineralCost(
                    value=100,
                ),
                EnergyCost(
                    value=50,
                ),
                get_research_requirement(
                    research_type=ResearchType.MOLECULAR_REFINEMENT,
                    required_research_level=1,
                    research_level_scaling=1,
                ),
            ],
            capacity_components=[
                AlloysCapacity(value=20),
            ],
        )


@StructureTemplate.register_structure_template
class GovernmentCenter(StructureTemplate):
    structure_type = StructureType.GOVERNMENT_CENTER

    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.GOVERNMENT_CENTER,
            title="Government Center",
            description="A center of government for your empire.",
            tier=0,
            entity_slot_categories={EntitySlotCategory.SURFACE},
            production_components=[
                AuthorityProduction(value=10),
                EnergyUpkeep(value=10),
            ],
            requirement_components=[
                MineralCost(value=100),
                EnergyCost(value=200),
                get_research_requirement(
                    research_type=ResearchType.BUREAUCRATIC_OPTIMIZATION,
                    required_research_level=0,
                    research_level_scaling=1,
                ),
            ],
            capacity_components=[AuthorityCapacity(value=500)],
        )


@StructureTemplate.register_structure_template
class DeuteriumExtractor(StructureTemplate):
    structure_type = StructureType.DEUTERIUM_EXTRACTOR

    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.DEUTERIUM_EXTRACTOR,
            title="Deuterium Extractor",
            description="Extracts deuterium from water to fuel fusion.",
            tier=0,
            entity_slot_categories={EntitySlotCategory.SURFACE},
            production_components=[
                EnergyUpkeep(value=50),
            ],
            requirement_components=[
                MineralCost(value=500),
                EnergyCost(value=100),
            ],
            capacity_components=[],
        )


@StructureTemplate.register_structure_template
class FusionReactor(StructureTemplate):
    structure_type = StructureType.FUSION_REACTOR

    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.FUSION_REACTOR,
            title="Fusion Reactor",
            description="A fusion reactor to generate energy.",
            tier=0,
            entity_slot_categories={EntitySlotCategory.SURFACE},
            production_components=[
                EnergyProduction(value=50),
            ],
            requirement_components=[
                MineralCost(value=100),
                EnergyCost(value=100),
                get_structure_requirement(
                    structure_type=StructureType.DEUTERIUM_EXTRACTOR,
                    required_structure_level=1,
                    structure_level_scaling=1,
                ),
                get_research_requirement(
                    research_type=ResearchType.FUSION_POWER,
                    required_research_level=3,
                    research_level_scaling=2,
                ),
            ],
            capacity_components=[],
        )


@StructureTemplate.register_structure_template
class Outpost(StructureTemplate):
    structure_type = StructureType.OUTPOST

    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.OUTPOST,
            title="Outpost",
            description="A small outpost to claim a location in space.",
            tier=0,
            entity_slot_categories={EntitySlotCategory.DEEP_SPACE},
            production_components=[
                EnergyUpkeep(value=10),
                AuthorityUpkeep(value=5),
            ],
            requirement_components=[
                MineralCost(value=100),
                AuthorityCost(value=200),
                get_research_requirement(
                    research_type=ResearchType.ORBITAL_CONSTRUCTION,
                    required_research_level=0,
                    research_level_scaling=0.5,
                ),
            ],
            capacity_components=[],
        )


@StructureTemplate.register_structure_template
class MineralStorage(StructureTemplate):
    structure_type = StructureType.MINERAL_STORAGE

    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.MINERAL_STORAGE,
            title="Mineral Storage",
            description="A storage facility for minerals.",
            tier=0,
            entity_slot_categories={EntitySlotCategory.SURFACE},
            production_components=[],
            requirement_components=[
                MineralCost(value=100),
                EnergyCost(value=50),
                get_research_requirement(
                    research_type=ResearchType.STORAGE_LOGISTICS,
                    required_research_level=0,
                    research_level_scaling=1,
                ),
            ],
            capacity_components=[
                MineralsCapacity(value=1000),
            ],
        )


@StructureTemplate.register_structure_template
class EnergyStorage(StructureTemplate):
    structure_type = StructureType.ENERGY_STORAGE

    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.ENERGY_STORAGE,
            title="Energy Storage",
            description="A storage facility for energy.",
            tier=0,
            entity_slot_categories={EntitySlotCategory.SURFACE},
            production_components=[],
            requirement_components=[
                MineralCost(value=100),
                EnergyCost(value=50),
                get_research_requirement(
                    research_type=ResearchType.STORAGE_LOGISTICS,
                    required_research_level=0,
                    research_level_scaling=1,
                ),
            ],
            capacity_components=[
                EnergyCapacity(value=1000),
            ],
        )


@StructureTemplate.register_structure_template
class OrbitalSolarFarm(StructureTemplate):
    structure_type = StructureType.ORBITAL_SOLAR_FARM

    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.ORBITAL_SOLAR_FARM,
            title="Orbital Solar Farm",
            description="Generates energy from sunlight in orbit.",
            tier=1,
            entity_slot_categories={EntitySlotCategory.ORBIT},
            production_components=[
                EnergyProduction(
                    slot_usage=1,
                    value=50,
                ),
            ],
            requirement_components=[
                MineralCost(
                    value=300,
                ),
                get_research_requirement(
                    research_type=ResearchType.ORBITAL_CONSTRUCTION,
                    required_research_level=3,
                    research_level_scaling=1,
                ),
                get_research_requirement(
                    research_type=ResearchType.SOLAR_POWER,
                    required_research_level=10,
                    research_level_scaling=2,
                ),
            ],
            capacity_components=[
                EnergyCapacity(value=100),
            ],
        )


@StructureTemplate.register_structure_template
class OrbitalGovernmentCenter(StructureTemplate):
    structure_type = StructureType.ORBITAL_GOVERNMENT_CENTER

    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.ORBITAL_GOVERNMENT_CENTER,
            title="Orbital Government Center",
            description="A center of government for your empire in orbit.",
            tier=0,
            entity_slot_categories={EntitySlotCategory.ORBIT},
            production_components=[
                AuthorityProduction(value=40),
            ],
            requirement_components=[
                MineralCost(value=1000),
                EnergyCost(value=2000),
                AuthorityCost(
                    value=400,
                ),
                get_research_requirement(
                    research_type=ResearchType.ORBITAL_CONSTRUCTION,
                    required_research_level=5,
                    research_level_scaling=1,
                ),
            ],
            capacity_components=[
                AuthorityCapacity(value=80),
            ],
        )
