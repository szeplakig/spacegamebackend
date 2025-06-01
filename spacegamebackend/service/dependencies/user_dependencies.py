import jwt
from fastapi import Cookie, HTTPException
from pydantic import BaseModel
from starlette import status

from spacegamebackend.domain.models.research.user_research_repository import (
    UserResearchRepository,
)
from spacegamebackend.domain.models.resource.user_resource_repository import (
    UserResourcesRepository,
)
from spacegamebackend.domain.models.structure.user_structure_repository import (
    UserStructureRepository,
)
from spacegamebackend.domain.models.user.user_repository import UserRepository
from spacegamebackend.infra.models.research.sqlite_user_research_repository import (
    SqliteUserResearchRepository,
)
from spacegamebackend.infra.models.resource.sqlite_user_resource_repository import (
    SqliteUserResourcesRepository,
)
from spacegamebackend.infra.models.structure.sqlite_user_structures_repository import (
    SqliteUserStructureRepository,
)
from spacegamebackend.infra.models.user.sqlite_user_repository import SqliteUserRepository

SECRET_KEY = "development"  # noqa: S105


class AccessTokenV1(BaseModel):
    user_id: str


def validate_access_token(access_token: str = Cookie(...)) -> AccessTokenV1:
    try:
        return AccessTokenV1.model_validate(jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"]))
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        ) from e


def user_repository_dependency() -> UserRepository:
    return SqliteUserRepository()


def user_resources_repository_dependency() -> UserResourcesRepository:
    return SqliteUserResourcesRepository()


def user_research_repository_dependency() -> UserResearchRepository:
    return SqliteUserResearchRepository()


def user_structure_repository_dependency() -> UserStructureRepository:
    return SqliteUserStructureRepository()
