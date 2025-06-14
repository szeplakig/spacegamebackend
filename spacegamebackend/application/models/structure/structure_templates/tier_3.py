from spacegamebackend.domain.models.space.entity_slot_category import EntitySlotCategory
from spacegamebackend.domain.models.structure.structure_template import StructureTemplate
from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.utils.resource_production_component import AntimatterProduction, EnergyUpkeep
from spacegamebackend.utils.resource_requirement_component import AlloysCost, MineralCost


class DarkMatterEngine(StructureTemplate):
    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.DARK_MATTER_ENGINE,
            title="Dark Matter Engine",
            description="Generates Antimatter from a Dark Matter Halo of a Space Entity and some Energy.",
            tier=3,
            entity_slot_categories={EntitySlotCategory.ORBIT},
            production_components=[
                AntimatterProduction(
                    slot_usage=1,
                    value=5,
                ),
                EnergyUpkeep(
                    value=400,
                ),
            ],
            requirement_components=[
                MineralCost(
                    value=20000,
                ),
                AlloysCost(
                    value=10000,
                ),
            ],
        )
