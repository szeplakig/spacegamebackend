import hashlib
from collections.abc import Hashable

from spacegamebackend.domain.constants import WORLD_SEED
from spacegamebackend.domain.models.space.seeder import Seeder, UnsupportedHashableTypeError


def consistent_hash(value: Hashable) -> int:
    if isinstance(value, int | float | str | bytes):
        return int(hashlib.sha384(str(value).encode("utf-8")).hexdigest(), 16)
    if isinstance(value, tuple):
        return int(
            hashlib.sha384("".join(map(str, value)).encode("utf-8")).hexdigest(),
            16,
        )
    raise UnsupportedHashableTypeError


class CoordinateSeeder(Seeder):
    def __init__(self, *, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def get_seed(self, *, differ: Hashable | None = None) -> int:
        if differ is None:
            return consistent_hash((WORLD_SEED, self.x, self.y))
        return consistent_hash((WORLD_SEED, self.x, self.y, differ))
