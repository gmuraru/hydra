"""The implementation for the Fixed Point Encoder.

The implementation is taken from the Facebook Research Project: CrypTen
Website: https://crypten.ai/
GitHub: https://github.com/facebookresearch/CrypTen
"""


# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Part of the code is from the CrypTen Facebook Project

# third party
import numpy as np


class FixedPointEncoder:
    """Encoding/decoding a tensor to/from a fixed precision representation.

    This class was inspired from the Facebook Research - CrypTen project

    Attributes:
        _precision (int): the precision for the encoder
        _base (int): the base for the encoder
        _scale (int): the scale used for encoding/decoding
    """

    __slots__ = {"_precision", "_base", "_scale"}

    def __init__(self, base: int = 2, precision: int = 16):
        """Initialize FP Encoder.

        Args:
            base: The base for the encoder.
            precision : The precision for the encoder.
        """
        self._precision = precision
        self._base = base
        self._scale = base**precision

    def encode(self, value: np.ndarray) -> np.ndarray:
        """Encodes a value using the FixedPoint Encoder.

        Args:
            value: value to encode

        Returns:
            Thwe encoded value
        """
        long_value = (value * self._scale).astype(np.uint)

        return long_value

    def decode(self, value: np.ndarray) -> np.float32:
        """Decodes a value using the FixedPoint Encoder.

        Args:
            value: A value to decode.

        Returns:
            The decoded value.

        Raises:
            ValueError: If value is not a numpy uint value
        """
        if np.issubdtype(value.dtype, float):
            raise ValueError(
                f"Expected value to be a 'uint' numpy array! Found type {type(value)}."
            )

        tensor = value
        if self._precision == 0:
            return tensor

        correction = (tensor < 0).astype(int)
        dividend = tensor // self._scale - correction
        remainder = tensor % self._scale
        remainder += (remainder == 0).astype(int) * self._scale * correction

        tensor = dividend.astype(float) + remainder.astype(float) / self._scale
        return tensor

    @property
    def precision(self) -> int:
        """Returns the precision for the FP Encoder."""
        return self._precision

    @precision.setter
    def precision(self, precision: int) -> None:
        """Sets the precision for the FP Encoder."""
        self._precision = precision
        self._scale = self._base**precision

    @property
    def base(self) -> int:
        """Returns the base for the FP Encoder."""
        return self._base

    @base.setter
    def base(self, base: int) -> None:
        """Sets the base for the FP Encoder."""
        self._base = base
        self._scale = base**self._precision

    @property
    def scale(self) -> int:
        """Returns for the FP Encoder."""
        return self._scale

    def __str__(self) -> str:
        """Returns the string representation for the FP Encoder."""
        type_name = type(self).__name__
        out = f"[{type_name}]: precision: {self._precision}, base: {self._base}"
        return out
