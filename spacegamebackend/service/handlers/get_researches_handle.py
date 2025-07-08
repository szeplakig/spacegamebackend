from spacegamebackend.domain.models.research.research_type import ResearchType
from spacegamebackend.domain.models.research.user_research_repository import (
    UserResearchRepository,
)


class GetResearchesHandler:
    def __init__(self, user_research_repository: UserResearchRepository) -> None:
        self.user_research_repository = user_research_repository

    def handle(self, user_id: str) -> dict[ResearchType, int]:
        return self.user_research_repository.get_user_research(user_id=user_id)
