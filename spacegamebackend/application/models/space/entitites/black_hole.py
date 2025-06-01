from spacegamebackend.domain.models.space.component import Component
from spacegamebackend.domain.models.space.entity import Entity
from spacegamebackend.domain.models.space.entity_slot_category import EntitySlotCategory


class BlackHole(Entity):
    def __init__(self, *, entity_id: str, components: list[Component]) -> None:
        super().__init__(
            title="Black Hole",
            entity_id=entity_id,
            entity_slot_categories={EntitySlotCategory.ORBIT},
            components=components,
        )
