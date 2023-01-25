""" Tests the store operations logic from the GRPC server side."""

# stdlib
import uuid

# third party
import numpy as np

from hydra.communication.grpc.client import GRPCClient
from hydra.communication.grpc.service import store_ops
from hydra.proto.service import store_ops_pb2_grpc
from hydra.tensor import Tensor


def test_store_get(
    grpc_clients: GRPCClient,
    grpc_stub_store_ops: list[store_ops_pb2_grpc.StoreOpsStub],
) -> None:
    grpc_client = grpc_clients[0]
    grpc_stub = grpc_stub_store_ops[0]

    tensor = Tensor(np.array([1, 2, 3]))
    store_request = store_ops.make_store_request(tensor)
    store_response = grpc_stub.store(store_request)
    id = uuid.UUID(store_response.id)
    get_request = store_ops.make_get_request(id)
    get_response = grpc_stub.get(get_request)

    tensor_retrieved = Tensor.deserialize(get_response.tensor)
    assert tensor_retrieved == tensor


def test_view(
    grpc_clients: list[GRPCClient],
    grpc_stub_store_ops: list[store_ops_pb2_grpc.StoreOpsStub],
) -> None:
    grpc_client = grpc_clients[0]
    grpc_stub = grpc_stub_store_ops[0]

    tensor = Tensor(np.array([1, 2, 3]))
    store_request = store_ops.make_store_request(tensor)

    ids = []
    for _ in range(3):
        store_response = grpc_stub.store(store_request)
        id = uuid.UUID(store_response.id)
        ids.append(id)

    print(ids)
    view_request = store_ops.make_view_request()
    view_response = grpc_stub.view(view_request)
