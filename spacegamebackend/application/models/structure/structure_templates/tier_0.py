from spacegamebackend.domain.models.space.entity_slot_category import EntitySlotCategory
from spacegamebackend.domain.models.structure.structure_template import (
    StructureTemplate,
)
from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.utils.resource_production_component import (
    AlloysProduction,
    AuthorityProduction,
    AuthorityUpkeep,
    EnergyProduction,
    EnergyUpkeep,
    MineralsProduction,
    ResearchProduction,
)
from spacegamebackend.utils.resource_requirement_component import (
    EnergyCost,
    MineralCost,
)
from spacegamebackend.utils.structure_requirement_component import (
    StructurePrerequisite,
    Where,
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
                # Available from the start, so no research requirement
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
                    value=15,
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
            ],
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
            ],
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
                    slot_usage=1,
                    value=10,
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
            ],
        )


@StructureTemplate.register_structure_template
class DeuteriumExtractor(StructureTemplate):
    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.DEUTERIUM_EXTRACTOR,
            title="Deuterium Extractor",
            description="Extracts deuterium from water.",
            tier=0,
            entity_slot_categories={EntitySlotCategory.SURFACE},
            production_components=[],
            requirement_components=[
                MineralCost(value=100),
                EnergyCost(value=50),
            ],
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
                StructurePrerequisite(
                    title="Deuterium Extractor",
                    structure_type=StructureType.DEUTERIUM_EXTRACTOR,
                    level=1,
                    where=Where.LOCAL,
                ),
            ],
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
            ],
        )


@StructureTemplate.register_structure_template
class OrbitalGovernmentCenter(StructureTemplate):
    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.ORBITAL_GOVERNMENT_CENTER,
            title="Orbital Government Center",
            description="A center of government for your empire in orbit.",
            tier=0,
            entity_slot_categories={EntitySlotCategory.ORBIT},
            production_components=[
                AuthorityProduction(value=15),
                EnergyProduction(value=20),
            ],
            requirement_components=[
                MineralCost(value=100),
                EnergyCost(value=200),
            ],
        )
