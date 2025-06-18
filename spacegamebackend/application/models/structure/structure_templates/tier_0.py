from spacegamebackend.application.models.research.research_templates.tier_0 import (
    AdvancedMiningTechniques,
    BasicResearchMethods,
    BureaucraticOptimization,
    MolecularRefinement,
    SolarPower,
)
from spacegamebackend.domain.models.research.research_type import ResearchType
from spacegamebackend.domain.models.space.entity_slot_category import EntitySlotCategory
from spacegamebackend.domain.models.structure.structure_template import (
    StructureTemplate,
)
from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.utils.research_requirement_component import ResearchRequirement
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


@StructureTemplate.register_structure_template
class MiningFacility(StructureTemplate):
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
                BasicResearchMethods().to_research_requirement(
                    required_research_level=0,
                    research_level_scaling=0.5,
                ),
            ],
            capacity_components=[],
        )


@StructureTemplate.register_structure_template
class AlloyFoundry(StructureTemplate):
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
                MolecularRefinement().to_research_requirement(
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
                BureaucraticOptimization().to_research_requirement(
                    required_research_level=0,
                    research_level_scaling=1,
                ),
            ],
            capacity_components=[AuthorityCapacity(value=500)],
        )


@StructureTemplate.register_structure_template
class DeuteriumExtractor(StructureTemplate):
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
                StructureRequirement(
                    title="Deuterium Extractor",
                    structure_type=StructureType.DEUTERIUM_EXTRACTOR,
                    required_structure_level=1,
                    structure_location_selector=StructureLocationSelector.LOCAL,
                    structure_level_scaling=1,
                ),
                ResearchRequirement(
                    title="Fusion Power",
                    research_type=ResearchType.FUSION_POWER,
                    required_research_level=3,
                    research_level_scaling=2,
                ),
            ],
            capacity_components=[],
        )


@StructureTemplate.register_structure_template
class Outpost(StructureTemplate):
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
            ],
            capacity_components=[],
        )


@StructureTemplate.register_structure_template
class MineralStorage(StructureTemplate):
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
            ],
            capacity_components=[
                MineralsCapacity(value=1000),
            ],
        )


@StructureTemplate.register_structure_template
class EnergyStorage(StructureTemplate):
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
            ],
            capacity_components=[
                EnergyCapacity(value=1000),
            ],
        )
