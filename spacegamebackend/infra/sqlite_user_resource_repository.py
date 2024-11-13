from datetime import UTC, datetime

from sqlalchemy import create_engine
from sqlmodel import Session, select

from spacegamebackend.infra.models import ResourceModel
from spacegamebackend.repositories.user_resource_repository import (
    UserResourcesRepository,
)
from spacegamebackend.schemas.resource.types import ResourceDescriptor, Resources


class SqliteUserResourcesRepository(UserResourcesRepository):
    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///database.db")

    def get_user_resources(self, *, user_id: str) -> Resources:
        """Get the resources of a user."""
        with Session(self.engine) as session:
            db_user_resource = session.exec(select(ResourceModel).where(ResourceModel.user_id == user_id)).first()
            if db_user_resource is None:
                self.set_user_resources(user_id=user_id, resources=Resources())
                return Resources()
            return Resources(
                energy=ResourceDescriptor(
                    amount=db_user_resource.energy,
                    change=db_user_resource.energy_change,
                    capacity=db_user_resource.energy_capacity,
                ),
                minerals=ResourceDescriptor(
                    amount=db_user_resource.minerals,
                    change=db_user_resource.minerals_change,
                    capacity=db_user_resource.minerals_capacity,
                ),
                alloys=ResourceDescriptor(
                    amount=db_user_resource.alloys,
                    change=db_user_resource.alloy_change,
                    capacity=db_user_resource.alloy_capacity,
                ),
                food=ResourceDescriptor(
                    amount=db_user_resource.food,
                    change=db_user_resource.food_change,
                    capacity=db_user_resource.food_capacity,
                ),
                antimatter=ResourceDescriptor(
                    amount=db_user_resource.antimatter,
                    change=db_user_resource.antimatter_change,
                    capacity=db_user_resource.antimatter_capacity,
                ),
                research=ResourceDescriptor(
                    amount=db_user_resource.research,
                    change=db_user_resource.research_points_change,
                    capacity=db_user_resource.research_points_capacity,
                ),
                population=ResourceDescriptor(
                    amount=db_user_resource.population,
                    change=db_user_resource.population_change,
                    capacity=db_user_resource.population_capacity,
                ),
                authority=ResourceDescriptor(
                    amount=db_user_resource.authority,
                    change=db_user_resource.authority_change,
                    capacity=db_user_resource.authority_capacity,
                ),
                updated_at=db_user_resource.updated_at,
            )

    def set_user_resources(self, *, user_id: str, resources: Resources) -> None:
        """Set the resources of a user.
        If a resource is None, do not update it.
        """
        with Session(self.engine) as session:
            db_user_resource = session.exec(select(ResourceModel).where(ResourceModel.user_id == user_id)).first()
            if db_user_resource is None:
                new_resource = ResourceModel(user_id=user_id)
                session.add(new_resource)
            else:
                db_user_resource.energy = resources.energy.amount
                db_user_resource.energy_change = resources.energy.change
                db_user_resource.energy_capacity = resources.energy.capacity
                db_user_resource.minerals = resources.minerals.amount
                db_user_resource.minerals_change = resources.minerals.change
                db_user_resource.minerals_capacity = resources.minerals.capacity
                db_user_resource.alloys = resources.alloys.amount
                db_user_resource.alloy_change = resources.alloys.change
                db_user_resource.alloy_capacity = resources.alloys.capacity
                db_user_resource.food = resources.food.amount
                db_user_resource.food_change = resources.food.change
                db_user_resource.food_capacity = resources.food.capacity
                db_user_resource.antimatter = resources.antimatter.amount
                db_user_resource.antimatter_change = resources.antimatter.change
                db_user_resource.antimatter_capacity = resources.antimatter.capacity
                db_user_resource.research = resources.research.amount
                db_user_resource.research_points_change = resources.research.change
                db_user_resource.research_points_capacity = resources.research.capacity
                db_user_resource.population = resources.population.amount
                db_user_resource.population_change = resources.population.change
                db_user_resource.population_capacity = resources.population.capacity
                db_user_resource.authority = resources.authority.amount
                db_user_resource.authority_change = resources.authority.change
                db_user_resource.authority_capacity = resources.authority.capacity
                db_user_resource.updated_at = datetime.now(tz=UTC)
                session.add(db_user_resource)
            session.commit()
