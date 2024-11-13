from abc import ABC, abstractmethod
from collections.abc import Hashable

from spacegamebackend.schemas.component_system.component import Component
from spacegamebackend.schemas.space.seeder import Seeder


class ComponentTemplate(ABC):
    def __init__(self, *, title: str) -> None:
        self.title = title
        self.category = self.__class__.__qualname__

    @abstractmethod
    def generate_component(self, *, seeder: Seeder, differ: Hashable | None) -> Component:
        pass
