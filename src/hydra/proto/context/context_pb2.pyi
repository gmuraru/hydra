from hydra.proto.communication import client_pb2 as _client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Context(_message.Message):
    __slots__ = ["clients", "rank"]
    CLIENTS_FIELD_NUMBER: _ClassVar[int]
    RANK_FIELD_NUMBER: _ClassVar[int]
    clients: _containers.RepeatedCompositeFieldContainer[_client_pb2.Client]
    rank: int
    def __init__(self, clients: _Optional[_Iterable[_Union[_client_pb2.Client, _Mapping]]] = ..., rank: _Optional[int] = ...) -> None: ...
