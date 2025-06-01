from dataclasses import dataclass

import pytest

from spacegamebackend.utils.component_store import ComponentStore
from spacegamebackend.utils.sortable_component import ComponentKey, SortableComponent


class DummyComponent(SortableComponent):
    @dataclass(frozen=True, slots=True)
    class Key(ComponentKey):
        value: int

    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def hash_key(self) -> Key:
        return self.Key(self.value)


class OtherComponent(SortableComponent):
    @dataclass(frozen=True, slots=True)
    class Key(ComponentKey):
        value: int

    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def hash_key(self) -> Key:
        return self.Key(self.value)


class TestComponentStore:
    @pytest.fixture
    def component_store(self) -> ComponentStore:
        return ComponentStore([])

    @pytest.fixture
    def component_zero(self) -> DummyComponent:
        return DummyComponent(0)

    @pytest.fixture
    def component_zero_in_store(
        self, component_store: ComponentStore, component_zero: DummyComponent
    ) -> DummyComponent:
        component_store.add_component(component_zero)
        return component_zero

    @pytest.fixture
    def component_one(self) -> DummyComponent:
        return DummyComponent(1)

    @pytest.fixture
    def component_one_in_store(self, component_store: ComponentStore, component_one: DummyComponent) -> DummyComponent:
        component_store.add_component(component_one)
        return component_one

    @pytest.fixture
    def other_component(self) -> OtherComponent:
        return OtherComponent(0)

    @pytest.fixture
    def other_component_in_store(
        self, component_store: ComponentStore, other_component: OtherComponent
    ) -> OtherComponent:
        component_store.add_component(other_component)
        return other_component

    def test_add_component(self, component_store: ComponentStore, component_zero: DummyComponent) -> None:
        component_store.add_component(component_zero)
        assert component_zero.hash_key() in component_store.components
        assert component_zero in component_store.components.values()

    def test_get_components_of_type(
        self,
        component_store: ComponentStore,
        component_zero_in_store: DummyComponent,
        component_one_in_store: DummyComponent,
        other_component_in_store: OtherComponent,
    ) -> None:
        assert component_store.get_components_of_type(DummyComponent) == [
            component_zero_in_store,
            component_one_in_store,
        ]

    def test_get_components(
        self,
        component_store: ComponentStore,
        component_zero_in_store: DummyComponent,
        component_one_in_store: DummyComponent,
        other_component_in_store: OtherComponent,
    ) -> None:
        component_store.add_component(component_zero_in_store)
        component_store.add_component(component_one_in_store)
        component_store.add_component(other_component_in_store)
        assert component_store.get_components() == [
            component_zero_in_store,
            component_one_in_store,
            other_component_in_store,
        ]

    def test_has_component__empty_store(
        self,
        component_store: ComponentStore,
        component_zero: DummyComponent,
    ) -> None:
        assert component_store.has_component(component_zero) is False

    def test_has_component__component_in_store(
        self,
        component_store: ComponentStore,
        component_zero_in_store: DummyComponent,
    ) -> None:
        assert component_store.has_component(component_zero_in_store) is True

    def test_has_components__empty_store(self) -> None:
        component_store = ComponentStore[DummyComponent | OtherComponent]([])
        assert component_store.has_components([]) is True

    def test_has_components__components_in_store(
        self,
        component_store: ComponentStore,
        component_zero_in_store: DummyComponent,
        component_one_in_store: DummyComponent,
    ) -> None:
        assert component_store.has_components([component_zero_in_store, component_one_in_store]) is True
