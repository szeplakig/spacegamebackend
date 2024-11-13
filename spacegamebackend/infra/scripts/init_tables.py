from sqlalchemy import create_engine
from sqlmodel import SQLModel

from spacegamebackend.infra.models import *  # noqa: F403


def create_tables() -> None:
    engine = create_engine("sqlite:///database.db")
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()
