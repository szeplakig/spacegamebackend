from fastapi import Depends

from spacegamebackend.domain.models.research.user_research_repository import (
    UserResearchRepository,
)
from spacegamebackend.domain.models.resource.user_resource_repository import UserResourcesRepository
from spacegamebackend.domain.models.structure.user_structure_repository import (
    UserStructureRepository,
)
from spacegamebackend.service.dependencies.user_dependencies import (
    user_research_repository_dependency,
    user_resources_repository_dependency,
    user_structure_repository_dependency,
)
from spacegamebackend.service.handlers.get_research_forest import (
    GetResearchForestHandler,
)
from spacegamebackend.service.handlers.get_researches_handle import GetResearchesHandler
from spacegamebackend.service.handlers.upgrade_research_handler import UpgradeResearchHandler


def get__get_research_forest_handler_dependency(
    user_research_repository: UserResearchRepository = Depends(user_research_repository_dependency),
    user_structure_repository: UserStructureRepository = Depends(user_structure_repository_dependency),
) -> GetResearchForestHandler:
    return GetResearchForestHandler(user_research_repository, user_structure_repository)


def get__get_researches_handler_dependency(
    user_research_repository: UserResearchRepository = Depends(user_research_repository_dependency),
) -> GetResearchesHandler:
    return GetResearchesHandler(user_research_repository)


def get__upgrade_research_handler_dependency(
    user_resources_repository: UserResourcesRepository = Depends(user_resources_repository_dependency),
    user_research_repository: UserResearchRepository = Depends(user_research_repository_dependency),
    user_structure_repository: UserStructureRepository = Depends(user_structure_repository_dependency),
) -> UpgradeResearchHandler:
    return UpgradeResearchHandler(user_resources_repository, user_research_repository, user_structure_repository)
