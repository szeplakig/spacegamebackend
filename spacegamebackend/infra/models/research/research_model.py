import datetime

from sqlmodel import Field, SQLModel

from spacegamebackend.infra.models.user.user_model import UserModel


class ResearchModel(SQLModel, table=True):
    index: int = Field(default=None, primary_key=True)
    research_id: str
    user_id: str = Field(foreign_key=f"{UserModel.__tablename__}.id")
    research_type: str
    level: int = Field(default=0, ge=0)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
