import random
from abc import ABC, abstractmethod
from collections.abc import Hashable


class UnsupportedHashableTypeError(TypeError):
    def __init__(self) -> None:
        super().__init__("Unsupported hashable type")


class Seeder(ABC):
    @abstractmethod
    def get_seed(self, *, differ: Hashable | None = None) -> float | str | bytes | None:
        pass

    def seed(self, *, differ: Hashable | None = None) -> None:
        random.seed(self.get_seed(differ=differ))
