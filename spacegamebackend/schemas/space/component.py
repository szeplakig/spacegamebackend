from abc import abstractmethod


class Component:
    def __init__(self, *, title: str) -> None:
        self.title = title
        self.category = self.__class__.__qualname__

    @abstractmethod
    def to_dict(self) -> dict:
        pass
