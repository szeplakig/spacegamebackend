from fastapi import HTTPException

from spacegamebackend.domain.models.research.research_type import ResearchType
from spacegamebackend.domain.models.research.user_research_repository import (
    UserResearchRepository,
)
from spacegamebackend.domain.models.resource.user_resource_repository import (
    UserResourcesRepository,
)
from spacegamebackend.domain.models.structure.user_structure_repository import (
    UserStructureRepository,
)
from spacegamebackend.domain.models.user_data_hub import UserDataHub


class UpgradeResearchHandler:
    def __init__(
        self,
        user_resources_repository: UserResourcesRepository,
        user_research_repository: UserResearchRepository,
        user_structure_repository: UserStructureRepository,
    ) -> None:
        self.user_resources_repository = user_resources_repository
        self.user_research_repository = user_research_repository
        self.user_structure_repository = user_structure_repository

    def handle(self, *, user_id: str, research_type: ResearchType) -> None:
        user_data_hub = UserDataHub(
            user_id=user_id,
            user_resources_repository=self.user_resources_repository,
            user_research_repository=self.user_research_repository,
            user_structure_repository=self.user_structure_repository,
        )

        if not True:  # TODO: implement research upgrade requirements check
            raise HTTPException(
                status_code=400,
                detail="Research upgrade requirements not met",
            )

        self.upgrade_research(user_data_hub, research_type)

    def upgrade_research(self, user_data_hub: UserDataHub, research_type: ResearchType) -> None:
        user_data_hub.upgrade_research(research_type)
