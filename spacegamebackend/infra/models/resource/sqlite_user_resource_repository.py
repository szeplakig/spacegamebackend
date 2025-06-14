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
    def __init__(self, db_url: str = "sqlite:///database.db") -> None:
        self.engine = create_engine(db_url, echo=False)

    def _map_db_to_resources(self, db_resource: ResourceModel) -> Resources:
        mapped: dict[str, ResourceDescriptor] = {
            rtype.value: ResourceDescriptor(
                amount=getattr(db_resource, rtype.value),
                change=getattr(db_resource, f"{rtype.value}_change"),
                capacity=getattr(db_resource, f"{rtype.value}_capacity"),
                updated_at=getattr(db_resource, f"{rtype.value}_updated_at"),
            )
            for rtype in ResourceType
        }
        return Resources(**mapped)

    def get_user_resources(self, *, user_id: str) -> Resources:
        with Session(self.engine) as session:
            db_resource = session.exec(select(ResourceModel).where(ResourceModel.user_id == user_id)).first()

            if db_resource is None:
                default_resources = Resources()
                self.set_user_resources(user_id=user_id, resources=default_resources)
                return default_resources

            return self._map_db_to_resources(db_resource)

    def set_user_resources(self, *, user_id: str, resources: Resources) -> None:
        with Session(self.engine) as session:
            db_resource = session.exec(select(ResourceModel).where(ResourceModel.user_id == user_id)).first()

            if db_resource is None:
                db_resource = ResourceModel(user_id=user_id)
                session.add(db_resource)

            now = datetime.now()

            for rtype in ResourceType:
                descriptor = getattr(resources, rtype.value)
                setattr(db_resource, rtype.value, descriptor.amount)
                setattr(db_resource, f"{rtype.value}_change", descriptor.change)
                setattr(db_resource, f"{rtype.value}_capacity", descriptor.capacity)
                setattr(db_resource, f"{rtype.value}_updated_at", now)

            session.commit()

    def warp_time(self, *, user_id: str, warp_by: datetime) -> None:
        with Session(self.engine) as session:
            db_resource = session.exec(select(ResourceModel).where(ResourceModel.user_id == user_id)).first()

            if db_resource is None:
                raise ValueError(f"User with ID {user_id} does not exist.")

            for rtype in ResourceType:
                descriptor = getattr(db_resource, rtype.value)
                change = getattr(db_resource, f"{rtype.value}_change")
                capacity = getattr(db_resource, f"{rtype.value}_capacity")
                updated_at = getattr(db_resource, f"{rtype.value}_updated_at")

                # Calculate the new amount based on the change and time warp
                hours_passed = (warp_by - updated_at).total_seconds() / 3600
                new_amount = round(
                    min(
                        descriptor.amount + change * hours_passed,
                        capacity if capacity is not None else float("inf"),
                    )
                )

                # Update the resource
                setattr(db_resource, rtype.value, new_amount)
                setattr(db_resource, f"{rtype.value}_updated_at", warp_by)

            session.commit()
