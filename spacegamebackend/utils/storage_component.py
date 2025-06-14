from abc import ABC, abstractmethod

from spacegamebackend.utils.sortable_component import SortableComponent


class StorageComponent(SortableComponent, ABC):
    def __init__(self, *, title: str, level: int = 1) -> None:
        self.title = title
        self.category = self.__class__.__qualname__
        self.level = level

    @abstractmethod
    def to_dict(self, *, level: int = 1) -> dict:
        """Convert the component to a dictionary representation."""

    @abstractmethod
    def scale(self, *, level: int) -> "StorageComponent":
        """Scale the component to a specific level."""
