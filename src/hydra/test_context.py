# third party
import numpy as np

from hydra.communication import get_client
from hydra.context import Context
from hydra.context import setup_context
from hydra.tensor import Tensor

client_1 = get_client("localhost", "50051", 1)
client_2 = get_client("localhost", "50052", 2)
client_1.reset_state()
client_2.reset_state()
context = Context([client_1, client_2])
# context = Context([client_1])
setup_context(context)
print(client_1.store_view())
print(client_2.store_view())

tensor = Tensor(data=np.array([[1, 2, 3, 4]]))
id = client_1.store(tensor)

client_1.share_secret(id)
