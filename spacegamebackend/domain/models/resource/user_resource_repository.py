from abc import ABC, abstractmethod

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
