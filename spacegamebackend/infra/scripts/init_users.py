from spacegamebackend.domain.models.user_data_hub import UserDataHub
from spacegamebackend.service.dependencies.user_dependencies import (
    user_research_repository_dependency,
    user_resources_repository_dependency,
    user_structure_repository_dependency,
)


def main() -> None:
    user_id = "bfbc8e7183d94cb5925778b69279303f"
    amount = 1000
    # add N resources to each user for each resource type
    user_resources_repository = user_resources_repository_dependency()
    user_structure_repository = user_structure_repository_dependency()
    user_research_repository = user_research_repository_dependency()
    user_data_hub = UserDataHub(
        user_id=user_id,
        user_resources_repository=user_resources_repository,
        user_research_repository=user_research_repository,
        user_structure_repository=user_structure_repository,
    )
    current_resources = user_resources_repository.get_user_resources(user_id=user_id)
    current_resources.energy.amount += amount
    current_resources.minerals.amount += amount

    user_resources_repository.set_user_resources(user_id=user_id, resources=current_resources)


if __name__ == "__main__":
    main()
