from datetime import datetime
from uuid import uuid4

import jwt
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from spacegamebackend.domain.models.resource.resource import (
    ResourceDescriptor,
    Resources,
)
from spacegamebackend.domain.models.resource.user_resource_repository import (
    UserResourcesRepository,
)
from spacegamebackend.domain.models.structure.structure import Structure
from spacegamebackend.domain.models.structure.structure_status import StructureStatus
from spacegamebackend.domain.models.structure.structure_template import (
    StructureTemplate,
)
from spacegamebackend.domain.models.structure.structure_type import StructureType
from spacegamebackend.domain.models.structure.user_structure_repository import (
    UserStructureRepository,
)
from spacegamebackend.domain.models.user.user_repository import UserRepository
from spacegamebackend.service.dependencies.user_dependencies import (
    SECRET_KEY,
    AccessTokenV1,
)
from spacegamebackend.service.handlers.entity_finder import get_system


class RegisterUserRequest(BaseModel):
    email: str
    password: str


class RegisterUserResponse(BaseModel):
    id: str
    email: str
    created_at: datetime
    access_token: str


class RegisterUserHandler:
    def __init__(
        self,
        *,
        user_repository: UserRepository,
        user_resource_repository: UserResourcesRepository,
        user_structure_repository: UserStructureRepository,
    ) -> None:
        self.user_repository = user_repository
        self.user_resource_repository = user_resource_repository
        self.user_structure_repository = user_structure_repository

    def handle(self, user_request: RegisterUserRequest) -> RegisterUserResponse:
        user = self.user_repository.register_user(email=user_request.email, password=user_request.password)
        self.user_resource_repository.set_user_resources(
            user_id=user.id,
            resources=Resources(
                energy=ResourceDescriptor(amount=1000, change=0, capacity=5000),
                minerals=ResourceDescriptor(amount=1000, change=0, capacity=2000),
                alloys=ResourceDescriptor(amount=0, change=0, capacity=0),
                antimatter=ResourceDescriptor(amount=0, change=0, capacity=0),
                research=ResourceDescriptor(amount=0, change=0, capacity=1000),
                authority=ResourceDescriptor(amount=0, change=0, capacity=1000),
            ),
        )
        solar_system = get_system(x=0, y=0)
        # Add structures to the user's home system
        # Add the outpost
        self.user_structure_repository.add_user_structure(
            user_id=user.id,
            entity_id=solar_system.entity_id,
            x=0,
            y=0,
            structure=Structure(
                structure_id=uuid4().hex,
                entity_id=solar_system.entity_id,
                structure_type=StructureType.OUTPOST,
                level=1,
                structure_status=StructureStatus.P100,
                structure_template=StructureTemplate.structure_templates[StructureType.OUTPOST],
            ),
        )
        # Add the OrbitalGovernmentCenter
        self.user_structure_repository.add_user_structure(
            user_id=user.id,
            entity_id=solar_system.entity_id,
            x=0,
            y=0,
            structure=Structure(
                structure_id=uuid4().hex,
                entity_id=solar_system.entity_id,
                structure_type=StructureType.ORBITAL_GOVERNMENT_CENTER,
                level=1,
                structure_status=StructureStatus.P100,
                structure_template=StructureTemplate.structure_templates[StructureType.ORBITAL_GOVERNMENT_CENTER],
            ),
        )

        return RegisterUserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at,
            access_token=jwt.encode(
                jsonable_encoder(AccessTokenV1(user_id=user.id).model_dump()),
                SECRET_KEY,
                algorithm="HS256",
            ),
        )
