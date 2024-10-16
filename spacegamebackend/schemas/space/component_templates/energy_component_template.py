from spacegamebackend.schemas.space.component_templates.resource_component_template import (
    ResourceComponentTemplate,
)
from spacegamebackend.schemas.space.components.energy_component import EnergyComponent


class EnergyComponentTemplate(ResourceComponentTemplate):
    def __init__(self, *, min_value: float, max_value: float) -> None:
        super().__init__(
            title="Energy",
            min_value=min_value,
            max_value=max_value,
            component_class=EnergyComponent,
        )
