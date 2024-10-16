from pydantic import BaseModel

from spacegamebackend.schemas.space.entity_templates.solar_system_template import (
    SolarSystemTemplate,
)
from spacegamebackend.schemas.space.seeder import CoordinateSeeder


class SystemRequest(BaseModel):
    x: int
    y: int


class SystemResponse(BaseModel):
    data: dict


class GetSystemHandler:
    def __init__(self) -> None:
        pass

    def handle(self, system_request: SystemRequest) -> SystemResponse | None:
        seeder = CoordinateSeeder(x=system_request.x, y=system_request.y)
        solar_system = SolarSystemTemplate().generate_entity(seeder=seeder, differ=None)
        return SystemResponse(data=solar_system.to_dict())
