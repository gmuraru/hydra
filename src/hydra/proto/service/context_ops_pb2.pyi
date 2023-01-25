from hydra.proto.context import context_pb2 as _context_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GeneratePRZSReply(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GeneratePRZSRequest(_message.Message):
    __slots__ = ["ctx_id", "shape"]
    CTX_ID_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    ctx_id: int
    shape: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, ctx_id: _Optional[int] = ..., shape: _Optional[_Iterable[int]] = ...) -> None: ...

class InitReply(_message.Message):
    __slots__ = ["is_success"]
    IS_SUCCESS_FIELD_NUMBER: _ClassVar[int]
    is_success: bool
    def __init__(self, is_success: bool = ...) -> None: ...

class InitRequest(_message.Message):
    __slots__ = ["context"]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    context: _context_pb2.Context
    def __init__(self, context: _Optional[_Union[_context_pb2.Context, _Mapping]] = ...) -> None: ...

class ResetReply(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ResetRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class SetupPRZSGeneratorsReply(_message.Message):
    __slots__ = ["is_success"]
    IS_SUCCESS_FIELD_NUMBER: _ClassVar[int]
    is_success: bool
    def __init__(self, is_success: bool = ...) -> None: ...

class SetupPRZSGeneratorsRequest(_message.Message):
    __slots__ = ["ctx_id"]
    CTX_ID_FIELD_NUMBER: _ClassVar[int]
    ctx_id: int
    def __init__(self, ctx_id: _Optional[int] = ...) -> None: ...

class ShareSecretReply(_message.Message):
    __slots__ = ["ids"]
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class ShareSecretRequest(_message.Message):
    __slots__ = ["ctx_id", "id"]
    CTX_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ctx_id: int
    id: str
    def __init__(self, ctx_id: _Optional[int] = ..., id: _Optional[str] = ...) -> None: ...
