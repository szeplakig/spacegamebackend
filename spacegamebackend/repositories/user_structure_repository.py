from abc import ABC, abstractmethod

from spacegamebackend.schemas.structures.structure import Structure, StructureStatus


class UserStructureRepository(ABC):
    @abstractmethod
    def get_all_user_structures(self, *, user_id: str) -> list[Structure]:
        """Get all the structures of a user. If the user does not exist, raise an exception."""

    @abstractmethod
    def get_user_structures(self, *, user_id: str, entity_id: str) -> list[Structure]:
        """Get the structures of a user. If the user does not exist, raise an exception."""

    @abstractmethod
    def add_user_structure(self, *, user_id: str, entity_id: str, structure: Structure) -> None:
        """Add a structure to the user. If the user does not exist, raise an exception."""

    @abstractmethod
    def set_structure_status(self, *, structure_id: str, status: StructureStatus) -> None:
        """Set the status of a structure. If the structure does not exist, raise an exception."""
