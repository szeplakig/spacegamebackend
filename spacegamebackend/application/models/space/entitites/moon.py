from spacegamebackend.domain.models.space.component import Component
from spacegamebackend.domain.models.space.entity import Entity
from spacegamebackend.domain.models.space.entity_slot_category import EntitySlotCategory


class Moon(Entity):
    def __init__(self, *, entity_id: str, components: list[Component]) -> None:
        super().__init__(
            title="Moon",
            entity_id=entity_id,
            entity_slot_categories={
                EntitySlotCategory.SURFACE,
                EntitySlotCategory.ORBIT,
            },
            components=components,
        )
