# stdlib
from abc import abstractmethod
import uuid

from hydra.tensor import Tensor


class Store:
    @abstractmethod
    def get(self, id: str) -> Tensor:
        ...

    @abstractmethod
    def set(self, tensor: Tensor) -> uuid.UUID:
        ...

    @abstractmethod
    def get_next_tensor(self, remove: bool) -> Tensor:
        ...

    @abstractmethod
    def item_ids(self) -> list[uuid.UUID]:
        ...

    @abstractmethod
    def clear(self) -> None:
        ...
