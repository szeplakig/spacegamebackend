import datetime

from sqlmodel import Field, SQLModel


class UserModel(SQLModel, table=True):
    index: int = Field(default=None, primary_key=True)
    id: str
    email: str
    password_hash: str
    salt: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
