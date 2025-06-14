from abc import ABC, abstractmethod

from spacegamebackend.utils.component_store import ComponentStore
from spacegamebackend.utils.sortable_component import SortableComponent


class RequirementComponent(SortableComponent, ABC):
    def __init__(self, *, title: str, level: int = 1) -> None:
        self.title = title
        self.category = self.__class__.__qualname__
        self.level = level

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def get_scaled_value(self) -> int:
        pass

    @abstractmethod
    def scale(self, level: int) -> "RequirementComponent":
        pass


RequirementComponentStore = ComponentStore[RequirementComponent]
