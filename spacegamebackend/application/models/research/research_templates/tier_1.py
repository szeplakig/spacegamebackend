from spacegamebackend.domain.models.research.research_template import ResearchTemplate
from spacegamebackend.domain.models.research.research_type import ResearchType
from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.utils.resource_requirement_component import (
    EnergyCost,
    MineralCost,
)
from spacegamebackend.utils.structure_requirement_component import (
    StructureLocationSelector,
    StructureRequirement,
)


@ResearchTemplate.register_research_template
class FusionPower(ResearchTemplate):
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
                StructureRequirement(
                    title="Research Lab",
                    structure_type=StructureType.RESEARCH_LAB,
                    structure_location_selector=StructureLocationSelector.GLOBAL,
                    required_structure_level=1,
                    structure_level_scaling=2,
                ),
            ],
        )
