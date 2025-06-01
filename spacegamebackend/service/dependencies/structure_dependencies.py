from fastapi import Depends

from spacegamebackend.domain.models.research.user_research_repository import (
    UserResearchRepository,
)
from spacegamebackend.domain.models.resource.user_resource_repository import (
    UserResourcesRepository,
)
from spacegamebackend.domain.models.structure.user_structure_repository import (
    UserStructureRepository,
)
from spacegamebackend.service.dependencies.user_dependencies import (
    user_research_repository_dependency,
    user_resources_repository_dependency,
    user_structure_repository_dependency,
)
from spacegamebackend.service.handlers.build_structure_handler import (
    BuildStructureHandler,
)
from spacegamebackend.service.handlers.get_structures_handler import (
    GetStructuresHandler,
)
from spacegamebackend.service.handlers.upgrade_structure_handler import UpgradeStructureHandler


def get__get_strucutres_handler_dependency(
    user_resources_repository: UserResourcesRepository = Depends(user_resources_repository_dependency),
    user_research_repository: UserResearchRepository = Depends(user_research_repository_dependency),
    user_structure_repository: UserStructureRepository = Depends(user_structure_repository_dependency),
) -> GetStructuresHandler:
    return GetStructuresHandler(
        user_resources_repository=user_resources_repository,
        user_research_repository=user_research_repository,
        user_structure_repository=user_structure_repository,
    )


def get__build_structure_handler_dependency(
    user_resources_repository: UserResourcesRepository = Depends(user_resources_repository_dependency),
    user_research_repository: UserResearchRepository = Depends(user_research_repository_dependency),
    user_structure_repository: UserStructureRepository = Depends(user_structure_repository_dependency),
) -> BuildStructureHandler:
    return BuildStructureHandler(
        user_resources_repository=user_resources_repository,
        user_research_repository=user_research_repository,
        user_structure_repository=user_structure_repository,
    )


def get__upgrade_structure_handler_dependency(
    user_resources_repository: UserResourcesRepository = Depends(user_resources_repository_dependency),
    user_research_repository: UserResearchRepository = Depends(user_research_repository_dependency),
    user_structure_repository: UserStructureRepository = Depends(user_structure_repository_dependency),
) -> UpgradeStructureHandler:
    return UpgradeStructureHandler(
        user_resources_repository=user_resources_repository,
        user_research_repository=user_research_repository,
        user_structure_repository=user_structure_repository,
    )
