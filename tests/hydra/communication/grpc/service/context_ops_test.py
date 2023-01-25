""" Tests the context operations logic from the GRPC server side."""
# stdlib
from unittest.mock import patch

# third party
import numpy as np

from hydra.communication.grpc.client import GRPCClient
from hydra.communication.grpc.service import EndPointAPI
from hydra.communication.grpc.service import context_ops
from hydra.context import Context
from hydra.proto.service import context_ops_pb2_grpc
from hydra.proto.service import store_ops_pb2_grpc
from hydra.tensor import Tensor


def test_init(
    grpc_clients: GRPCClient,
    grpc_stub_context_ops: list[context_ops_pb2_grpc.ContextOpsStub],
) -> None:
    context = Context(clients=grpc_clients)
    context.rank = 2
    request = context_ops.make_init_request(context)
    grpc_stub_context_ops[0].init(request)


def test_setup_przs_generators(
    grpc_clients: GRPCClient,
    grpc_stub_context_ops: list[context_ops_pb2_grpc.ContextOpsStub],
    grpc_stub_store_ops: list[store_ops_pb2_grpc.StoreOpsStub],
) -> None:
    nr_clients = len(grpc_clients)
    stubs = [
        {EndPointAPI.STORE: grpc_store_stub} for grpc_store_stub in grpc_stub_store_ops
    ] * nr_clients
    with patch("hydra.communication.grpc.client.build_stubs", side_effect=stubs):
        for rank, grpc_context_stub in enumerate(grpc_stub_context_ops):
            context = Context(clients=grpc_clients)
            context.rank = rank
            request = context_ops.make_init_request(context)
            is_success = grpc_context_stub.init(request)
            assert is_success

    request = context_ops.make_setup_przs_generators_request()
    responses = []
    for grpc_context_stub in grpc_stub_context_ops:
        responses.append(grpc_context_stub.setup_przs_generators(request))

    assert all(responses)


def test_generate_przs(
    grpc_clients: GRPCClient,
    grpc_stub_context_ops: list[context_ops_pb2_grpc.ContextOpsStub],
    grpc_stub_store_ops: list[store_ops_pb2_grpc.StoreOpsStub],
) -> None:
    # TODO A lot of duplicate code with the previous test
    nr_clients = len(grpc_clients)
    stubs = []
    for grpc_context_stub, grpc_store_stub in zip(
        grpc_stub_context_ops, grpc_stub_store_ops
    ):
        stubs.append(
            {
                EndPointAPI.CONTEXT: grpc_context_stub,
                EndPointAPI.STORE: grpc_store_stub,
            }
        )
    stubs *= nr_clients
    with patch("hydra.communication.grpc.client.build_stubs", side_effect=stubs):
        for rank, grpc_context_stub in enumerate(grpc_stub_context_ops):
            context = Context(clients=grpc_clients)
            context.rank = rank
            request = context_ops.make_init_request(context)
            is_success = grpc_context_stub.init(request)
            assert is_success

    responses = []
    for grpc_context_stub in grpc_stub_context_ops:
        responses.append(grpc_context_stub.setup_przs_generators(request))

    assert all(responses)

    przs_ids = []
    shape = (3, 54, 54)
    for client in grpc_clients:
        przs_ids.append(client.generate_przs(shape))

    tensors = [client.get(id) for id, client in zip(przs_ids, grpc_clients)]
    assert all(tensor.shape == shape for tensor in tensors)
    print(tensors[0])
    assert sum(tensors) == Tensor(np.zeros(shape))


# def test_share_secret(
#     grpc_clients: GRPCClient,
#     grpc_stub_context_ops: list[context_ops_pb2_grpc.ContextOpsStub],
#     grpc_stub_store_ops: list[store_ops_pb2_grpc.StoreOpsStub],
# ) -> None:
#     # TODO A lot of duplicate code with the previous test
#     nr_clients = len(grpc_clients)
#     stubs = []
#     for grpc_context_stub, grpc_store_stub in zip(
#         grpc_stub_context_ops, grpc_stub_store_ops
#     ):
#         stubs.append(
#             {
#                 EndPointAPI.CONTEXT: grpc_context_stub,
#                 EndPointAPI.STORE: grpc_store_stub,
#             }
#         )
#     stubs *= nr_clients
#     with patch("hydra.communication.grpc.client.build_stubs", side_effect=stubs):
#         for rank, grpc_context_stub in enumerate(grpc_stub_context_ops):
#             context = Context(clients=grpc_clients)
#             context.rank = rank
#             request = context_ops.make_init_request(context)
#             is_success = grpc_context_stub.init(request)
#             assert is_success

#     responses = []
#     for grpc_context_stub in grpc_stub_context_ops:
#         responses.append(grpc_context_stub.setup_przs_generators(request))

#     assert all(responses)

#     id = grpc_clients[1].store(Tensor(np.array([1, 2, 3])))
#     ids = grpc_clients[1].share_secret(id)

#     for id, client in zip(ids, grpc_clients):
#         assert id in client.store_view()
