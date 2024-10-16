from spacegamebackend.schemas.space.component_templates.resource_component_template import (
    ResourceComponentTemplate,
)
from spacegamebackend.schemas.space.components.minerals_component import MineralsComponent


class MineralsComponentTemplate(ResourceComponentTemplate):
    def __init__(self, *, min_value: float, max_value: float) -> None:
        super().__init__(
            title="Minerals",
            min_value=min_value,
            max_value=max_value,
            component_class=MineralsComponent,
        )
