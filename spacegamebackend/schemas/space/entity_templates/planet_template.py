from collections.abc import Hashable

from spacegamebackend.schemas.space.component_templates.entities_component_template import (
    EntitiesComponentTemplate,
    WeightedEntityTemplate,
)
from spacegamebackend.schemas.space.component_templates.resource_component_template import (
    EnergyComponentTemplate,
    MineralsComponentTemplate,
)
from spacegamebackend.schemas.space.component_templates.structures_component_template import (
    OrbitalStructuresComponentTemplate,
    SurfaceStructuresComponentTemplate,
)
from spacegamebackend.schemas.space.entitites.planet import Planet
from spacegamebackend.schemas.space.entity import Entity
from spacegamebackend.schemas.space.entity_template import EntityTemplate
from spacegamebackend.schemas.space.entity_templates.moon_template import MoonTemplate
from spacegamebackend.schemas.space.seeder import Seeder


class PlanetTemplateBase(EntityTemplate):
    def __init__(self, *, title: str) -> None:
        super().__init__(
            component_templates=[
                EnergyComponentTemplate(min_value=2, max_value=5),
                MineralsComponentTemplate(min_value=10, max_value=20),
                EntitiesComponentTemplate(
                    title="Moons",
                    weighted_entity_templates=[WeightedEntityTemplate(weight=1, entity_template=MoonTemplate())],
                    min_entities=0,
                    max_entities=5,
                ),
                OrbitalStructuresComponentTemplate(
                    min_structure_slots=0,
                    max_structure_slots=30,
                ),
                SurfaceStructuresComponentTemplate(
                    min_structure_slots=0,
                    max_structure_slots=15,
                ),
            ],
        )
        self.title = title

    def generate_entity(self, *, seeder: Seeder, differ: Hashable | None) -> Entity:
        seeder.seed(differ=(differ, self.category, "entity"))
        return Planet(
            title=self.title,
            entity_id=self.get_entity_id(seeder=seeder, differ=differ),
            components=self.generate_components(seeder=seeder, differ=differ),
        )


class RockyPlanetTemplate(PlanetTemplateBase):
    def __init__(self) -> None:
        super().__init__(title="Rocky Planet")


class IcePlanetTemplate(PlanetTemplateBase):
    def __init__(self) -> None:
        super().__init__(title="Ice Planet")


class LavaPlanetTemplate(PlanetTemplateBase):
    def __init__(self) -> None:
        super().__init__(title="Lava Planet")


class DesertPlanetTemplate(PlanetTemplateBase):
    def __init__(self) -> None:
        super().__init__(title="Desert Planet")


class OceanPlanetTemplate(PlanetTemplateBase):
    def __init__(self) -> None:
        super().__init__(title="Ocean Planet")


class ForestPlanetTemplate(PlanetTemplateBase):
    def __init__(self) -> None:
        super().__init__(title="Forest Planet")


class GasGiantTemplate(PlanetTemplateBase):
    def __init__(self) -> None:
        super().__init__(title="Gas Giant")
        self.component_templates = [
            EnergyComponentTemplate(min_value=5, max_value=10),
            MineralsComponentTemplate(min_value=20, max_value=50),
            EntitiesComponentTemplate(
                title="Moons",
                weighted_entity_templates=[WeightedEntityTemplate(weight=1, entity_template=MoonTemplate())],
                min_entities=0,
                max_entities=10,
            ),
            OrbitalStructuresComponentTemplate(
                min_structure_slots=0,
                max_structure_slots=50,
            ),
        ]


class IceGiantTemplate(PlanetTemplateBase):
    def __init__(self) -> None:
        super().__init__(title="Ice Giant")
        self.component_templates = [
            EnergyComponentTemplate(min_value=5, max_value=10),
            MineralsComponentTemplate(min_value=20, max_value=50),
            EntitiesComponentTemplate(
                title="Moons",
                weighted_entity_templates=[WeightedEntityTemplate(weight=1, entity_template=MoonTemplate())],
                min_entities=0,
                max_entities=10,
            ),
            OrbitalStructuresComponentTemplate(
                min_structure_slots=0,
                max_structure_slots=50,
            ),
        ]


PLANET_TEMPLATES = [
    RockyPlanetTemplate(),
    IcePlanetTemplate(),
    LavaPlanetTemplate(),
    DesertPlanetTemplate(),
    OceanPlanetTemplate(),
    ForestPlanetTemplate(),
    GasGiantTemplate(),
    IceGiantTemplate(),
]
