from abc import ABC, abstractmethod


class ComponentKey:
    pass


class SortableComponent(ABC):
    @abstractmethod
    def hash_key(self) -> ComponentKey:
        pass
