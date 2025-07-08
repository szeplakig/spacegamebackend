from spacegamebackend.domain.models.space.entity_slot_category import EntitySlotCategory
from spacegamebackend.domain.models.structure.structure_template import (
    StructureTemplate,
)
from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.utils.resource_capacity_component import (
    AuthorityCapacity,
    EnergyCapacity,
)
from spacegamebackend.utils.resource_production_component import (
    AuthorityProduction,
    EnergyProduction,
)
from spacegamebackend.utils.resource_requirement_component import (
    AuthorityCost,
    EnergyCost,
    MineralCost,
)


@StructureTemplate.register_structure_template
class OrbitalSolarFarm(StructureTemplate):
    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.ORBITAL_SOLAR_FARM_T1,
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
            ],
            capacity_components=[
                EnergyCapacity(value=100),
            ],
        )


@StructureTemplate.register_structure_template
class OrbitalGovernmentCenter(StructureTemplate):
    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.ORBITAL_GOVERNMENT_CENTER_T1,
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
            ],
            capacity_components=[
                AuthorityCapacity(value=80),
            ],
        )
