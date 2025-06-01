import datetime

from sqlmodel import Field, SQLModel

from spacegamebackend.infra.models.blob_int import BlobInt
from spacegamebackend.infra.models.user.user_model import UserModel


class ResourceModel(SQLModel, table=True):
    index: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key=f"{UserModel.__tablename__}.id")
    energy: int = Field(default=0, ge=0, sa_type=BlobInt)
    energy_change: int = Field(default=0, ge=0, sa_type=BlobInt)
    energy_capacity: int | None = Field(default=None, nullable=True, sa_type=BlobInt)
    energy_updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    minerals: int = Field(default=0, ge=0, sa_type=BlobInt)
    minerals_change: int = Field(default=0, ge=0, sa_type=BlobInt)
    minerals_capacity: int | None = Field(default=None, nullable=True, sa_type=BlobInt)
    minerals_updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    alloys: int = Field(default=0, ge=0, sa_type=BlobInt)
    alloys_change: int = Field(default=0, ge=0, sa_type=BlobInt)
    alloys_capacity: int | None = Field(default=None, nullable=True, sa_type=BlobInt)
    alloys_updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    antimatter: int = Field(default=0, ge=0, sa_type=BlobInt)
    antimatter_change: int = Field(default=0, ge=0, sa_type=BlobInt)
    antimatter_capacity: int | None = Field(default=None, nullable=True, sa_type=BlobInt)
    antimatter_updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    research: int = Field(default=0, ge=0, sa_type=BlobInt)
    research_change: int = Field(default=0, ge=0, sa_type=BlobInt)
    research_capacity: int | None = Field(default=None, nullable=True, sa_type=BlobInt)
    research_updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    authority: int = Field(default=0, ge=0, sa_type=BlobInt)
    authority_change: int = Field(default=0, ge=0, sa_type=BlobInt)
    authority_capacity: int | None = Field(default=None, nullable=True, sa_type=BlobInt)
    authority_updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
