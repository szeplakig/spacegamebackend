from datetime import UTC, datetime
from enum import StrEnum
from functools import partial

from pydantic import BaseModel, Field


class ResourceType(StrEnum):
    ENERGY = "energy"
    MINERALS = "minerals"
    ALLOYS = "alloys"
    FOOD = "food"
    ANTIMATTER = "antimatter"
    RESEARCH = "research"
    POPULATION = "population"
    AUTHORITY = "authority"


class ResourceDescriptor(BaseModel):
    amount: int = 0
    change: int = 0
    capacity: int | None = None

    @property
    def is_full(self) -> bool:
        return self.capacity is not None and self.amount >= self.capacity


class Resources(BaseModel):
    energy: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    minerals: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    alloys: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    food: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    antimatter: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    research: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    population: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    authority: ResourceDescriptor = Field(default_factory=ResourceDescriptor)
    updated_at: datetime = Field(default_factory=partial(datetime.now, UTC))

    def get_resource(self, resource_type: ResourceType) -> ResourceDescriptor:
        return getattr(self, resource_type.value)

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
