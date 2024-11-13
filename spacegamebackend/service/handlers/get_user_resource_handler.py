from pydantic import BaseModel, Field

from spacegamebackend.repositories.user_resource_repository import (
    UserResourcesRepository,
)
from spacegamebackend.schemas.resource.types import ResourceDescriptor


class UserResourcesResponse(BaseModel):
    energy: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    minerals: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    alloys: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    food: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    antimatter: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    research: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    population: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    authority: ResourceDescriptor = Field(default_factory=ResourceDescriptor)

    class Config:
        from_attributes = True


class GetUserResourcesHandler:
    def __init__(
        self,
        user_resources_repository: UserResourcesRepository,
    ) -> None:
        self.user_resources_repository = user_resources_repository

    def handle(self, user_id: str) -> UserResourcesResponse:
        return UserResourcesResponse.model_validate(self.user_resources_repository.get_user_resources(user_id=user_id))
