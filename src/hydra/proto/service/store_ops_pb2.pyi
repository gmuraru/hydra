from hydra.proto.tensor import tensor_pb2 as _tensor_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClearReply(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ClearRequest(_message.Message):
    __slots__ = ["client_id"]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: int
    def __init__(self, client_id: _Optional[int] = ...) -> None: ...

class GetReply(_message.Message):
    __slots__ = ["tensor"]
    TENSOR_FIELD_NUMBER: _ClassVar[int]
    tensor: _tensor_pb2.Tensor
    def __init__(self, tensor: _Optional[_Union[_tensor_pb2.Tensor, _Mapping]] = ...) -> None: ...

class GetRequest(_message.Message):
    __slots__ = ["client_id", "id"]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    client_id: int
    id: str
    def __init__(self, client_id: _Optional[int] = ..., id: _Optional[str] = ...) -> None: ...

class StoreReply(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class StoreRequest(_message.Message):
    __slots__ = ["client_id", "tensor"]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    TENSOR_FIELD_NUMBER: _ClassVar[int]
    client_id: int
    tensor: _tensor_pb2.Tensor
    def __init__(self, client_id: _Optional[int] = ..., tensor: _Optional[_Union[_tensor_pb2.Tensor, _Mapping]] = ...) -> None: ...

class ViewReply(_message.Message):
    __slots__ = ["ids"]
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ViewRequest(_message.Message):
    __slots__ = ["client_id"]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    client_id: int
    def __init__(self, client_id: _Optional[int] = ...) -> None: ...
