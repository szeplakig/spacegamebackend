from spacegamebackend.application.models.structure.structure_templates.tier_0 import (
    ResearchLab,
)
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
class BasicResearchMethods(ResearchTemplate):
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
                    structure_level_scaling=1,
                ),
            ],
        )


@ResearchTemplate.register_research_template
class GeothermalPower(ResearchTemplate):
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
                ResearchLab().to_structure_requirement(
                    required_structure_level=1,
                    structure_level_scaling=2,
                ),
            ],
        )


@ResearchTemplate.register_research_template
class AdvancedMiningTechniques(ResearchTemplate):
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
                StructureRequirement(
                    title="Research Lab",
                    structure_type=StructureType.RESEARCH_LAB,
                    structure_location_selector=StructureLocationSelector.GLOBAL,
                    required_structure_level=3,
                    structure_level_scaling=2,
                ),
                BasicResearchMethods().to_research_requirement(
                    required_research_level=2,
                    research_level_scaling=1,
                ),
            ],
        )


@ResearchTemplate.register_research_template
class MolecularRefinement(ResearchTemplate):
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
                StructureRequirement(
                    title="Research Lab",
                    structure_type=StructureType.RESEARCH_LAB,
                    structure_location_selector=StructureLocationSelector.GLOBAL,
                    required_structure_level=1,
                    structure_level_scaling=2,
                ),
                BasicResearchMethods().to_research_requirement(
                    required_research_level=5,
                    research_level_scaling=1,
                ),
            ],
        )


@ResearchTemplate.register_research_template
class IonDrives(ResearchTemplate):
    def __init__(self) -> None:
        super().__init__(
            research_type=ResearchType.ION_DRIVES,
            title="Ion Drives",
            description="Research into ion drive technology.",
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
class BureaucraticOptimization(ResearchTemplate):
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
                StructureRequirement(
                    title="Research Lab",
                    structure_type=StructureType.RESEARCH_LAB,
                    structure_location_selector=StructureLocationSelector.GLOBAL,
                    required_structure_level=1,
                    structure_level_scaling=2,
                ),
            ],
        )
