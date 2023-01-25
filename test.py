from hydra.communication import get_client
from hydra.context import Context
from hydra.context import setup_context

client_1 = get_client("localhost", "50051")
client_2 = get_client("localhost", "50052")

context = Context([client_1, client_2])
setup_context(context)
