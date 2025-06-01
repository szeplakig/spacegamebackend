from collections.abc import Hashable

from spacegamebackend.application.models.space.component_templates.entities_component_template import (
    EntitiesComponentTemplate,
    WeightedEntityTemplate,
)
from spacegamebackend.application.models.space.component_templates.structure_slot_component_template import (
    OrbitalGovernmentCenterStructureSlotComponentTemplate,
    OutpostStructureSlotComponentTemplate,
)
from spacegamebackend.application.models.space.entitites.system import System
from spacegamebackend.application.models.space.entity_templates.nebula import (
    NebulaTemplate,
)
from spacegamebackend.application.models.space.entity_templates.solar_system_template import (
    SolarSystemTemplate,
)
from spacegamebackend.domain.models.space.entity import Entity
from spacegamebackend.domain.models.space.entity_template import EntityTemplate
from spacegamebackend.domain.models.space.seeder import Seeder


class SystemTemplate(EntityTemplate):
    def __init__(self) -> None:
        super().__init__(
            component_templates=[
                OutpostStructureSlotComponentTemplate(),
                EntitiesComponentTemplate(
                    title="Content",
                    weighted_entity_templates=[
                        WeightedEntityTemplate(weight=10, entity_template=SolarSystemTemplate()),
                        WeightedEntityTemplate(weight=1, entity_template=NebulaTemplate()),
                    ],
                    min_entities=1,
                    max_entities=1,
                ),
            ],
        )

    def generate_entity(self, *, seeder: Seeder, differ: Hashable | None) -> Entity:
        seeder.seed(differ=(differ, self.category, "generate_entity"))
        return System(
            entity_id=self.get_entity_id(seeder=seeder, differ=differ),
            components=self.generate_components(seeder=seeder, differ=differ),
        )


class CenterSystemTemplate(EntityTemplate):
    def __init__(self) -> None:
        super().__init__(
            component_templates=[
                OutpostStructureSlotComponentTemplate(),
                OrbitalGovernmentCenterStructureSlotComponentTemplate(),
                EntitiesComponentTemplate(
                    title="Content",
                    weighted_entity_templates=[
                        WeightedEntityTemplate(weight=1, entity_template=SolarSystemTemplate()),
                    ],
                    min_entities=1,
                    max_entities=1,
                ),
            ],
        )

    def generate_entity(self, *, seeder: Seeder, differ: Hashable | None) -> Entity:
        seeder.seed(differ=(differ, self.category, "generate_entity"))
        return System(
            entity_id=self.get_entity_id(seeder=seeder, differ=differ),
            components=self.generate_components(seeder=seeder, differ=differ),
        )
