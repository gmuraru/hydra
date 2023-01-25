""" Tests the in memory store."""

# stdlib
import uuid

# third party
import numpy as np
import pytest

from hydra.store import InMemoryStore
from hydra.tensor import Tensor


def test_get_empty_store() -> None:
    data_store = InMemoryStore()
    assert data_store.get(uuid.uuid1()) is None


def test_store_get() -> None:
    data_store = InMemoryStore()
    tensor = Tensor(np.array([1, 2, 3]))
    id = data_store.store(tensor)

    tensor_retrieved = data_store.get(id)

    assert tensor_retrieved == tensor

    # It should remain in the store
    tensor_retrieved = data_store.get(id)
    assert tensor_retrieved == tensor


def test_get_next_tensor_no_remove() -> None:
    data_store = InMemoryStore()
    tensor = Tensor(np.array([1, 2, 3]))
    data_store.store(tensor)

    tensor_retrieved = data_store.get_next_tensor(remove_item=False)
    assert tensor_retrieved == tensor

    tensor_retrieved = data_store.get_next_tensor(remove_item=False)
    assert tensor_retrieved == tensor


def test_get_next_tensor_with_remove() -> None:
    data_store = InMemoryStore()
    tensor = Tensor(np.array([1, 2, 3]))
    data_store.store(tensor)

    tensor_retrieved = data_store.get_next_tensor()
    assert tensor_retrieved == tensor

    with pytest.raises(TimeoutError):
        data_store.get_next_tensor(timeout=0.01)


def test_item_ids() -> None:
    data_store = InMemoryStore()
    tensor = Tensor(np.array([1, 2, 3]))
    ids = [data_store.store(tensor) for _ in range(3)]

    assert data_store.item_ids() == ids


def test_clear() -> None:
    data_store = InMemoryStore()
    tensor = Tensor(np.array([1, 2, 3]))
    ids = [data_store.store(tensor) for _ in range(3)]

    data_store.clear()

    for id in ids:
        assert data_store.get(id) is None
