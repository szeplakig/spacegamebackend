from spacegamebackend.infra.sqlite_user_resource_repository import (
    SqliteUserResourcesRepository,
)


def main() -> None:
    user_id = "e2f2691247354cc8a3a29d80ce92904f"
    amount = 1000000
    # add N resources to each user for each resource type
    repo = SqliteUserResourcesRepository()
    current_resources = repo.get_user_resources(user_id=user_id)
    current_resources.energy.amount += amount
    current_resources.minerals.amount += amount
    current_resources.alloys.amount += amount
    current_resources.food.amount += amount
    current_resources.antimatter.amount += amount
    current_resources.research.amount += amount
    current_resources.population.amount += amount
    current_resources.authority.amount += amount

    repo.set_user_resources(user_id=user_id, resources=current_resources)


if __name__ == "__main__":
    main()
