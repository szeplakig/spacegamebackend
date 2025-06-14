from datetime import datetime

from sqlalchemy import create_engine
from sqlmodel import Session, select

from spacegamebackend.domain.models.resource.resource import (
    ResourceDescriptor,
    Resources,
)
from spacegamebackend.domain.models.resource.resource_types import ResourceType
from spacegamebackend.domain.models.resource.user_resource_repository import (
    UserResourcesRepository,
)
from spacegamebackend.infra.models.resource.resource_model import ResourceModel


class SqliteUserResourcesRepository(UserResourcesRepository):
    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///database.db")

    def get_user_resources(self, *, user_id: str) -> Resources:
        """Get the resources of a user."""
        with Session(self.engine) as session:
            db_user_resource = session.exec(
                select(ResourceModel).where(ResourceModel.user_id == user_id)
            ).first()
            if db_user_resource is None:
                self.set_user_resources(user_id=user_id, resources=Resources())
                return Resources()
            return Resources(
                energy=ResourceDescriptor(
                    amount=db_user_resource.energy,
                    change=db_user_resource.energy_change,
                    capacity=db_user_resource.energy_capacity,
                    updated_at=db_user_resource.energy_updated_at,
                ),
                minerals=ResourceDescriptor(
                    amount=db_user_resource.minerals,
                    change=db_user_resource.minerals_change,
                    capacity=db_user_resource.minerals_capacity,
                    updated_at=db_user_resource.minerals_updated_at,
                ),
                alloys=ResourceDescriptor(
                    amount=db_user_resource.alloys,
                    change=db_user_resource.alloys_change,
                    capacity=db_user_resource.alloys_capacity,
                    updated_at=db_user_resource.alloys_updated_at,
                ),
                antimatter=ResourceDescriptor(
                    amount=db_user_resource.antimatter,
                    change=db_user_resource.antimatter_change,
                    capacity=db_user_resource.antimatter_capacity,
                    updated_at=db_user_resource.antimatter_updated_at,
                ),
                research=ResourceDescriptor(
                    amount=db_user_resource.research,
                    change=db_user_resource.research_change,
                    capacity=db_user_resource.research_capacity,
                    updated_at=db_user_resource.research_updated_at,
                ),
                authority=ResourceDescriptor(
                    amount=db_user_resource.authority,
                    change=db_user_resource.authority_change,
                    capacity=db_user_resource.authority_capacity,
                    updated_at=db_user_resource.authority_updated_at,
                ),
            )

    def set_user_resources(self, *, user_id: str, resources: Resources) -> None:
        with Session(self.engine) as session:
            db_user_resource = session.exec(
                select(ResourceModel).where(ResourceModel.user_id == user_id)
            ).first()
            if db_user_resource is None:
                db_user_resource = ResourceModel(
                    user_id=user_id,
                )
                session.add(db_user_resource)
            for resource_type in ResourceType:
                setattr(
                    db_user_resource,
                    resource_type.value,
                    getattr(resources, resource_type.value).amount,
                )
                setattr(
                    db_user_resource,
                    f"{resource_type.value}_change",
                    getattr(resources, resource_type.value).change,
                )
                setattr(
                    db_user_resource,
                    f"{resource_type.value}_capacity",
                    getattr(resources, resource_type.value).capacity,
                )
                setattr(
                    db_user_resource,
                    f"{resource_type.value}_updated_at",
                    datetime.now(),
                )
                session.add(db_user_resource)
            session.commit()
