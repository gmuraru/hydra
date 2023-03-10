# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from hydra.proto.service import store_ops_pb2 as hydra_dot_proto_dot_service_dot_store__ops__pb2


class StoreOpsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.clear = channel.unary_unary(
                '/hydra.service.StoreOps/clear',
                request_serializer=hydra_dot_proto_dot_service_dot_store__ops__pb2.ClearRequest.SerializeToString,
                response_deserializer=hydra_dot_proto_dot_service_dot_store__ops__pb2.ClearReply.FromString,
                )
        self.get = channel.unary_unary(
                '/hydra.service.StoreOps/get',
                request_serializer=hydra_dot_proto_dot_service_dot_store__ops__pb2.GetRequest.SerializeToString,
                response_deserializer=hydra_dot_proto_dot_service_dot_store__ops__pb2.GetReply.FromString,
                )
        self.store = channel.unary_unary(
                '/hydra.service.StoreOps/store',
                request_serializer=hydra_dot_proto_dot_service_dot_store__ops__pb2.StoreRequest.SerializeToString,
                response_deserializer=hydra_dot_proto_dot_service_dot_store__ops__pb2.StoreReply.FromString,
                )
        self.view = channel.unary_unary(
                '/hydra.service.StoreOps/view',
                request_serializer=hydra_dot_proto_dot_service_dot_store__ops__pb2.ViewRequest.SerializeToString,
                response_deserializer=hydra_dot_proto_dot_service_dot_store__ops__pb2.ViewReply.FromString,
                )


class StoreOpsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def clear(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def store(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def view(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_StoreOpsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'clear': grpc.unary_unary_rpc_method_handler(
                    servicer.clear,
                    request_deserializer=hydra_dot_proto_dot_service_dot_store__ops__pb2.ClearRequest.FromString,
                    response_serializer=hydra_dot_proto_dot_service_dot_store__ops__pb2.ClearReply.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=hydra_dot_proto_dot_service_dot_store__ops__pb2.GetRequest.FromString,
                    response_serializer=hydra_dot_proto_dot_service_dot_store__ops__pb2.GetReply.SerializeToString,
            ),
            'store': grpc.unary_unary_rpc_method_handler(
                    servicer.store,
                    request_deserializer=hydra_dot_proto_dot_service_dot_store__ops__pb2.StoreRequest.FromString,
                    response_serializer=hydra_dot_proto_dot_service_dot_store__ops__pb2.StoreReply.SerializeToString,
            ),
            'view': grpc.unary_unary_rpc_method_handler(
                    servicer.view,
                    request_deserializer=hydra_dot_proto_dot_service_dot_store__ops__pb2.ViewRequest.FromString,
                    response_serializer=hydra_dot_proto_dot_service_dot_store__ops__pb2.ViewReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'hydra.service.StoreOps', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class StoreOps(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def clear(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/hydra.service.StoreOps/clear',
            hydra_dot_proto_dot_service_dot_store__ops__pb2.ClearRequest.SerializeToString,
            hydra_dot_proto_dot_service_dot_store__ops__pb2.ClearReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/hydra.service.StoreOps/get',
            hydra_dot_proto_dot_service_dot_store__ops__pb2.GetRequest.SerializeToString,
            hydra_dot_proto_dot_service_dot_store__ops__pb2.GetReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def store(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/hydra.service.StoreOps/store',
            hydra_dot_proto_dot_service_dot_store__ops__pb2.StoreRequest.SerializeToString,
            hydra_dot_proto_dot_service_dot_store__ops__pb2.StoreReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def view(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/hydra.service.StoreOps/view',
            hydra_dot_proto_dot_service_dot_store__ops__pb2.ViewRequest.SerializeToString,
            hydra_dot_proto_dot_service_dot_store__ops__pb2.ViewReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
