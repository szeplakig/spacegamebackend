import random
from functools import lru_cache
from typing import TYPE_CHECKING
from uuid import UUID

from spacegamebackend.application.models.space.component_templates.structure_slot_component_template import (
    OutpostStructureSlotComponentTemplate,
)
from spacegamebackend.application.models.space.components.entities_component import (
    EntitiesComponent,
)
from spacegamebackend.application.models.space.entitites.solar_system import SolarSystem
from spacegamebackend.application.models.space.entitites.system import System
from spacegamebackend.application.models.space.entity_templates.nebula_template import (
    NebulaTemplate,
)
from spacegamebackend.application.models.space.entity_templates.planet_template import *
from spacegamebackend.application.models.space.entity_templates.solar_system_template import (
    SolarSystemTemplate,
)
from spacegamebackend.application.models.space.entity_templates.star_template import (
    StarTemplate,
)
from spacegamebackend.application.models.space.entity_templates.system_template import (
    SystemTemplate,
)
from spacegamebackend.application.models.space.entity_templates.void_template import (
    VoidTemplate,
)
from spacegamebackend.application.models.space.seeder import CoordinateSeeder
from spacegamebackend.domain.models.space.entity import Entity
from spacegamebackend.domain.models.space.seeder import Seeder

if TYPE_CHECKING:
    from spacegamebackend.domain.models.space.entity_template import EntityTemplate

MATERIAL_DENSITY_SCALE = 200
VOID_DENSITY_THRESHOLD = 0.1
AGE_NOISE_SCALE = 10
AGE_OFFSET_X, AGE_OFFSET_Y = (10000.0, -20000.0)


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


def get_entity_id() -> str:
    return UUID(bytes=random.randbytes(16), version=4).hex


start_system_differ = 0


def generate_starter_planet(seeder: Seeder) -> Entity:
    return ForestPlanetTemplate().generate_entity(seeder=seeder, differ=start_system_differ)


def generate_starter_system(seeder: Seeder) -> System:
    star = StarTemplate().generate_entity(seeder=seeder, differ=start_system_differ + 1)
    planet_1 = LavaPlanetTemplate().generate_entity(seeder=seeder, differ=start_system_differ + 2)
    planet_2 = DesertPlanetTemplate().generate_entity(seeder=seeder, differ=start_system_differ + 3)
    planet_3 = generate_starter_planet(seeder)
    planet_4 = RockyPlanetTemplate().generate_entity(seeder=seeder, differ=start_system_differ + 4)
    planet_5 = GasGiantTemplate().generate_entity(seeder=seeder, differ=start_system_differ + 5)
    planet_6 = GasGiantTemplate().generate_entity(seeder=seeder, differ=start_system_differ + 6)
    planet_7 = IceGiantTemplate().generate_entity(seeder=seeder, differ=start_system_differ + 7)
    planet_8 = IceGiantTemplate().generate_entity(seeder=seeder, differ=start_system_differ + 8)
    solar_system = SolarSystem(
        entity_id=get_entity_id(),
        components=[
            EntitiesComponent(title="Primary Entities", entities=[star]),
            EntitiesComponent(
                title="Secondary Entities",
                entities=[
                    planet_1,
                    planet_2,
                    planet_3,
                    planet_4,
                    planet_5,
                    planet_6,
                    planet_7,
                    planet_8,
                ],
            ),
        ],
    )
    return System(
        entity_id=get_entity_id(),
        components=[
            OutpostStructureSlotComponentTemplate().generate_component(seeder=seeder, differ=start_system_differ + 9),
            EntitiesComponent(title="Content", entities=[solar_system]),
        ],
    )


@lru_cache
def get_system(x: int, y: int) -> Entity:
    seeder = CoordinateSeeder(x=x, y=y)
    if x == 0 and y == 0:
        # Special case for the center system
        return generate_starter_system(seeder)

    value = random.uniform(0, 1)
    template: EntityTemplate
    if value < VOID_DENSITY_THRESHOLD:
        # Generate a void system
        template = VoidTemplate()
    elif value < VOID_DENSITY_THRESHOLD * 3:
        # Generate a nebula system
        template = NebulaTemplate()
    else:
        # Generate a solar system
        template = SolarSystemTemplate()
    return SystemTemplate(template).generate_entity(seeder=seeder, differ=None)


@lru_cache
def get_entity(x: int, y: int, entity_id: str) -> Entity | None:
    solar_system = get_system(x=x, y=y)
    return find_entity(solar_system, entity_id)


def get_entity_checked(x: int, y: int, entity_id: str) -> Entity:
    entity = get_entity(x=x, y=y, entity_id=entity_id)
    if not entity:
        raise RuntimeError("Entity not found")
    return entity
