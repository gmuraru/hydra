# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hydra/proto/context/context.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from hydra.proto.communication import client_pb2 as hydra_dot_proto_dot_communication_dot_client__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!hydra/proto/context/context.proto\x12\rhydra.context\x1a&hydra/proto/communication/client.proto\"E\n\x07\x43ontext\x12,\n\x07\x63lients\x18\x01 \x03(\x0b\x32\x1b.hydra.communication.Client\x12\x0c\n\x04rank\x18\x02 \x01(\rb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'hydra.proto.context.context_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CONTEXT._serialized_start=92
  _CONTEXT._serialized_end=161
# @@protoc_insertion_point(module_scope)