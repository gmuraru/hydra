"""The implementation for the Context.

It is used to identify different SMPC internals like the used protocol,
"""
# future
from __future__ import annotations

# stdlib
import concurrent
import copy
import secrets
from typing import Any
from typing import Iterable

# third party
import numpy as np

from hydra import store as store_manager
from hydra.common import Serializable
from hydra.common import utils
from hydra.communication import client
from hydra.proto.context.context_pb2 import Context as Context_PB2
from hydra.tensor import Tensor


class Context(Serializable):
    """Class used to keep information about computation"""

    def __init__(self, clients: list[client.Client]) -> None:
        """Initializer for the Session.

        Args:
            clients : Used to call the API for each party
            rank: The rank of the party/client

        Raises:
            ValueError: If protocol is not registered or ring size different than 2^64
        """
        self._rank = -1  # Invalid Rank
        self._generator = None
        self._generator_next = None
        self._clients = clients

    @property
    def clients(self) -> list[client.Client]:
        return self._clients

    @property
    def rank(self) -> int:
        return self._rank

    @rank.setter
    def rank(self, value: int) -> int:

        self._rank = value

    def setup_przs_generators(self) -> None:
        """Setup the Pseudo Random Zero Share Generators"""

        assert self._rank >= 0, "Rank should be populated"

        current_seed = secrets.randbelow(2**64)

        prev_client = self._clients[self._rank - 1]
        prev_client.store(Tensor(np.array(current_seed)))
        data_store = store_manager.get_store(id=self._rank)
        next_seed = data_store.get_next_tensor().item()

        current_generator = np.random.default_rng(current_seed)
        next_generator = np.random.default_rng(next_seed)
        self._generators = [current_generator, next_generator]

    def serialize(self) -> Context_PB2:

        clients_proto = [
            client.serialize(client_instance) for client_instance in self._clients
        ]
        return Context_PB2(clients=clients_proto, rank=self.rank)

    @staticmethod
    def deserialize(context: Context_PB2) -> Context:
        clients = [
            client.deserialize(client_instance) for client_instance in context.clients
        ]

        ctx = Context(clients=clients)
        ctx.rank = context.rank
        return ctx

    @property
    def clients(self) -> list[client.Client]:
        return self._clients

    def generate_przs(self, shape: Iterable[int]) -> Tensor:
        share1 = utils.generate_random_element(self._generators[0], shape=shape)
        share2 = utils.generate_random_element(self._generators[1], shape=shape)

        share = Tensor(share1 - share2)
        return share

    def mask_secret(self, tensor: Tensor) -> Tensor:
        shape = tensor.shape
        share = self.generate_przs(shape=tensor.shape) + tensor
        return share

    # def _generate_random_share(
    #     self,
    #     shape: tuple,
    # ) -> list[torch.Tensor]:
    #     """Generate random tensor share for the given shape and ring_size.

    #     Args:
    #         shape (Union[tuple, torch.Size]): Shape for the share.
    #         ring_size (int): ring size to generate share.

    #     The generators are invoked in Counter(CTR) mode as parties with the same initial seeds
    #     could generate correlated random numbers on subsequent invocations.

    #     Returns:
    #         list[np.ndarray] : shares generated by the generators.
    #     """

    #     gen1, gen2 = self.przs_generators

    #     tensor_share1 = generate_random_element(
    #         tensor_type=tensor_type, generator=gen1, shape=shape, max_val=max_val
    #     )

    #     tensor_share2 = generate_random_element(
    #         tensor_type=tensor_type, generator=gen2, shape=shape, max_val=max_val
    #     )

    #     return [tensor_share1, tensor_share2]

    # def przs_generate_random_share(
    #     self,
    #     shape: Union[tuple, torch.Size],
    #     ring_size: Optional[str] = None,
    # ) -> Any:
    #     """Generates a random zero share using the two generators held by a party.

    #     Args:
    #         shape (Union[tuple, torch.Size]): Shape for the share.
    #         ring_size (str): ring size to generate share.

    #     Returns:
    #         Any: ShareTensor or ReplicatedSharedTensor

    #     """
    #     # third party
    #     from sympc.tensor import ReplicatedSharedTensor
    #     from sympc.tensor import ShareTensor

    #     if ring_size is None:
    #         ring_size = self.ring_size
    #     else:
    #         ring_size = int(ring_size)  # 2**64 cannot be serialized.

    #     current_share, next_share = self._generate_random_share(shape, ring_size)

    #     if self.protocol.share_class == ShareTensor:
    #         # It has encoder_precision = 0 such that the value would not be encoded
    #         share = ShareTensor(
    #             data=current_share - next_share,
    #             session_uuid=self.uuid,
    #             config=Config(encoder_precision=0),
    #             ring_size=ring_size,
    #         )
    #     else:
    #         op = ReplicatedSharedTensor.get_op(ring_size, "sub")
    #         share = ReplicatedSharedTensor(
    #             shares=[op(current_share, next_share)],
    #             session_uuid=self.uuid,
    #             config=Config(encoder_precision=0),
    #             ring_size=ring_size,
    #         )
    #     return share

    # def prrs_generate_random_share(
    #     self,
    #     shape: Union[tuple, torch.Size],
    #     ring_size: Optional[str] = None,
    # ) -> Any:
    #     """Generates a random share using the generators held by a party.

    #     Args:
    #         shape (Union[tuple, torch.Size]): Shape for the share.
    #         ring_size (str): ring size to generate share.

    #     Returns:
    #         Any: ShareTensor or ReplicatedSharedTensor

    #     """
    #     # third party
    #     from sympc.tensor import ReplicatedSharedTensor
    #     from sympc.tensor import ShareTensor

    #     if ring_size is None:
    #         ring_size = self.ring_size
    #     else:
    #         ring_size = int(ring_size)  # 2**64 cannot be serialized.

    #     share1, share2 = self._generate_random_share(shape, ring_size)

    #     if self.protocol.share_class == ShareTensor:
    #         # It has encoder_precision = 0 such that the value would not be encoded
    #         share = ShareTensor(
    #             data=share1,
    #             session_uuid=self.uuid,
    #             config=Config(encoder_precision=0),
    #             ring_size=ring_size,
    #         )
    #     else:
    #         share = ReplicatedSharedTensor(
    #             shares=[share1, share2],
    #             session_uuid=self.uuid,
    #             config=Config(encoder_precision=0),
    #             ring_size=ring_size,
    #         )

    #     return share

    # def init_generators(self, seed_current: int, seed_next: int) -> None:
    #     """Initialize the generators - that are used for Pseudo Random Zero Shares.

    #     Args:
    #         seed_current (int): the seed for our party
    #         seed_next (int): thee seed for the next party
    #     """
    #     generator_current = get_new_generator(seed_current)
    #     generator_next = get_new_generator(seed_next)
    #     self.przs_generators = [generator_current, generator_next]

    def __str__(self) -> str:

        val = f"Context\n"
        val = f"{val} | Rank: {self._rank}\n"
        clients_str = "\n\t".join(map(str, self._clients))
        val = f"{val} | Clients:\n\t{clients_str}"
        return val

    __repr__ = __str__

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Context):
            return False

        return other.rank == self.rank and other.clients == self.clients

    def __copy__(self) -> Context:
        new_context = Context(self.clients)
        return new_context


_TIMEOUT_SETUP = 10


def setup_context(context: Context) -> None:
    """Send the context to all clients.

    Args:
        context: The context to initialize the clients with.
    """

    # TODO(george) rank might need to be outside context?
    for client in context.clients:
        client_context = copy.copy(context)
        client_context.rank = (
            client.client_id
        )  # TODO: At the moment the client_id is the rank.
        client.init_context(client_context)

    nr_clients = len(context.clients)
    request_futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=nr_clients) as executor:
        for rank, client in enumerate(context.clients):
            # The PRZS Generators request needs to be sent to all clients
            # because behind the scenes those clients will communicate
            # with one another to exchange some data without the without
            # the Orchestrator (Data Scientist) help.
            request_futures.append(executor.submit(client.setup_przs_generators))

    concurrent.futures.wait(
        request_futures,
        timeout=_TIMEOUT_SETUP,
        return_when=concurrent.futures.ALL_COMPLETED,
    )
