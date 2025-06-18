from datetime import timedelta

from spacegamebackend.domain.models.resource.user_resource_repository import (
    UserResourcesRepository,
)


class TimeWarpHandler:
    def __init__(self, user_resource_repository: UserResourcesRepository) -> None:
        self.user_resource_repository = user_resource_repository

    def handle(self, user_id: str, seconds: int) -> None:
        self.user_resource_repository.warp_time(user_id=user_id, warp_by=timedelta(seconds=seconds))
