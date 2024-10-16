from spacegamebackend.schemas.space.component import Component
from spacegamebackend.schemas.space.entity import Entity


class SolarSystem(Entity):
    def __init__(
        self,
        *,
        entity_id: str,
        components: list[Component],
    ) -> None:
        super().__init__(title="Solar System", entity_id=entity_id, components=components)

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "title": self.title,
            "entity_id": self.entity_id,
            "components": [component.to_dict() for component in self.components],
        }
