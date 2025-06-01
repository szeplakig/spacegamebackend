from spacegamebackend.domain.models.space.component import Component
from spacegamebackend.domain.models.space.entity import Entity
from spacegamebackend.domain.models.space.entity_slot_category import EntitySlotCategory


class Nebula(Entity):
    def __init__(
        self,
        *,
        entity_id: str,
        components: list[Component],
    ) -> None:
        super().__init__(
            title="Nebula",
            entity_id=entity_id,
            entity_slot_categories={
                EntitySlotCategory.DEEP_SPACE,
            },
            components=components,
        )
