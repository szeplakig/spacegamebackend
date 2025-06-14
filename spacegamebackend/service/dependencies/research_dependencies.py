from fastapi import Depends

from spacegamebackend.domain.models.research.user_research_repository import (
    UserResearchRepository,
)
from spacegamebackend.domain.models.structure.user_structure_repository import (
    UserStructureRepository,
)
from spacegamebackend.service.dependencies.user_dependencies import (
    user_research_repository_dependency,
    user_structure_repository_dependency,
)
from spacegamebackend.service.handlers.get_research_forest import (
    GetResearchForestHandler,
)


def get__get_research_forest_handler_dependency(
    user_research_repository: UserResearchRepository = Depends(user_research_repository_dependency),
    user_structure_repository: UserStructureRepository = Depends(user_structure_repository_dependency),
) -> GetResearchForestHandler:
    return GetResearchForestHandler(user_research_repository, user_structure_repository)
