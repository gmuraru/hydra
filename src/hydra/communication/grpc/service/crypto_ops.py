# stdlib
import logging

from hydra.proto.service import crypto_ops_pb2
from hydra.proto.service import crypto_ops_pb2_grpc


def _make_init_przs_generators_response() -> crypto_ops_pb2.InitPRZSGeneratorReply:
    return crypto_ops_pb2.InitPRZSGeneratorReply(True)


class CryptoOps(crypto_ops_pb2_grpc.CryptoOpsServicer):
    def init_przs_generators(
        self, request, context
    ) -> crypto_ops_pb2.InitPRZSGeneratorReply:
        logging.info("Processing InitPRZSGenerators request %s", request)

        return _make_init_przs_generators_response()
