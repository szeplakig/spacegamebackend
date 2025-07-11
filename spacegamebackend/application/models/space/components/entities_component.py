from spacegamebackend.domain.models.space.component import Component
from spacegamebackend.domain.models.space.entity import Entity


class EntitiesComponent(Component):
    def __init__(self, *, title: str, entities: list[Entity]) -> None:
        super().__init__(title=title)
        self.entities = entities

    def to_dict(self) -> dict:
        return {
            "type": "entities",
            "category": self.category,
            "title": self.title,
            "entities": [entity.to_dict() for entity in self.entities],
        }
