from pydantic import BaseModel

from spacegamebackend.service.handlers.entity_finder import get_system


class SystemRequest(BaseModel):
    x: int
    y: int


class SystemResponse(BaseModel):
    data: dict


class GetSystemHandler:
    def __init__(self) -> None:
        pass

    def handle(self, system_request: SystemRequest) -> SystemResponse | None:
        return SystemResponse(data=get_system(system_request.x, system_request.y).to_dict())
