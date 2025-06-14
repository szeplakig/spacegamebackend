from abc import ABC, abstractmethod

from spacegamebackend.domain.models.structure.structure import Structure
from spacegamebackend.domain.models.structure.structure_status import StructureStatus
from spacegamebackend.domain.models.structure.structure_type import StructureType


class UserStructureRepository(ABC):
    @abstractmethod
    def get_all_user_structures(self, *, user_id: str) -> list[Structure]:
        """Get all the structures of a user. If the user does not exist, raise an exception."""

    @abstractmethod
    def get_user_structures(self, *, user_id: str, entity_id: str) -> list[Structure]:
        """Get the structures of a user. If the user does not exist, raise an exception."""

    @abstractmethod
    def get_structure(self, *, structure_id: str) -> Structure:
        """Get a structure. If the structure does not exist, raise an exception."""

    @abstractmethod
    def has_structure(self, *, user_id: str, entity_id: str, structure_type: StructureType) -> bool:
        """Check if a user has a structure. If the user does not exist, raise an exception."""

    @abstractmethod
    def has_structure_at(self, *, user_id: str, x: int, y: int, structure_type: StructureType) -> bool:
        """Check if a user has a structure at a specific position. If the user does not exist, raise an exception."""

    @abstractmethod
    def add_user_structure(self, *, user_id: str, entity_id: str, x: int, y: int, structure: Structure) -> None:
        """Add a structure to the user. If the user does not exist, raise an exception."""

    @abstractmethod
    def set_structure_status(self, *, structure_id: str, status: StructureStatus) -> None:
        """Set the status of a structure. If the structure does not exist, raise an exception."""

    @abstractmethod
    def upgrade_structure(self, *, structure_id: str) -> None:
        """Upgrade a structure. If the structure does not exist, raise an exception."""

    @abstractmethod
    def delete_user_structure(self, *, structure_id: str) -> None:
        """Delete a structure. If the structure does not exist, raise an exception."""

    @abstractmethod
    def get_user_structure_levels(self, *, user_id: str, entity_id: str | None = None) -> dict[StructureType, int]:
        """Get the levels of structures for a user at a specific entity.
        If the user does not exist, raise an exception."""
