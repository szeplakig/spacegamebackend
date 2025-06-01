from spacegamebackend.domain.models.research.research_template import ResearchTemplate
from spacegamebackend.domain.models.research.research_type import ResearchType
from spacegamebackend.utils.resource_requirement_component import (
    EnergyCost,
    MineralCost,
)


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
            ],
            production_components=[],
        )
