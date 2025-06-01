import datetime

from sqlmodel import Field, SQLModel

import spacegamebackend.domain.models.structure.structure_status
from spacegamebackend.infra.models.blob_int import BlobInt
from spacegamebackend.infra.models.user.user_model import UserModel


class StructuresModel(SQLModel, table=True):
    index: int = Field(default=None, primary_key=True)
    x: int = Field(default=0, ge=0, sa_type=BlobInt)
    y: int = Field(default=0, ge=0, sa_type=BlobInt)
    user_id: str = Field(foreign_key=f"{UserModel.__tablename__}.id")
    structure_id: str
    entity_id: str
    structure_type: str
    level: int
    structure_status: spacegamebackend.domain.models.structure.structure_status.StructureStatus
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
