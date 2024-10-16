import random
from abc import ABC, abstractmethod
from collections.abc import Hashable
from uuid import UUID

from spacegamebackend.schemas.space.component import Component
from spacegamebackend.schemas.space.component_template import ComponentTemplate
from spacegamebackend.schemas.space.entity import Entity
from spacegamebackend.schemas.space.seeder import Seeder


class EntityTemplate(ABC):
    def __init__(self, *, component_templates: list[ComponentTemplate]) -> None:
        self.category = self.__class__.__qualname__
        self.component_templates = component_templates

    @abstractmethod
    def generate_entity(self, *, seeder: Seeder, differ: Hashable | None) -> Entity:
        pass

    def get_entity_id(self, *, seeder: Seeder, differ: Hashable | None) -> str:
        seeder.seed(differ=(differ, self.category, "entity_id"))
        return UUID(bytes=random.randbytes(16), version=4).hex

    def generate_components(self, *, seeder: Seeder, differ: Hashable | None) -> list[Component]:
        seeder.seed(differ=(differ, self.category, "components"))
        return [
            ct.generate_component(seeder=seeder, differ=(i, differ)) for i, ct in enumerate(self.component_templates)
        ]
