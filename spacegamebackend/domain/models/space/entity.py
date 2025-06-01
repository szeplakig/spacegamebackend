from spacegamebackend.domain.models.space.component import Component
from spacegamebackend.domain.models.space.entity_slot_category import EntitySlotCategory


class Entity:
    def __init__(
        self,
        *,
        title: str,
        entity_id: str,
        entity_slot_categories: set[EntitySlotCategory],
        components: list[Component],
    ) -> None:
        self.category = self.__class__.__qualname__
        self.title = title
        self.entity_id = entity_id
        self.entity_slot_categories = entity_slot_categories
        self.components = components

    def add_component(self, component: Component) -> None:
        self.components.append(component)

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "title": self.title,
            "entity_id": self.entity_id,
            "entity_slot_categories": list(self.entity_slot_categories),
            "components": [component.to_dict() for component in self.components],
        }

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(title={self.title!r}, entity_id={self.entity_id!r})"
