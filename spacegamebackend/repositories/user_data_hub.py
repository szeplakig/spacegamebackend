from functools import lru_cache

from spacegamebackend.repositories.user_research_repository import (
    UserResearchRepository,
)
from spacegamebackend.repositories.user_resource_repository import (
    UserResourcesRepository,
)
from spacegamebackend.repositories.user_structure_repository import (
    UserStructureRepository,
)
from spacegamebackend.schemas.research.research_type import ResearchType
from spacegamebackend.schemas.resource.types import Resources
from spacegamebackend.schemas.structures.structure import Structure


class UserDataHub:
    def __init__(
        self,
        user_id: str,
        user_resources_repository: UserResourcesRepository,
        user_research_repository: UserResearchRepository,
        user_structure_repository: UserStructureRepository,
    ) -> None:
        self.user_id = user_id
        self.user_resources_repository = user_resources_repository
        self.user_research_repository = user_research_repository
        self.user_structure_repository = user_structure_repository

    @lru_cache
    def get_resources(self) -> Resources:
        return self.user_resources_repository.get_user_resources(user_id=self.user_id)

    @lru_cache
    def get_research(self) -> dict[ResearchType, int]:
        return self.user_research_repository.get_user_research(user_id=self.user_id)

    @lru_cache
    def get_structures(self, entity_id: str) -> list[Structure]:
        return self.user_structure_repository.get_user_structures(user_id=self.user_id, entity_id=entity_id)

    @lru_cache
    def get_all_structures(self) -> list[Structure]:
        return self.user_structure_repository.get_all_user_structures(user_id=self.user_id)
