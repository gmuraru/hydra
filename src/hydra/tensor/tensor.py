# future
from __future__ import annotations

# stdlib
from abc import abstractmethod
import io
from typing import Any
from typing import Final
from typing import Union

# third party
import numpy as np
import numpy.typing as npt

from hydra.common import Serializable
from hydra.proto.tensor.tensor_pb2 import Tensor as Tensor_PB

# from hydra.context import ctx
# from hydra.tensor import MPCTensor

_FORWARD_ATTRS: Final[set[str]] = {
    "item",
    "shape",
}


class Tensor(Serializable):
    """Base data object.

    Abstraction around a numpy array to handle specific methods
    like serialization/deserialization logic.
    """

    def __init__(self, data: npt.ArrayLike) -> None:
        """Inits Tensor class with data."""
        self._data = data

    @abstractmethod
    def unimplemented_method(self) -> None:
        ...

    # def share(self) -> None:
    #     if not ctx:
    #         raise ValueError(
    #             "Context should be populated. ",
    #             "Make sure to call `setup_context` before sharing!",
    #         )

    #     return MPCTensor

    def __add__(self, other: Union[int, float, npt.ArrayLike, Tensor]) -> Tensor:
        if isinstance(other, (float, int, np.ndarray)):
            return Tensor(self._data + other)
        return Tensor(self._data + other._data)

    __sub__ = unimplemented_method
    __mul__ = unimplemented_method
    __matmul__ = unimplemented_method
    __gt__ = unimplemented_method
    __gte__ = unimplemented_method
    __lt__ = unimplemented_method
    __lte__ = unimplemented_method

    def __getattr__(self, name: str) -> Any:
        """Returns the normal Tensor attribute or the underlying data
        attribute.

        This is used in cases where the attribute is specific to
        the underlying numpy array.
        """
        if name in _FORWARD_ATTRS:
            return getattr(self._data, name)

        raise AttributeError(f"Attribute {name} was not found!")

    @property
    def data(self) -> npt.ArrayLike:
        return self._data

    def serialize(self) -> Tensor_PB:
        """Serializez the tensor."""
        bytes = io.BytesIO()
        np.save(bytes, self._data, allow_pickle=False)
        return Tensor_PB(data=bytes.getvalue())

    def deserialize(tensor: Tensor_PB) -> Tensor:
        """Deserialize the protobuf tensor and returns a new tensor."""
        bytes = io.BytesIO()
        bytes.write(tensor.data)
        bytes.seek(0)
        data = np.load(bytes)
        return Tensor(data)

    def __str__(self) -> str:
        """Returns the representation of the Tensor."""
        return f"Tensor: {self._data}"

    __repr__ = __str__

    def __eq__(self, other: Tensor) -> bool:
        """Checks if two tensors are equal.

        Args:
            other: The object to compare `self` against.

        Returns:
            true if the objects are equal or False
        """
        if not isinstance(other, Tensor):
            return False

        return np.all(self._data == other.data)
