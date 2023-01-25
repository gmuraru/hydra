# future
from __future__ import annotations

# stdlib
from abc import ABCMeta
from abc import abstractmethod
from typing import Iterable
from typing import Type
import uuid

from hydra.context import context
from hydra.proto.communication.client_pb2 import Client as Client_PB
from hydra.tensor.tensor import Tensor


class Client(ABCMeta):
    _registry: dict[str, Type[Client]] = {}

    def __new__(cls: Type[Client], name: str, bases: tuple, namespace: dict) -> Client:
        new_cls = super().__new__(cls, name, bases, namespace)

        if getattr(new_cls, "client_type") is None:
            raise ValueError("client_type should be populated in child")

        if new_cls.client_type in cls._registry:
            raise ValueError(f"{new_cls.client_type} already registered!")

        cls._registry[new_cls.client_type] = new_cls
        return new_cls

    @abstractmethod
    def store(self, tensor: Tensor) -> uuid.UUID:
        ...

    @abstractmethod
    def get(self, id: uuid.UUID) -> Tensor:
        ...

    @abstractmethod
    def store_length(self) -> int:
        ...

    @abstractmethod
    def init_context(self, ctx: context.Context) -> bool:
        ...

    @abstractmethod
    def reset_state(self) -> None:
        ...

    @abstractmethod
    def share_secret(self, id: uuid.UUID) -> list[uuid.UUID]:
        ...

    @abstractmethod
    def generate_przs(self, shape: Iterable[int]) -> uuid.UUID:
        ...


def serialize(client: Client) -> Client_PB:
    field_name = client.client_type
    client_pb = Client_PB(**{field_name: client.serialize()})
    return client_pb


def deserialize(client: Client_PB) -> Client:
    client_type = client.WhichOneof("client")
    class_client = Client._registry[client_type]
    client_serialized = getattr(client, client_type)
    return class_client.deserialize(client_serialized)
