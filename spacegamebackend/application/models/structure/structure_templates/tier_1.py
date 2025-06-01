from spacegamebackend.domain.models.space.entity_slot_category import EntitySlotCategory
from spacegamebackend.domain.models.structure.structure_template import StructureTemplate
from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.utils.resource_production_component import EnergyProduction
from spacegamebackend.utils.resource_requirement_component import MineralCost


@StructureTemplate.register_structure_template
class OrbitalSolarFarm(StructureTemplate):
    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.ORBITAL_SOLAR_FARM,
            title="Orbital Solar Farm",
            description="Generates energy from sunlight in orbit.",
            tier=1,
            entity_slot_categories={EntitySlotCategory.ORBIT},
            production_components=[
                EnergyProduction(
                    slot_usage=2,
                    value=25,
                ),
            ],
            requirement_components=[
                MineralCost(
                    value=300,
                ),
            ],
        )
