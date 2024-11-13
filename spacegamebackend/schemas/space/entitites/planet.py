from spacegamebackend.schemas.component_system.component import Component
from spacegamebackend.schemas.space.entity import Entity


class Planet(Entity):
    def __init__(self, *, title: str, entity_id: str, components: list[Component]) -> None:
        super().__init__(title=title, entity_id=entity_id, components=components)
