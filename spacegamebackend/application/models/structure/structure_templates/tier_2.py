from spacegamebackend.domain.models.space.entity_slot_category import EntitySlotCategory
from spacegamebackend.domain.models.structure.structure_template import StructureTemplate
from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.utils.resource_production_component import EnergyUpkeep, ResearchProduction
from spacegamebackend.utils.resource_requirement_component import MineralCost


@StructureTemplate.register_structure_template
class DeepSpaceResearchStation(StructureTemplate):
    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.DEEP_SPACE_RESEARCH_STATION,
            title="Deep Space Research Station",
            description="A research station in deep space.",
            tier=2,
            entity_slot_categories={EntitySlotCategory.DEEP_SPACE},
            production_components=[
                ResearchProduction(
                    slot_usage=2,
                    value=25,
                ),
                EnergyUpkeep(
                    value=40,
                ),
            ],
            requirement_components=[
                MineralCost(
                    value=2000,
                ),
            ],
        )
