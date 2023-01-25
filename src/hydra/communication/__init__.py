from hydra.communication.grpc.client import GRPCClient


def get_client(ip: str, port: str, client_id: int) -> GRPCClient:
    # TODO: Replace client_id with something else
    assert client_id > 0, "Client id should be a positive number"
    return GRPCClient(ip, port, client_id)


__all__ = ["get_client"]
