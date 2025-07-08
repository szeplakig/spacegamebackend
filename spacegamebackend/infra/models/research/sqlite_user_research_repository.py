from sqlalchemy import create_engine
from sqlmodel import Session, select

from spacegamebackend.domain.models.research.research_type import ResearchType
from spacegamebackend.domain.models.research.user_research_repository import (
    UserResearchRepository,
)
from spacegamebackend.infra.models.research.research_model import ResearchModel

default_research_levels = {research_type: 0 for research_type in ResearchType}  # Default levels for all research types


class SqliteUserResearchRepository(UserResearchRepository):
    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///database.db")

    def get_user_research(self, *, user_id: str) -> dict[ResearchType, int]:
        """Get the research of a user. If the user does not exist, raise an exception."""

        with Session(self.engine) as session:
            db_researches = session.exec(select(ResearchModel).where(ResearchModel.user_id == user_id)).all()

        return default_research_levels.copy() | {
            ResearchType(research.research_type): research.level for research in db_researches
        }

    def upgrade_user_research(self, *, user_id: str, research: ResearchType, level: int = 1) -> None:
        """Add a research to the user. If the user does not exist, raise an exception.

        Args:
            user_id (str): The ID of the user.
            research (ResearchType): The type of research to upgrade.
            level (int, optional): The level to upgrade the research to. Defaults to 1.
        """
        with Session(self.engine) as session:
            db_research = session.exec(
                select(ResearchModel).where(
                    ResearchModel.user_id == user_id,
                    ResearchModel.research_type == research.value,
                )
            ).first()

            if db_research:
                db_research.level += level
            else:
                db_research = ResearchModel(user_id=user_id, research_type=research.value, level=level)
                session.add(db_research)

            session.commit()
            session.refresh(db_research)
