import datetime
from functools import partial

from sqlmodel import Field, SQLModel

from spacegamebackend.schemas.structure_slot_type import StructureSlotType


class UserModel(SQLModel, table=True):
    index: int = Field(default=None, primary_key=True)
    id: str
    email: str
    password_hash: str
    salt: str
    created_at: datetime.datetime = Field(default_factory=partial(datetime.datetime.now, datetime.UTC))


class StructuresModel(SQLModel, table=True):
    index: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key=f"{UserModel.__tablename__}.id")
    entity_id: str
    structure_type: StructureSlotType
    created_at: datetime.datetime = Field(default_factory=partial(datetime.datetime.now, datetime.UTC))
