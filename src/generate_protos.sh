#!/bin/bash

python -m grpc_tools.protoc -Iproto_src --python_out=. --pyi_out=. --grpc_python_out=. $(find proto_src/hydra/proto/service -name "*.proto")
python -m grpc_tools.protoc -Iproto_src --python_out=. --pyi_out=. $(find proto_src/hydra/proto/{context,tensor,communication} -name "*.proto")
