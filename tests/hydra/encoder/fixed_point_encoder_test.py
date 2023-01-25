"""Tests for the Fixed Precision Encoder."""
# third party
import numpy as np
import pytest

from hydra.encoder import FixedPointEncoder


def test_fp_encoder_init():
    fp_encoder = FixedPointEncoder(
        base=3,
        precision=8,
    )
    assert fp_encoder.base == 3
    assert fp_encoder.precision == 8
    assert fp_encoder.scale == 3**8


def test_fp_encoding():
    fp_encoder = FixedPointEncoder()
    tensor = np.array([1.2, 2.23, 3.42], dtype=float)
    encoded_tensor = fp_encoder.encode(tensor)
    target_tensor = (tensor * fp_encoder.scale).astype(np.uint)
    assert (encoded_tensor == target_tensor).all()
    assert encoded_tensor.dtype == target_tensor.dtype


def test_fp_decoding():
    fp_encoder = FixedPointEncoder(precision=2, base=10)

    tensor = np.array([212, 132, 314])

    decoded_tensor = fp_encoder.decode(tensor)
    target_tensor = np.array([2.12, 1.32, 3.14])
    assert (decoded_tensor == target_tensor).all()


def test_fp_decoding_value_expcetion():
    """Test that an exception is raised when decoding a wrong value type."""
    fp_encoder = FixedPointEncoder(precision=2, base=10)
    tensor = np.array([2.0, 1.0, -1.0])
    with pytest.raises(ValueError):
        fp_encoder.decode(tensor)


def test_fp_string_representation():
    fp_encoder = FixedPointEncoder(precision=5, base=10)
    assert str(fp_encoder) == "[FixedPointEncoder]: precision: 5, base: 10"
