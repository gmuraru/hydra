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
            base (int): The base for the encoder.
            precision (int): The precision for the encoder.
        """
        self._precision = precision
        self._base = base
        self._scale = base**precision

    def encode(self, value: np.ndarray) -> np.ndarray:
        """Encode a value using the FixedPoint Encoder.

        Args:
            value (np.ndarray): value to encode

        Returns:
            A uint numpy array representing the encoded value
        """
        long_value = (value * self._scale).astype(np.uint)

        return long_value

    def decode(self, value: np.ndarray) -> np.float32:
        """Decode a value using the FixedPoint Encoder.

        Args:
            value (np.ndarray): Value to decode.

        Returns:
            A float numpy array representing the decoded tensor.

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
    def precision(self):
        """Get the precision for the FixedPrecision Encoder.

        Returns:
            int: precision.
        """
        return self._precision

    @precision.setter
    def precision(self, precision: int) -> None:
        self._precision = precision
        self._scale = self._base**precision

    @property
    def base(self) -> int:
        """Base for the FixedPrecision Encoder.

        Returns:
            int: base
        """
        return self._base

    @base.setter
    def base(self, base: int) -> None:

        self._base = base
        self._scale = base**self._precision

    @property
    def scale(self) -> int:
        """Scale for the FixedPrecision Encoder.

        Returns:
            int: the scale.
        """
        return self._scale

    def __str__(self) -> str:
        """Representation.

        Returns:
            str: The representation.
        """
        type_name = type(self).__name__
        out = f"[{type_name}]: precision: {self._precision}, base: {self._base}"
        return out
