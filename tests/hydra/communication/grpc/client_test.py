# stdlib
from unittest.mock import MagicMock
import uuid

# third party
import numpy as np

from hydra.communication.grpc.client import GRPCClient
from hydra.communication.grpc.service import EndPointAPI
from hydra.context import Context
from hydra.proto.service import context_ops_pb2
from hydra.proto.service import context_ops_pb2_grpc
from hydra.proto.service import store_ops_pb2
from hydra.proto.service import store_ops_pb2_grpc
from hydra.tensor import Tensor


def test_store() -> None:
    id = uuid.uuid1()
    store_ops_stub = MagicMock(spec_set=store_ops_pb2_grpc.StoreOps)
    store_ops_stub.store.return_value = store_ops_pb2.StoreReply(id=str(id))

    client = GRPCClient("dummy_ip", "dummy_port")
    client._stubs = {EndPointAPI.STORE: store_ops_stub}

    response_id = client.store(Tensor(np.array(4)))
    assert response_id == id


def test_get() -> None:
    tensor = Tensor(np.array([1, 2, 3]))
    store_ops_stub = MagicMock(spec_set=store_ops_pb2_grpc.StoreOps)
    store_ops_stub.get.return_value = store_ops_pb2.GetReply(tensor=tensor.serialize())
    client = GRPCClient("dummy_ip", "dummy_port")
    client._stubs = {EndPointAPI.STORE: store_ops_stub}

    id_obj = uuid.uuid1()
    response_tensor = client.get(id_obj)

    assert response_tensor == tensor


def test_view() -> None:
    store_ops_stub = MagicMock(spec_set=store_ops_pb2_grpc.StoreOps)
    ids = [uuid.uuid1(), uuid.uuid1()]
    ids_proto = [str(id) for id in ids]
    store_ops_stub.view.return_value = store_ops_pb2.ViewReply(ids=ids_proto)
    client = GRPCClient("dummy_ip", "dummy_port")
    client._stubs = {EndPointAPI.STORE: store_ops_stub}

    ids_view = client.store_view()

    assert ids_view == ids


def test_init_context() -> None:
    context_ops_stub = MagicMock(spec_set=context_ops_pb2_grpc.ContextOps)
    context_ops_stub.init.return_value = context_ops_pb2.InitReply(is_success=True)
    client = GRPCClient(f"dummy_ip", "dummy_port")
    client._stubs = {EndPointAPI.CONTEXT: context_ops_stub}

    context = Context(clients=[client])
    context.rank = 0
    is_success = client.init_context(context)

    assert is_success is True


def test_setup_przs_generators() -> None:
    context_ops_stub = MagicMock(spec_set=context_ops_pb2_grpc.ContextOps)
    context_ops_stub.setup_przs_generators.return_value = (
        context_ops_pb2.SetupPRZSGeneratorsReply(is_success=True)
    )

    client = GRPCClient("dummy_ip", "dummy_port")
    client._stubs = {EndPointAPI.CONTEXT: context_ops_stub}

    context = Context(clients=[client])
    context.rank = 0
    is_success = client.setup_przs_generators()
    assert is_success is True


def test_serializer() -> None:
    client = GRPCClient("dummy_ip", "dummy_port")
    client_serialized = client.serialize()
    client_deserialized = GRPCClient.deserialize(client_serialized)
    assert client_deserialized == client


def test_representation() -> None:
    client = GRPCClient("dummy_ip", "dummy_port")
    return str(client) == "GRPCClient:\n\tdummy_ip\n\tdummy_port"
