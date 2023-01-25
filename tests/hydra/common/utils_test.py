# third party
import numpy as np

from hydra.common import utils


def test_generate_random_element() -> None:
    generator = np.random.default_rng()
    shape = (42, 32, 32)
    ring_size = 2**32
    value = utils.generate_random_element(
        generator,
        shape=shape,
        ring_size=ring_size,
    )

    assert np.all(0 <= value) and np.all(value <= ring_size)
    assert value.shape == shape
