from functools import lru_cache

from spacegamebackend.application.models.space.components.entities_component import (
    EntitiesComponent,
)
from spacegamebackend.application.models.space.entity_templates.system_template import (
    SystemTemplate,
)
from spacegamebackend.application.models.space.seeder import CoordinateSeeder
from spacegamebackend.domain.models.space.entity import Entity


def find_entity(root_entity: Entity, entity_id: str) -> Entity | None:
    stack = [root_entity]
    while stack:
        current_entity = stack.pop()
        if current_entity.entity_id == entity_id:
            return current_entity
        for component in current_entity.components:
            if isinstance(component, EntitiesComponent):
                stack.extend(component.entities)
    return None


@lru_cache
def get_system(x: int, y: int) -> Entity:
    seeder = CoordinateSeeder(x=x, y=y)
    return SystemTemplate().generate_entity(seeder=seeder, differ=None)


@lru_cache
def get_entity(x: int, y: int, entity_id: str) -> Entity | None:
    solar_system = get_system(x=x, y=y)
    return find_entity(solar_system, entity_id)


def get_entity_checked(x: int, y: int, entity_id: str) -> Entity:
    entity = get_entity(x=x, y=y, entity_id=entity_id)
    if not entity:
        raise RuntimeError("Entity not found")
    return entity
