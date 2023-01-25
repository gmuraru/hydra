"""Registration logic for specific gRPC API."""

# stdlib
import enum
from typing import Any

# third party
import grpc

from hydra.communication.grpc.service.context_ops import ContextOps
from hydra.communication.grpc.service.crypto_ops import CryptoOps
from hydra.communication.grpc.service.share_tensor_ops import ShareTensorOps
from hydra.communication.grpc.service.store_ops import StoreOps
from hydra.proto.service import context_ops_pb2_grpc
from hydra.proto.service import crypto_ops_pb2_grpc
from hydra.proto.service import share_tensor_ops_pb2_grpc
from hydra.proto.service import store_ops_pb2_grpc


class EndPointAPI(enum.Enum):
    SHARE = "SHARE"
    STORE = "STORE"
    CONTEXT = "CONTEXT"


def register_api(server: grpc.Server) -> None:
    share_tensor_ops_pb2_grpc.add_ShareTensorOpsServicer_to_server(
        ShareTensorOps(),
        server,
    )
    store_ops_pb2_grpc.add_StoreOpsServicer_to_server(
        StoreOps(),
        server,
    )
    context_ops_pb2_grpc.add_ContextOpsServicer_to_server(
        ContextOps(),
        server,
    )


def build_stubs(channel: grpc.Channel) -> dict[EndPointAPI, Any]:
    stubs = {
        EndPointAPI.SHARE: share_tensor_ops_pb2_grpc.ShareTensorOpsStub(channel),
        EndPointAPI.STORE: store_ops_pb2_grpc.StoreOpsStub(channel),
        EndPointAPI.CONTEXT: context_ops_pb2_grpc.ContextOpsStub(channel),
    }
    return stubs
