from datetime import datetime
from typing import cast

from pydantic import BaseModel, Field

from spacegamebackend.domain.models.resource.resource_types import ResourceType


class ResourceDescriptor(BaseModel):
    amount: int = 0
    change: int = 0
    buffs: float = 1
    capacity: int | None = None
    updated_at: datetime = Field(default_factory=datetime.now)

    def current_amount(self, t: datetime | None = None) -> int:
        t = t or datetime.now()
        hours_passed = (t - self.updated_at).total_seconds() / 3600
        diff = round(
            min(
                self.change * self.buffs * hours_passed,
                self.capacity if self.capacity is not None else float("inf"),
            )
        )
        return self.amount + diff


class Resources(BaseModel):
    energy: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    minerals: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    alloys: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    antimatter: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    research: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    authority: ResourceDescriptor = Field(default_factory=ResourceDescriptor)

    def get_resource(self, resource_type: ResourceType) -> ResourceDescriptor:
        return getattr(self, resource_type.value)

    def update_resource(self, resource_type: ResourceType, t: datetime | None = None) -> None:
        t = t or datetime.now()
        resource = cast(ResourceDescriptor, getattr(self, resource_type.value))
        if (new_value := resource.current_amount(t)) != resource.amount:
            resource.amount = new_value
            resource.updated_at = t

    def update_resources(self) -> None:
        t = datetime.now()
        for resource_type in ResourceType:
            self.update_resource(resource_type, t)

    def set_resource(
        self,
        resource_type: ResourceType,
        amount: int,
        change: int = 0,
        capacity: int | None = None,
    ) -> None:
        resource = self.get_resource(resource_type)
        resource.amount = amount
        resource.change = change
        resource.capacity = capacity

    class Config:
        from_attributes = True
