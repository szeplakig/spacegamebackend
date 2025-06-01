from abc import ABC, abstractmethod

from spacegamebackend.domain.models.user.user import User


class UserRepository(ABC):
    @abstractmethod
    def register_user(self, *, email: str, password: str) -> User:
        pass

    @abstractmethod
    def login_user(self, *, email: str, password: str) -> User | None:
        pass

    @abstractmethod
    def get_user_by_id(self, *, user_id: str) -> User | None:
        pass
