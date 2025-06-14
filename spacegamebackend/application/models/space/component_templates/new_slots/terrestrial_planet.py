from spacegamebackend.application.models.space.component_templates.resource_component_template import (
    ResourceComponentTemplate,
)
from spacegamebackend.application.models.space.component_templates.structure_slot_component_template import (
    StructureSlotComponentTemplate,
)
from spacegamebackend.application.models.space.components.resource_component import (
    ResourceComponent,
)
from spacegamebackend.domain.models.resource.resource_types import ResourceType
from spacegamebackend.domain.models.structure.structure_type import StructureType


class RichVeinRange(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Rich Vein Range",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.MINERALS,
            component_class=ResourceComponent,
        )


class GreatRiftValley(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Great Rift Valley",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.RESEARCH,
            component_class=ResourceComponent,
        )


class SolarThermalDesert(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Solar-Thermal Desert",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.ENERGY,
            component_class=ResourceComponent,
        )


class AncientImpactBasin(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Ancient Impact Basin",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.MINERALS,
            component_class=ResourceComponent,
        )


class PolarAuroraDome(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Polar Aurora Dome",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.ENERGY,
            component_class=ResourceComponent,
        )


class BioAnomalyJungle(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Bio-Anomaly Jungle",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.RESEARCH,
            component_class=ResourceComponent,
        )


class GeothermalRiftValley(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Geothermal Rift Valley",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.ENERGY,
            component_class=ResourceComponent,
        )


class IridiumImpactLayer(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Iridium Impact Layer",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.MINERALS,
            component_class=ResourceComponent,
        )


class CrystallineSaltSpires(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Crystalline Salt Spires",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.MINERALS,
            component_class=ResourceComponent,
        )


class SubtropicalCloudForest(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Subtropical Cloud Forest",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.RESEARCH,
            component_class=ResourceComponent,
        )


class MagnetiteStormPlains(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Magnetite Storm Plains",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.ENERGY,
            component_class=ResourceComponent,
        )


class AncientMonolithArray(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Ancient Monolith Array",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.RESEARCH,
            component_class=ResourceComponent,
        )


class EquatorialBasaltShield(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Equatorial Basalt Shield",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.MINERALS,
            component_class=ResourceComponent,
        )


class SilicaSolarSink(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Silica Solar Sink",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.ENERGY,
            component_class=ResourceComponent,
        )


class TectonicTripleJunction(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Tectonic Triple Junction",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.MINERALS,
            component_class=ResourceComponent,
        )


class XenobioticGeyserField(ResourceComponentTemplate):
    def __init__(self, *, min_value: int, max_value: int) -> None:
        super().__init__(
            title="Xenobiotic Geyser Field",
            min_value=min_value,
            max_value=max_value,
            resource_type=ResourceType.RESEARCH,
            component_class=ResourceComponent,
        )


class OrbitalElevatorAnchor(StructureSlotComponentTemplate):
    def __init__(self, *, min_slots: int, max_slots: int) -> None:
        super().__init__(
            title="Orbital Elevator Anchor",
            min_slots=min_slots,
            max_slots=max_slots,
            allowed_structure_types=StructureType.tier_0(),
        )


class FertileAlluvialPlain(StructureSlotComponentTemplate):
    def __init__(self, *, min_slots: int, max_slots: int) -> None:
        super().__init__(
            title="Fertile Alluvial Plain",
            min_slots=min_slots,
            max_slots=max_slots,
            allowed_structure_types=StructureType.tier_0(),
        )


class HollowMesaLabyrinth(StructureSlotComponentTemplate):
    def __init__(self, *, min_slots: int, max_slots: int) -> None:
        super().__init__(
            title="Hollow Mesa Labyrinth",
            min_slots=min_slots,
            max_slots=max_slots,
            allowed_structure_types=StructureType.tier_0(),
        )


class PolarIceShelfCavern(StructureSlotComponentTemplate):
    def __init__(self, *, min_slots: int, max_slots: int) -> None:
        super().__init__(
            title="Polar Ice Shelf Cavern",
            min_slots=min_slots,
            max_slots=max_slots,
            allowed_structure_types=StructureType.tier_0(),
        )


terrestial_planet_features = [
    RichVeinRange(min_value=100, max_value=500),
    GreatRiftValley(min_value=50, max_value=300),
    SolarThermalDesert(min_value=200, max_value=600),
    AncientImpactBasin(min_value=150, max_value=400),
    PolarAuroraDome(min_value=100, max_value=350),
    BioAnomalyJungle(min_value=80, max_value=250),
    GeothermalRiftValley(min_value=120, max_value=450),
    IridiumImpactLayer(min_value=90, max_value=300),
    CrystallineSaltSpires(min_value=70, max_value=200),
    SubtropicalCloudForest(min_value=60, max_value=180),
    MagnetiteStormPlains(min_value=110, max_value=360),
    AncientMonolithArray(min_value=130, max_value=420),
    EquatorialBasaltShield(min_value=140, max_value=480),
    SilicaSolarSink(min_value=160, max_value=500),
    TectonicTripleJunction(min_value=170, max_value=550),
    XenobioticGeyserField(min_value=90, max_value=300),
    OrbitalElevatorAnchor(min_slots=1, max_slots=3),
    FertileAlluvialPlain(min_slots=1, max_slots=3),
    HollowMesaLabyrinth(min_slots=1, max_slots=3),
    PolarIceShelfCavern(min_slots=1, max_slots=3),
]
