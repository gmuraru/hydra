"""Class used to represent a share owned by a party."""

# stdlib
from typing import Optional

# third party
import numpy as np

from hydra.encoder import FixedPointEncoder
from hydra.tensor import Tensor


class ShareTensor(Tensor):
    """Single Share representation.

    Arguments:
        data: the share a party holds
        encoder_base: the base for the encoder
        encoder_precision: the precision for the encoder
        ring_size: field used for the operations applied on the shares

    Attributes:
        tensor: The value of the share
    """

    def __init__(
        self,
        data: Optional[np.ndarray] = None,
        ring_size: int = 2**64,
    ) -> None:
        """Initialize ShareTensor.

        Args:
            data (Optional[Any]): The share a party holds. Defaults to None
            config (Config): The configuration where we keep the encoder precision and base.
            session_uuid (Optional[UUID]): Used to keep track of a share that is associated with a
                remote session
            ring_size (int): field used for the operations applied on the shares
                Defaults to 2**64
        """
        self.fp_encoder = FixedPointEncoder(
            base=config.encoder_base, precision=config.encoder_precision
        )

        self.tensor: Optional[torch.Tensor] = None
        if data is not None:
            tensor_type = get_type_from_ring(ring_size)
            self.tensor = self._encode(data).to(tensor_type)
