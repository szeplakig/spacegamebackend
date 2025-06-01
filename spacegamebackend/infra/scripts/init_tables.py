import os

from sqlalchemy import create_engine
from sqlmodel import SQLModel

from spacegamebackend.infra.models.research.research_model import ResearchModel
from spacegamebackend.infra.models.resource.resource_model import ResourceModel
from spacegamebackend.infra.models.structure.structure_model import StructuresModel
from spacegamebackend.infra.models.user.user_model import UserModel

models = [UserModel, ResearchModel, StructuresModel, ResourceModel]

DB_PATH = "database.db"


def delete_db() -> None:
    os.remove(DB_PATH)  # noqa: PTH107


def create_tables() -> None:
    engine = create_engine(f"sqlite:///{DB_PATH}")
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    delete_db()
    create_tables()
