from spacegamebackend.domain.models.space.entity_slot_category import EntitySlotCategory
from spacegamebackend.domain.models.structure.structure_template import StructureTemplate
from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.utils.resource_production_component import EnergyUpkeep, ResearchProduction
from spacegamebackend.utils.resource_requirement_component import AlloysCost, AntimatterCost, EnergyCost, MineralCost


@StructureTemplate.register_structure_template
class MegaDeepSpaceParticleAccelerator(StructureTemplate):
    def __init__(self) -> None:
        super().__init__(
            structure_type=StructureType.MEGA_DEEP_SPACE_PARTICLE_ACCELERATOR,
            title="Mega Deep Space Particle Accelerator",
            description="A research station in deep space. Uses lots of energy to create more research.",
            tier=5,
            entity_slot_categories={EntitySlotCategory.DEEP_SPACE},
            production_components=[
                ResearchProduction(
                    value=200,
                    slot_usage=10,
                ),
                EnergyUpkeep(
                    value=500,
                ),
            ],
            requirement_components=[
                MineralCost(
                    value=10000,
                ),
                AlloysCost(
                    value=15000,
                ),
                EnergyCost(
                    value=40000,
                ),
                AntimatterCost(value=3000),
            ],
        )
