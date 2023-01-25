# stdlib
import logging
import uuid

# third party
import grpc

from hydra import store as store_manager
from hydra.proto.service import store_ops_pb2
from hydra.proto.service import store_ops_pb2_grpc
from hydra.tensor import Tensor


def make_get_request(client_id: int, id: uuid.UUID) -> store_ops_pb2.GetRequest:
    return store_ops_pb2.GetRequest(client_id=client_id, id=str(id))


def _make_get_reply(tensor: Tensor) -> store_ops_pb2.GetReply:
    tensor_proto = tensor.serialize()
    return store_ops_pb2.GetReply(tensor=tensor_proto)


def make_store_request(client_id: int, tensor: Tensor) -> store_ops_pb2.StoreRequest:
    tensor_proto = tensor.serialize()
    return store_ops_pb2.StoreRequest(client_id=client_id, tensor=tensor_proto)


def _make_store_reply(id: uuid.UUID) -> store_ops_pb2.StoreRequest:
    return store_ops_pb2.StoreReply(id=str(id))


def make_view_request(client_id: int) -> store_ops_pb2.ViewRequest:
    return store_ops_pb2.ViewRequest(client_id=client_id)


def _make_view_reply(ids: list[uuid.UUID]) -> store_ops_pb2.ViewReply:
    ids_proto = [str(id) for id in ids]
    return store_ops_pb2.ViewReply(ids=ids_proto)


def make_clear_request(client_id: int) -> store_ops_pb2.ClearRequest:
    return store_ops_pb2.ClearRequest(client_id=client_id)


def _make_clear_reply() -> store_ops_pb2.ClearReply:
    return store_ops_pb2.ClearReply()


class StoreOps(store_ops_pb2_grpc.StoreOpsServicer):
    def get(
        self,
        request: store_ops_pb2.GetRequest,
        context: grpc.RpcContext,
    ) -> store_ops_pb2.GetReply:
        logging.info("Processing get request %s", request)
        id = uuid.UUID(request.id)
        data_store = store_manager.get_store(request.client_id)
        object = data_store.get(id)
        return _make_get_reply(object)

    def store(
        self,
        request: store_ops_pb2.StoreRequest,
        context: grpc.RpcContext,
    ) -> store_ops_pb2.StoreReply:
        logging.info("Processing store request %s", request)
        tensor = Tensor.deserialize(request.tensor)
        data_store = store_manager.get_store(request.client_id)
        id = data_store.store(tensor)
        return _make_store_reply(id)

    def view(
        self,
        request: store_ops_pb2.ViewRequest,
        context: grpc.RpcContext,
    ) -> store_ops_pb2.ViewReply:
        logging.info("Processing view request %s", request)
        data_store = store_manager.get_store(request.client_id)
        item_ids = data_store.item_ids()
        return _make_view_reply(item_ids)

    def clear(
        self,
        request: store_ops_pb2.ClearRequest,
        context: grpc.RpcContext,
    ) -> store_ops_pb2.ClearReply:
        logging.info("Processing clear request %s", request)
        data_store = store_manager.get_store(request.client_id)
        data_store.clear()
        return _make_clear_reply()
