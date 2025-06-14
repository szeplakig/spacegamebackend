import datetime

from pydantic import BaseModel, Field

from spacegamebackend.domain.models.resource.resource import (
    ResourceDescriptor,
    Resources,
)
from spacegamebackend.domain.models.resource.resource_types import ResourceType
from spacegamebackend.domain.models.resource.user_resource_repository import (
    UserResourcesRepository,
)
from spacegamebackend.domain.models.structure.user_structure_repository import (
    UserStructureRepository,
)
from spacegamebackend.utils.resource_capacity_component import ResourceCapacityComponent
from spacegamebackend.utils.resource_production_component import (
    ResourceProductionComponent,
)


class UserResourcesResponse(BaseModel):
    energy: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    minerals: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    alloys: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    antimatter: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    research: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    authority: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)

    class Config:
        from_attributes = True


class GetUserResourcesHandler:
    def __init__(
        self,
        user_resources_repository: UserResourcesRepository,
        user_structure_repository: UserStructureRepository,
    ) -> None:
        self.user_resources_repository = user_resources_repository
        self.user_structure_repository = user_structure_repository

    def handle(self, user_id: str) -> UserResourcesResponse:
        resources = self.user_resources_repository.get_user_resources(user_id=user_id)
        user_structures = self.user_structure_repository.get_all_user_structures(user_id=user_id)

        new_resources = Resources()
        resources.update_resources()
        for resource_type in ResourceType:
            new_resources.get_resource(resource_type).amount = resources.get_resource(resource_type).amount
            new_resources.get_resource(resource_type).updated_at = resources.get_resource(resource_type).updated_at
        for structure in user_structures:
            for component in structure.structure_template.production_components.get_components_of_type(
                ResourceProductionComponent
            ):
                new_resources.get_resource(component.resource_type).change += component.get_scaled_value(
                    structure.level
                )
            for component in structure.structure_template.capacity_components.get_components_of_type(
                ResourceCapacityComponent
            ):
                resource = new_resources.get_resource(component.resource_type)
                if resource.capacity is None:
                    resource.capacity = 0
                resource.capacity += component.get_scaled_value()
        self.user_resources_repository.set_user_resources(user_id=user_id, resources=new_resources)
        return UserResourcesResponse.model_validate(new_resources)
