from hydra.proto.communication.grpc import client_pb2 as _client_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Client(_message.Message):
    __slots__ = ["grpc_client"]
    GRPC_CLIENT_FIELD_NUMBER: _ClassVar[int]
    grpc_client: _client_pb2.GRPCClient
    def __init__(self, grpc_client: _Optional[_Union[_client_pb2.GRPCClient, _Mapping]] = ...) -> None: ...
