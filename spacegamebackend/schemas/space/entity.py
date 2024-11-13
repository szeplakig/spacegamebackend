from spacegamebackend.schemas.component_system.component import Component


class Entity:
    def __init__(self, *, title: str, entity_id: str, components: list[Component]) -> None:
        self.category = self.__class__.__qualname__
        self.title = title
        self.entity_id = entity_id
        self.components = components

    def add_component(self, component: Component) -> None:
        self.components.append(component)

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "title": self.title,
            "entity_id": self.entity_id,
            "components": [component.to_dict() for component in self.components],
        }
