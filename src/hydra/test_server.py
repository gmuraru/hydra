# stdlib
import argparse
import uuid

# third party
import numpy as np

from hydra.communication import get_client
from hydra.tensor import Tensor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start one SMPC party server.")
    parser.add_argument(
        "--port", type=str, help="port to listen for incoming requests", required=True
    )

    args = parser.parse_args()
    party = get_client(ip="localhost", port=args.port)

    tensor = Tensor(data=np.array([[1, 2, 3, 4]]))
    id = party.store(tensor)
    # id = uuid.UUID("52ab7a52-9dad-11ed-b8d1-50e085b861ae")
    print(f"Value {party.get(id)}")
