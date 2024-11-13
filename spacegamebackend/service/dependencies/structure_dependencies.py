from fastapi import Depends

from spacegamebackend.repositories.user_research_repository import (
    UserResearchRepository,
)
from spacegamebackend.repositories.user_resource_repository import (
    UserResourcesRepository,
)
from spacegamebackend.repositories.user_structure_repository import (
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
