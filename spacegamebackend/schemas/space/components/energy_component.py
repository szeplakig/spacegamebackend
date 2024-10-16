from spacegamebackend.schemas.space.components.resource_component import ResourceComponent


class EnergyComponent(ResourceComponent):
    def __init__(self, *, title: str, value: float) -> None:
        super().__init__(title=title, value=value)
