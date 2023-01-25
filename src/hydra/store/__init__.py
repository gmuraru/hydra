# stdlib
from collections import defaultdict

from hydra.store.memory_store import InMemoryStore

_data_store = defaultdict(InMemoryStore)


def get_store(id: int = 0) -> InMemoryStore:
    """Returns the store from the specified id."""
    return _data_store[id]


__all__ = ["get_store"]
