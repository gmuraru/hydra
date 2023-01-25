# stdlib
from typing import Any


class Protocol(type):
    """Keep traces of registered protocols.
    Attributes:
        registered_protocols: Dictionary with the registered protocols.
    """

    registered_protocols: dict[Any, Any] = {}

    def __new__(cls, name: str, bases, dct: dict[Any, Any]):
        """Control creation of new instances.
        Args:
            name : Name of the protocol
            bases: asdf.
            dct ): Dictionary.
        Returns:
            Protocol: Defined protocol.
        Raises:
            ValueError: if the protocol we want to register does not have a 'share_class' attribute
                        if the protocol registered does not have a 'security_levels' attribute
                        if the protocol is already registered with the same name
        """
        new_cls = super().__new__(cls, name, bases, dct)

        if getattr(new_cls, "share_class", None) is None:
            raise ValueError(
                "share_class attribute should be present in the protocol class"
            )

        if getattr(new_cls, "security_levels", None) is None:
            raise ValueError(
                "security_levels attribute should be present in the protocol class."
            )

        if name in Protocol.registered_protocols.keys():
            raise ValueError(f"{name} is already registered.")

        Protocol.registered_protocols[name] = new_cls

        return new_cls
