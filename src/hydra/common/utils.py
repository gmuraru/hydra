# stdlib
from typing import Final

# third party
import numpy as np
import numpy.typing as npt

_RING_SIZE_TO_TYPE: Final[dict[int, np.dtype]] = {
    2**32: np.uint32,
    2**64: np.uint64,
}


def generate_random_element(
    generator: np.random.Generator,
    shape: tuple[int],
    ring_size: int = 2**64,
) -> npt.ArrayLike:
    return generator.integers(
        low=0,
        high=ring_size - 1,
        endpoint=True,
        size=shape,
        dtype=_RING_SIZE_TO_TYPE[ring_size],
    )
