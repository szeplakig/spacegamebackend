from abc import ABC, abstractmethod
from datetime import timedelta

from spacegamebackend.domain.models.resource.resource import Resources


class UserResourcesRepository(ABC):
    @abstractmethod
    def get_user_resources(self, *, user_id: str) -> Resources:
        """Get the resources of a user. If the user does not exist, raise an exception."""

    @abstractmethod
    def set_user_resources(self, *, user_id: str, resources: Resources) -> None:
        """Set the resources of a user. If the user does not exist, raise an exception.
        If a resource is None, do not update it.
        """

    @abstractmethod
    def warp_time(self, *, user_id: str, warp_by: timedelta) -> None:
        """Warp the time of the user by a given timedelta. This will update the resources of the user
        based on the current amount and change of each resource.
        """
