"""GRPC Client implementation."""


# future
from __future__ import annotations

# stdlib
import logging
from typing import Any
from typing import Iterable
import uuid

# third party
import grpc

from hydra.communication.client import Client
from hydra.communication.grpc.service import EndPointAPI
from hydra.communication.grpc.service import build_stubs
from hydra.communication.grpc.service import context_ops
from hydra.communication.grpc.service import store_ops
from hydra.context import Context
from hydra.proto.communication.grpc.client_pb2 import GRPCClient as GRPCClient_PB
from hydra.tensor import Tensor


class GRPCClient(metaclass=Client):
    client_type = "grpc_client"

    def __init__(self, ip: str, port: str, client_id: int) -> None:
        self._ip = ip
        self._port = port
        self._client_id = client_id
        self._channel = grpc.insecure_channel(f"{ip}:{port}")
        self._stubs = build_stubs(self._channel)

    def __del__(self) -> None:
        self._channel.close()

    # Store operations
    def store(self, tensor: Tensor) -> uuid.UUID:
        request = store_ops.make_store_request(self._client_id, tensor)
        logging.info("Sending store request %s", request)
        response = self._stubs[EndPointAPI.STORE].store(request)
        return uuid.UUID(response.id)

    def get(self, id: uuid.UUID) -> Tensor:
        """Gets the tensor with the specified from the client."""
        request = store_ops.make_get_request(self._client_id, id)
        logging.info("Sending get request %s", request)
        response = self._stubs[EndPointAPI.STORE].get(request)
        return Tensor.deserialize(response.tensor)

    def store_view(self) -> list[uuid.UUID]:
        """Gets the ids of items that are in the data store."""
        request = store_ops.make_view_request(self._client_id)
        logging.info("Sending store_view request %s", request)
        response = self._stubs[EndPointAPI.STORE].view(request)
        return [uuid.UUID(id) for id in response.ids]

    # Context operations
    def init_context(self, context: Context) -> bool:
        """Initialize the context in all the clients"""
        request = context_ops.make_init_request(context)
        logging.info("Sending init_context request %s", request)
        response = self._stubs[EndPointAPI.CONTEXT].init(request)
        return response.is_success

    def reset_state(self) -> None:
        """Resets the state of the server."""
        context_request = context_ops.make_reset_request()
        logging.info("Sending reset request %s", context_request)

        store_request = store_ops.make_clear_request(self._client_id)
        logging.info("Sending clear request %s", store_request)
        self._stubs[EndPointAPI.CONTEXT].reset(context_request)
        self._stubs[EndPointAPI.STORE].clear(store_request)

    def setup_przs_generators(self) -> bool:
        """Instructs the servers to initialize the generators
        that will be used to construct pseudo random zero shares.

        Assumption:
            The context should have already been sent to the clients.
        """
        request = context_ops.make_setup_przs_generators_request(ctx_id=self._client_id)
        logging.info("Sending setup_przs_generators request %s", request)
        response = self._stubs[EndPointAPI.CONTEXT].setup_przs_generators(request)
        return response.is_success

    def share_secret(self, id: uuid.UUID) -> list[uuid.UUID]:
        """Splits the the secret into shares."""
        request = context_ops.make_share_secret_request(ctx_id=self._client_id, id=id)
        logging.info("Sending share_secret request %s", request)
        response = self._stubs[EndPointAPI.CONTEXT].share_secret(request)
        return [uuid.UUID(id) for id in response.ids]

    def generate_przs(self, shape: Iterable[int]) -> uuid.UUID:
        """Generate the next Pseudo Random Zero Share"""
        request = context_ops.make_generate_przs_request(
            ctx_id=self._client_id, shape=shape
        )
        logging.info("Sending generate_przs request %s", request)
        response = self._stubs[EndPointAPI.CONTEXT].generate_przs(request)
        id = uuid.UUID(response.id)
        return id

    def serialize(self) -> GRPCClient_PB:
        """Serializes the GRPC Client."""
        return GRPCClient_PB(ip=self._ip, port=self._port, client_id=self._client_id)

    @staticmethod
    def deserialize(client: GRPCClient_PB) -> GRPCClient:
        """Deserializes the GRPC Client."""
        return GRPCClient(ip=client.ip, port=client.port, client_id=client.client_id)

    @property
    def ip(self) -> str:
        return self._ip

    @property
    def port(self) -> str:
        return self._port

    @property
    def client_id(self) -> int:
        return self._client_id

    def __str__(self) -> str:
        """Returns the representation of the GRPC Client."""
        return f"GRPCClient [IP: {self._ip} PORT: {self._port}]"

    __repr__ = __str__

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, GRPCClient):
            return False

        return other.ip == self.ip and other.port == self.port
