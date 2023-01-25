# stdlib
from concurrent import futures
import contextlib
import socket
from typing import Final
from unittest.mock import MagicMock

# third party
import grpc
import pytest
from pytest_grpc.plugin import FakeChannel
from pytest_grpc.plugin import FakeServer

from hydra.communication.grpc.client import GRPCClient
from hydra.communication.grpc.service import register_api
from hydra.proto.service import context_ops_pb2_grpc
from hydra.proto.service import crypto_ops_pb2_grpc
from hydra.proto.service import share_tensor_ops_pb2_grpc
from hydra.proto.service import store_ops_pb2_grpc

_NR_CLIENTS: Final[int] = 3


@pytest.fixture(scope="module")
def _grpc_servers(request, grpc_interceptors):
    max_workers = request.config.getoption("grpc-max-workers")
    try:
        max_workers = max(request.module.grpc_max_workers, max_workers)
    except AttributeError:
        pass
    pools = []
    servers = []

    for _ in range(_NR_CLIENTS):
        pool = futures.ThreadPoolExecutor(max_workers=max_workers)
        pools.append(pool)
        if request.config.getoption("grpc-fake"):
            servers.append(FakeServer(pool))
        else:
            servers.append(grpc.server(pool, interceptors=grpc_interceptors))
    yield servers

    for pool in pools:
        pool.shutdown(wait=True)


@pytest.fixture(scope="module")
def _grpc_addresses():
    addresses = []
    for _ in range(_NR_CLIENTS):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("localhost", 0))
        addresses.append(f"localhost:{sock.getsockname()[1]}")

    return addresses


@pytest.fixture(scope="module")
def _servers(request, _grpc_servers, _grpc_addresses):
    for server, addr in zip(_grpc_servers, _grpc_addresses):
        register_api(server)

        server.add_insecure_port(addr)
        server.start()

    yield _grpc_servers

    for server in _grpc_servers:
        server.stop(grace=None)


@pytest.fixture(scope="module")
def grpc_create_channels(request, _servers, _grpc_addresses):
    def _create_channel(credentials=None, options=None):
        if request.config.getoption("grpc-fake"):
            return [FakeChannel(server, credentials) for server in _servers]
        if credentials is not None:
            return [
                grpc.secure_channel(addr, credentials, options)
                for addr in _grpc_addresses
            ]
        return [grpc.insecure_channel(addr, options) for addr in _grpc_addresses]

    return _create_channel


@pytest.fixture(scope="module")
def grpc_channels(grpc_create_channels):
    channels = []
    with contextlib.ExitStack() as stack:
        for channel in grpc_create_channels():
            stack.enter_context(channel)
            channels.append(channel)
        yield channels


@pytest.fixture(scope="module")
def grpc_stub_context_ops(grpc_channels):
    return [
        context_ops_pb2_grpc.ContextOpsStub(grpc_channel)
        for grpc_channel in grpc_channels
    ]


@pytest.fixture(scope="module")
def grpc_stub_store_ops(grpc_channels):
    return [
        store_ops_pb2_grpc.StoreOpsStub(grpc_channel) for grpc_channel in grpc_channels
    ]


@pytest.fixture(scope="module")
def grpc_stub_share_tensor_ops(grpc_channels):
    return [
        share_tensor_ops_pb2_grpc.ShareTensorOpsStub(grpc_channel)
        for grpc_channel in grpc_channels
    ]


@pytest.fixture(scope="module")
def grpc_stub_crypto_ops_ops(grpc_channels):
    return [
        crypto_ops_pb2_grpc.CryptoOpsStub(grpc_channel)
        for grpc_channel in grpc_channels
    ]


@pytest.fixture
def grpc_clients(request, _grpc_addresses) -> list[GRPCClient]:
    clients = []
    ports = [address.split(":")[-1] for address in _grpc_addresses]
    for port in ports:
        grpc_client = GRPCClient(ip=f"localhost", port=port)
        if request.config.getoption("grpc-fake"):
            client = MagicMock(spec_set=GRPCClient, wraps=grpc_client)
            client.client_type = GRPCClient.client_type
        else:
            client = grpc_client

        clients.append(client)
        client.reset_state()
    yield clients
