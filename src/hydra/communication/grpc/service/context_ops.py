# stdlib
import logging
from typing import Iterable
import uuid

# third party
import grpc

from hydra import context as context_manager
from hydra import store as store_manager
from hydra.context import Context
from hydra.proto.service import context_ops_pb2
from hydra.proto.service import context_ops_pb2_grpc


def make_init_request(context: Context) -> context_ops_pb2.InitRequest:
    context_proto = context.serialize()
    return context_ops_pb2.InitRequest(context=context_proto)


def _make_init_response(is_success: bool = True) -> context_ops_pb2.InitReply:
    return context_ops_pb2.InitReply(is_success=is_success)


def make_setup_przs_generators_request(
    ctx_id: int,
) -> context_ops_pb2.SetupPRZSGeneratorsRequest:
    return context_ops_pb2.SetupPRZSGeneratorsRequest(ctx_id=ctx_id)


def _make_setup_przs_response() -> context_ops_pb2.SetupPRZSGeneratorsReply:
    return context_ops_pb2.SetupPRZSGeneratorsReply(is_success=True)


def make_share_secret_request(
    ctx_id: int, id: uuid.UUID
) -> context_ops_pb2.ShareSecretRequest:
    return context_ops_pb2.ShareSecretRequest(ctx_id=ctx_id, id=str(id))


def _make_share_secret_response(
    share_ids: Iterable[uuid.UUID],
) -> context_ops_pb2.ShareSecretReply:
    return context_ops_pb2.ShareSecretReply(ids=[str(id) for id in share_ids])


def make_generate_przs_request(
    ctx_id: int,
    shape: Iterable[int],
) -> context_ops_pb2.GeneratePRZSRequest:
    return context_ops_pb2.GeneratePRZSRequest(ctx_id=ctx_id, shape=shape)


def _make_generate_przs_response(id: uuid.UUID) -> context_ops_pb2.GeneratePRZSReply:
    return context_ops_pb2.GeneratePRZSReply(id=str(id))


def make_reset_request() -> context_ops_pb2.ResetRequest:
    return context_ops_pb2.ResetRequest()


def _make_reset_response() -> context_ops_pb2.ResetReply:
    return context_ops_pb2.ResetReply()


class ContextOps(context_ops_pb2_grpc.ContextOpsServicer):
    def reset(
        self,
        request: context_ops_pb2.ResetRequest,
        context: grpc.RpcContext,
    ) -> context_ops_pb2.ResetReply:
        """Resets the context."""
        logging.info("Processing reset request %s", request)
        context_manager.reset()
        return _make_reset_response()

    def init(
        self,
        request: context_ops_pb2.InitRequest,
        context: grpc.RpcContext,
    ) -> context_ops_pb2.InitReply:
        """Initializes the context with the received one."""
        logging.info("Processing init request %s", request)

        # TODO This context from here gets overwritten
        # Each server instance should come with a clean state

        ctx = Context.deserialize(request.context)
        context_manager.set_context(ctx)
        return _make_init_response()

    def setup_przs_generators(
        self,
        request: context_ops_pb2.SetupPRZSGeneratorsRequest,
        context: grpc.RpcContext,
    ) -> context_ops_pb2.SetupPRZSGeneratorsReply:
        """Setups the pseudo random zero shares generators."""
        logging.info("Processing setup_przs_generators request %s", request)
        ctx = context_manager.get_context(request.ctx_id)
        ctx.setup_przs_generators()
        return _make_setup_przs_response()

    def share_secret(
        self,
        request: context_ops_pb2.ShareSecretRequest,
        context: grpc.RpcContext,
    ) -> context_ops_pb2.ShareSecretReply:
        """Masks the secret/plaintext using the PRZS generators."""
        logging.info("Processing share_secret request %s", request)
        ctx = context_manager.get_context(request.ctx_id)
        data_store = store_manager.get_store(ctx.rank)
        id = uuid.UUID(request.id)
        value = data_store.get(id)
        secret_shape = value.shape
        share = ctx.mask_secret(value)
        share_id = data_store.store(share)
        share_ids = [client.generate_przs(secret_shape) for client in ctx.clients]
        share = ctx.share_secret(value)
        share_ids.append(data_store.store(share))
        return _make_share_secret_response(share_ids)

    def generate_przs(
        self,
        request: context_ops_pb2.GeneratePRZSRequest,
        context: grpc.RpcContext,
    ) -> context_ops_pb2.GeneratePRZSReply:
        """Generates a pseudo random zero share."""
        logging.info("Processing generate_przs request %s", request)

        shape = request.shape
        ctx = context_manager.get_context(request.ctx_id)
        share = ctx.generate_przs(shape=shape)
        data_store = store_manager.get_store(ctx.rank)
        id = data_store.store(share)
        return _make_generate_przs_response(id)
