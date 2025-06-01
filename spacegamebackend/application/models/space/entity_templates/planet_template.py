from collections.abc import Hashable

from spacegamebackend.application.models.space.component_templates.entities_component_template import (
    EntitiesComponentTemplate,
    WeightedEntityTemplate,
)
from spacegamebackend.application.models.space.component_templates.resource_component_template import (
    EnergyComponentTemplate,
    MineralsComponentTemplate,
    ResearchComponentTemplate,
)
from spacegamebackend.application.models.space.component_templates.structure_slot_component_template import (
    Tier0SlotComponentTemplate,
)
from spacegamebackend.application.models.space.entitites.planet import Planet
from spacegamebackend.application.models.space.entity_templates.moon_template import (
    MoonTemplate,
)
from spacegamebackend.domain.models.space.entity import Entity
from spacegamebackend.domain.models.space.entity_slot_category import EntitySlotCategory
from spacegamebackend.domain.models.space.entity_template import EntityTemplate
from spacegamebackend.domain.models.space.seeder import Seeder


class PlanetTemplateBase(EntityTemplate):
    def __init__(
        self,
        *,
        title: str,
        entity_slot_categories: set[EntitySlotCategory] | None = None
    ) -> None:
        super().__init__(
            component_templates=[
                Tier0SlotComponentTemplate(
                    min_slots=1,
                    max_slots=5,
                ),
                EnergyComponentTemplate(min_value=2, max_value=10),
                MineralsComponentTemplate(min_value=5, max_value=20),
                EntitiesComponentTemplate(
                    title="Moons",
                    weighted_entity_templates=[
                        WeightedEntityTemplate(weight=1, entity_template=MoonTemplate())
                    ],
                    min_entities=0,
                    max_entities=5,
                ),
            ],
        )
        self.title = title
        self.entity_slot_categories = entity_slot_categories

    def generate_entity(self, *, seeder: Seeder, differ: Hashable | None) -> Entity:
        seeder.seed(differ=(differ, self.category, "generate_entity"))
        return Planet(
            title=self.title,
            entity_id=self.get_entity_id(seeder=seeder, differ=differ),
            components=self.generate_components(seeder=seeder, differ=differ),
            entity_slot_categories=self.entity_slot_categories,
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
        super().__init__(
            title="Gas Giant",
            entity_slot_categories={
                EntitySlotCategory.ORBIT,
            },
        )
        self.component_templates = [
            EnergyComponentTemplate(min_value=5, max_value=30),
            ResearchComponentTemplate(min_value=0, max_value=10),
            EntitiesComponentTemplate(
                title="Moons",
                weighted_entity_templates=[
                    WeightedEntityTemplate(weight=1, entity_template=MoonTemplate())
                ],
                min_entities=0,
                max_entities=10,
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
                weighted_entity_templates=[
                    WeightedEntityTemplate(weight=1, entity_template=MoonTemplate())
                ],
                min_entities=0,
                max_entities=10,
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
