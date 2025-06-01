from spacegamebackend.domain.models.space.component import Component
from spacegamebackend.domain.models.space.entity import Entity
from spacegamebackend.domain.models.space.entity_slot_category import EntitySlotCategory


class Planet(Entity):
    def __init__(
        self,
        *,
        title: str,
        entity_id: str,
        components: list[Component],
        entity_slot_categories: set[EntitySlotCategory] | None = None,
    ) -> None:
        super().__init__(
            title=title,
            entity_id=entity_id,
            entity_slot_categories=(
                {
                    EntitySlotCategory.SURFACE,
                    EntitySlotCategory.ORBIT,
                }
                if entity_slot_categories is None
                else entity_slot_categories
            ),
            components=components,
        )
