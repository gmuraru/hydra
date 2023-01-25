# stdlib
import logging

# third party
import grpc

from hydra.proto.service import share_tensor_ops_pb2
from hydra.proto.service import share_tensor_ops_pb2_grpc


class ShareTensorOps(share_tensor_ops_pb2_grpc.ShareTensorOpsServicer):
    def compute(self, request, context) -> share_tensor_ops_pb2.ComputeReply:
        logging.info("Processing compute request %s", request)
        return share_tensor_ops_pb2.ComputeReply(id="helllo")
