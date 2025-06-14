from spacegamebackend.domain.models.space.component import Component


class FeaturesComponent(Component):
    def __init__(self, *, title: str, components: list[Component]) -> None:
        super().__init__(title=title)
        self.components = components

    def to_dict(self) -> dict:
        return {
            "type": "features",
            "category": self.category,
            "title": self.title,
            "components": [component.to_dict() for component in self.components],
        }
