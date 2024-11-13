import datetime
from functools import partial

from sqlmodel import Field, SQLModel

from spacegamebackend.schemas.research.research_type import ResearchType
from spacegamebackend.schemas.structures import structure
from spacegamebackend.schemas.structures.structure_type import StructureType


class UserModel(SQLModel, table=True):
    index: int = Field(default=None, primary_key=True)
    id: str
    email: str
    password_hash: str
    salt: str
    created_at: datetime.datetime = Field(default_factory=partial(datetime.datetime.now, datetime.UTC))


class ResourceModel(SQLModel, table=True):
    index: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key=f"{UserModel.__tablename__}.id")
    energy: int = Field(default=0, ge=0)
    energy_change: int = Field(default=0, ge=0)
    energy_capacity: int | None = Field(default=None, nullable=True)
    minerals: int = Field(default=0, ge=0)
    minerals_change: int = Field(default=0, ge=0)
    minerals_capacity: int | None = Field(default=None, nullable=True)
    alloys: int = Field(default=0, ge=0)
    alloy_change: int = Field(default=0, ge=0)
    alloy_capacity: int | None = Field(default=None, nullable=True)
    food: int = Field(default=0, ge=0)
    food_change: int = Field(default=0, ge=0)
    food_capacity: int | None = Field(default=None, nullable=True)
    antimatter: int = Field(default=0, ge=0)
    antimatter_change: int = Field(default=0, ge=0)
    antimatter_capacity: int | None = Field(default=None, nullable=True)
    research: int = Field(default=0, ge=0)
    research_points_change: int = Field(default=0, ge=0)
    research_points_capacity: int | None = Field(default=None, nullable=True)
    population: int = Field(default=0, ge=0)
    population_change: int = Field(default=0, ge=0)
    population_capacity: int | None = Field(default=None, nullable=True)
    authority: int = Field(default=0, ge=0)
    authority_change: int = Field(default=0, ge=0)
    authority_capacity: int | None = Field(default=None, nullable=True)
    updated_at: datetime.datetime = Field(default_factory=partial(datetime.datetime.now, datetime.UTC))


class StructuresModel(SQLModel, table=True):
    index: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key=f"{UserModel.__tablename__}.id")
    structure_id: str
    entity_id: str
    structure_type: StructureType
    level: int
    structure_status: structure.StructureStatus
    created_at: datetime.datetime = Field(default_factory=partial(datetime.datetime.now, datetime.UTC))


class ResearchModel(SQLModel, table=True):
    index: int = Field(default=None, primary_key=True)
    research_id: str
    user_id: str = Field(foreign_key=f"{UserModel.__tablename__}.id")
    research_type: ResearchType
    level: int = Field(default=0, ge=0)
    created_at: datetime.datetime = Field(default_factory=partial(datetime.datetime.now, datetime.UTC))
