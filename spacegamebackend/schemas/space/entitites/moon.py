from spacegamebackend.schemas.component_system.component import Component
from spacegamebackend.schemas.space.entity import Entity


class Moon(Entity):
    def __init__(self, *, entity_id: str, components: list[Component]) -> None:
        super().__init__(title="Moon", entity_id=entity_id, components=components)
