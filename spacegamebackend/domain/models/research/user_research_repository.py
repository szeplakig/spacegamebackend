from abc import ABC, abstractmethod

from spacegamebackend.domain.models.research.research_type import ResearchType


class UserResearchRepository(ABC):
    @abstractmethod
    def get_user_research(self, *, user_id: str) -> dict[ResearchType, int]:
        """Get the research of a user. If the user does not exist, raise an exception."""

    @abstractmethod
    def upgrade_user_research(self, *, user_id: str, research: ResearchType, level: int = 1) -> None:
        """Add a research to the user. If the user does not exist, raise an exception.

        Args:
            user_id (str): The ID of the user.
            research (ResearchType): The type of research to upgrade.
            level (int, optional): The level to upgrade the research to. Defaults to 1.
        """
