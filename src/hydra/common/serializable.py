# stdlib
from abc import abstractmethod


class Serializable:
    @abstractmethod
    def serialize(self) -> None:
        ...

    @staticmethod
    @abstractmethod
    def deserialize() -> None:
        ...
