from abc import ABC, abstractmethod
from collections.abc import Hashable

from spacegamebackend.schemas.space.component import Component
from spacegamebackend.schemas.space.seeder import Seeder


class ComponentTemplate(ABC):
    def __init__(self, *, title: str) -> None:
        self.category = self.__class__.__qualname__
        self.title = title

    @abstractmethod
    def generate_component(self, *, seeder: Seeder, differ: Hashable | None) -> Component:
        pass
