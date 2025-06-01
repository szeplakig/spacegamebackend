from functools import lru_cache

from spacegamebackend.application.models.space.components.entities_component import (
    EntitiesComponent,
)
from spacegamebackend.application.models.space.entity_templates.system_template import (
    CenterSystemTemplate,
    SystemTemplate,
)
from spacegamebackend.application.models.space.seeder import CoordinateSeeder
from spacegamebackend.domain.models.space.entity import Entity

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


# @lru_cache
# def get_system_feature(x: int, y: int) -> tuple[float, float]:
#     def m(xo: int, yo: int) -> float:
#         v = noise2(x / MATERIAL_DENSITY_SCALE + xo, y / MATERIAL_DENSITY_SCALE + yo)
#         return min(
#             1,
#             max(
#                 0,
#                 v,
#             ),
#         )

#     material_density = m(0, 0) * m(100000, 0) * m(0, 100000) * m(100000, 10000)
#     age = (
#         noise2(x / AGE_NOISE_SCALE + AGE_OFFSET_X, y / AGE_NOISE_SCALE + AGE_OFFSET_Y)
#         + 1
#     ) / 2
#     return material_density, age


@lru_cache
def get_system(x: int, y: int) -> Entity:
    seeder = CoordinateSeeder(x=x, y=y)
    if x == 0 and y == 0:
        # Special case for the center system
        return CenterSystemTemplate().generate_entity(seeder=seeder, differ=2)

    # material_density, age = get_system_feature(x, y)

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


# if __name__ == "__main__":
#     # generate a feature map with matplotlib for testing, 10001x10001, 0,0 in the middle pixels,
#     # if material density is below 0.2, color black, if above color it based on the age
#     import numpy as np
#     import matplotlib.pyplot as plt

#     size = 1000
#     x = np.arange(-size // 2, size // 2 + 1)
#     y = np.arange(-size // 2, size // 2 + 1)
#     X, Y = np.meshgrid(x, y)
#     Z = np.zeros((size + 1, size + 1))
#     for i in range(size + 1):
#         for j in range(size + 1):
#             material_density, age = get_system_feature(X[i, j], Y[i, j])
#             Z[i, j] = material_density
#     plt.imshow(Z, extent=(-size // 2, size // 2, -size // 2, size // 2), cmap="viridis")
#     plt.colorbar(label="Age")
#     plt.title("System Feature Map")
#     plt.xlabel("X Coordinate")
#     plt.ylabel("Y Coordinate")
#     plt.show()
