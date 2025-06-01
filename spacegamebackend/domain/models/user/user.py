from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
