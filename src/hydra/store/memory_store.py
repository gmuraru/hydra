# stdlib
from collections import OrderedDict
import threading
from typing import Optional
import uuid

from hydra.store.store import Store
from hydra.tensor import Tensor


class InMemoryStore(Store):
    def __init__(self) -> None:
        self._store: dict[uuid.UUID, Tensor] = OrderedDict()
        self._condition = threading.Condition()

    def get(self, id: uuid.UUID) -> Optional[Tensor]:
        with self._condition:
            return self._store.get(id)

    def get_next_tensor(
        self,
        timeout: Optional[int] = None,
        remove_item: bool = True,
    ) -> Tensor:
        with self._condition:
            if not self._store:
                acquired_lock = self._condition.wait(timeout=timeout)
                if not acquired_lock:
                    raise TimeoutError("There was no item added in the store!")
            if remove_item:
                _, item = self._store.popitem(last=False)
            else:
                _, item = next(iter(self._store.items()))

            return item

    def store(self, tensor: Tensor) -> uuid.UUID:
        id = uuid.uuid1()
        with self._condition:
            self._store[id] = tensor
            self._condition.notify_all()
            return id

    def item_ids(self) -> list[uuid.UUID]:
        with self._condition:
            return list(self._store.keys())

    def clear(self) -> None:
        with self._condition:
            self._store.clear()
