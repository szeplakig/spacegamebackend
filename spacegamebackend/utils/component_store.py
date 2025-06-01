from spacegamebackend.utils.sortable_component import ComponentKey, SortableComponent


class ComponentStore[C: SortableComponent]:
    def __init__(self, components: list[C]) -> None:
        self.components: dict[ComponentKey, C] = {component.hash_key(): component for component in components}

    def add_component(self, component: C) -> None:
        self.components[component.hash_key()] = component

    def get_components_of_type[T](self, component_type: type[T]) -> list[T]:
        return [component for component in self.components.values() if isinstance(component, component_type)]

    def get_components[T](self, exclude: set[type[T]] | None = None) -> list[C]:
        exclude = exclude or set()
        return [component for component in self.components.values() if type(component) not in exclude]

    def has_component(self, component: C) -> bool:
        return component.hash_key() in self.components

    def has_components(self, components: list[C]) -> bool:
        return all(self.has_component(component) for component in components)

    def clear(self) -> None:
        self.components.clear()
