from sqlalchemy import create_engine
from sqlmodel import Session, select

from spacegamebackend.domain.models.research.research_type import ResearchType
from spacegamebackend.domain.models.research.user_research_repository import (
    UserResearchRepository,
)
from spacegamebackend.infra.models.research.research_model import ResearchModel


class SqliteUserResearchRepository(UserResearchRepository):
    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///database.db")

    def get_user_research(self, *, user_id: str) -> dict[ResearchType, int]:
        """Get the research of a user. If the user does not exist, raise an exception."""

        with Session(self.engine) as session:
            db_researches = session.exec(select(ResearchModel).where(ResearchModel.user_id == user_id)).all()

        return {ResearchType(research.research_type): research.level for research in db_researches}

    def add_user_research(self, *, user_id: str, research: ResearchType, level: int = 1) -> None:
        """Add a research to the user. If the user does not exist, raise an exception."""
