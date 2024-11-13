from abc import ABC, abstractmethod

from spacegamebackend.schemas.research.research_type import ResearchType


class UserResearchRepository(ABC):
    @abstractmethod
    def get_user_research(self, *, user_id: str) -> dict[ResearchType, int]:
        """Get the research of a user. If the user does not exist, raise an exception."""

    @abstractmethod
    def add_user_research(self, *, user_id: str, research: ResearchType, level: int = 1) -> None:
        """Add a research to the user. If the user does not exist, raise an exception."""
