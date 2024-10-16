from abc import ABC, abstractmethod

from spacegamebackend.schemas.space.component import Component


class Entity(ABC):
    def __init__(self, *, title: str, entity_id: str, components: list[Component]) -> None:
        self.category = self.__class__.__qualname__
        self.title = title
        self.entity_id = entity_id
        self.components = components

    def add_component(self, component: Component) -> None:
        self.components.append(component)

    @abstractmethod
    def to_dict(self) -> dict:
        pass
