from abc import ABC, abstractmethod

from spacegamebackend.utils.component_store import ComponentStore
from spacegamebackend.utils.sortable_component import SortableComponent


class ProductionComponent(SortableComponent, ABC):
    def __init__(self, *, title: str, level: int = 1) -> None:
        self.title = title
        self.category = self.__class__.__qualname__
        self.level = level

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def scale(self, *, level: int) -> "ProductionComponent":
        pass


ProductionComponentStore = ComponentStore[ProductionComponent]
