# stdlib
from unittest.mock import MagicMock
from unittest.mock import patch

from hydra.communication.grpc.client import GRPCClient
from hydra.context import Context
from hydra.context import setup_context


@patch("hydra.communication.client.deserialize")
def test_serializer(client_deserialize_mock: MagicMock) -> None:
    clients = []
    for i in range(3):
        grpc_client = GRPCClient(ip=f"ip_{i}", port=f"port_{i}")
        client = MagicMock(spec_set=GRPCClient, wraps=grpc_client)
        client.client_type = GRPCClient.client_type
        clients.append(client)
    ctx = Context(clients=clients)
    client_deserialize_mock.side_effect = clients

    ctx.rank = 1

    context_serialized = ctx.serialize()
    context_deserialized = Context.deserialize(context_serialized)

    assert ctx == context_deserialized


@patch("hydra.communication.client.deserialize")
def test_setup_context(_: MagicMock) -> None:
    clients = []
    for i in range(3):
        client = MagicMock(spec_set=GRPCClient)
        client.client_type = GRPCClient.client_type
        clients.append(client)
    ctx = Context(clients=clients)

    setup_context(ctx)

    for i in range(3):
        call_context = clients[i].init_context.call_args[0][0]
        assert call_context.rank == i

        call_context.rank = -1
        assert call_context == ctx
