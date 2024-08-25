from abc import abstractmethod
from typing import Any


class ABCExtension:
    children = []

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.children.append(cls)

    def __getattribute__(self, name: str) -> Any:
        if name == "children":
            return []
        return super().__getattribute__(name)

    @property
    @abstractmethod
    def ENABLED(self) -> bool:
        return False
