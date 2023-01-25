"""Context information about parties that are involved in the protocol.

All the parties should have the same information.
"""

# stdlib
from typing import Optional

from hydra.context.context import Context
from hydra.context.context import setup_context

# Contextes that should be populated during the communication
_ctxs: dict[int, Context] = {}


def set_context(context: Context) -> None:
    """Sets the context.

    In a testing/local scenario there might be more contextes in the
    on the same machine.
    Example: using gRPC servers on the same machine and with no container based

    In a real scenario there will be only one context per deployed server and
    those server will live on different machines.

    Arguments:
        context: Context to be registered
    """
    id = context.rank
    if id in _ctxs:
        raise ValueError(f"Id {id} was already used!")

    _ctxs[id] = context


def get_context(id: int = 0) -> Context:
    """Returns the context from the specified id."""
    return _ctxs.get(id)


def reset() -> None:
    """Clears the context registry."""
    _ctxs.clear()


all = ["setup_context", "set_context", "get_context", "reset"]
