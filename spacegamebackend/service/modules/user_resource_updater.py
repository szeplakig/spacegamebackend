from spacegamebackend.domain.models.research.research_type import ResearchType
from spacegamebackend.domain.models.research.user_research_repository import (
    UserResearchRepository,
)
from spacegamebackend.domain.models.resource.resource import Resources
from spacegamebackend.domain.models.resource.user_resource_repository import (
    UserResourcesRepository,
)
from spacegamebackend.domain.models.structure.structure import Structure
from spacegamebackend.domain.models.structure.user_structure_repository import (
    UserStructureRepository,
)


class UserResourceUpdater:
    def __init__(
        self,
        user_resources_repository: UserResourcesRepository,
        user_structure_repository: UserStructureRepository,
        user_research_repository: UserResearchRepository,
    ) -> None:
        self.user_resources_repository = user_resources_repository
        self.user_structure_repository = user_structure_repository
        self.user_research_repository = user_research_repository

    def update_user_resources(self, user_id: str) -> None:
        # Get the resources of the user
        user_resources = self.user_resources_repository.get_user_resources(user_id=user_id)
        # Get the structures of the user
        structures = self.user_structure_repository.get_all_user_structures(user_id=user_id)
        # Get the research of the user
        research = self.user_research_repository.get_user_research(user_id=user_id)
        # Calculate the resources
        updated_resources = self.calculate_resources(user_resources, structures, research)
        # Update the resources
        self.user_resources_repository.set_user_resources(user_id=user_id, resources=updated_resources)

    def calculate_resources(
        self,
        user_resources: Resources,
        structures: list[Structure],
        research: dict[ResearchType, int],
    ) -> Resources:
        # Calculate the resources
        return user_resources
