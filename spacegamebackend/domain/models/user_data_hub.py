from functools import lru_cache

from spacegamebackend.domain.models.research.research_type import ResearchType
from spacegamebackend.domain.models.research.user_research_repository import (
    UserResearchRepository,
)
from spacegamebackend.domain.models.resource.resource import Resources
from spacegamebackend.domain.models.resource.user_resource_repository import (
    UserResourcesRepository,
)
from spacegamebackend.domain.models.structure.structure import Structure
from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.domain.models.structure.user_structure_repository import (
    UserStructureRepository,
)


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

    @lru_cache
    def get_structure(self, structure_id: str) -> Structure:
        return self.user_structure_repository.get_structure(structure_id=structure_id)

    @lru_cache
    def has_structure(self, entity_id: str, structure_type: StructureType) -> bool:
        return self.user_structure_repository.has_structure(
            user_id=self.user_id, entity_id=entity_id, structure_type=structure_type
        )

    @lru_cache
    def has_structure_at(self, x: int, y: int, structure_type: StructureType) -> bool:
        return self.user_structure_repository.has_structure_at(
            user_id=self.user_id, x=x, y=y, structure_type=structure_type
        )

    def upgrade_structure(self, structure_id: str) -> None:
        self.get_structure.cache_clear()
        self.get_structures.cache_clear()
        self.get_all_structures.cache_clear()
        self.has_structure.cache_clear()
        self.has_structure_at.cache_clear()
        self.user_structure_repository.upgrade_structure(structure_id=structure_id)

    def delete_structure(self, structure_id: str) -> None:
        self.get_structure.cache_clear()
        self.get_structures.cache_clear()
        self.get_all_structures.cache_clear()
        self.has_structure.cache_clear()
        self.has_structure_at.cache_clear()
        self.user_structure_repository.delete_user_structure(structure_id=structure_id)
