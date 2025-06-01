from abc import ABC, abstractmethod

from spacegamebackend.utils.component_store import ComponentStore
from spacegamebackend.utils.sortable_component import SortableComponent


class ProductionComponent(SortableComponent, ABC):
    def __init__(self, *, title: str) -> None:
        self.title = title
        self.category = self.__class__.__qualname__

    @abstractmethod
    def to_dict(self, *, level: int = 1) -> dict:
        pass


ProductionComponentStore = ComponentStore[ProductionComponent]
