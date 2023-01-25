# stdlib
import argparse
from concurrent import futures
import logging

# third party
import grpc

from hydra.communication.grpc.service import register_api


def serve(port: str, grpc_server_workers: int) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=grpc_server_workers))

    register_api(server)

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logging.info("Server started, listening on %s", port)
    server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start one SMPC party server.")
    parser.add_argument(
        "--port",
        type=int,
        help="port to listen for incoming requests",
        required=True,
    )
    parser.add_argument(
        "--rank",
        type=int,
        help="rank for the client/party",
        required=True,
    )
    parser.add_argument(
        "--grpc_server_workers",
        type=int,
        help="number of threads to serve the requests",
        default=5,
    )

    args = parser.parse_args()
    logging.basicConfig(
        level=logging.INFO,
        filename=f"party_{args.rank}.log",
    )

    serve(args.port, args.grpc_server_workers)
