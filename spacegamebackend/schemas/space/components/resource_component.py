from spacegamebackend.schemas.space.component import Component


class ResourceComponent(Component):
    def __init__(self, *, title: str, value: float) -> None:
        super().__init__(title=title)
        self.value = value

    def to_dict(self) -> dict:
        return {
            "type": "resource",
            "category": self.category,
            "title": self.title,
            "value": self.value,
        }
