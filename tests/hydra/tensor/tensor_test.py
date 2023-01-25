# third party
import numpy as np

from hydra.tensor import Tensor


def test_eq_tensor() -> None:
    tensor_1 = Tensor(np.array([1, 2, 3]))
    tensor_2 = Tensor(np.array([1.0, 2.0, 3.0]))

    assert tensor_1 == tensor_2


def test_serializer() -> None:
    tensor = Tensor(np.arange(42))

    tensor_serialized = tensor.serialize()
    tensor_deserialized = Tensor.deserialize(tensor_serialized)
    assert tensor == tensor_deserialized


def test_forward_method() -> None:
    tensor = Tensor(np.array([42]))
    assert tensor.item() == 42


def test_representation() -> None:
    tensor = Tensor(np.array([42]))
    assert str(tensor) == f"Tensor: {tensor.data}"
