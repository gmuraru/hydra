"""This package represents some top level SMPC functionalities.

For the moment it has some basic functionality, but more would
come in the following weeks.
"""

# stdlib
from importlib.metadata import PackageNotFoundError  # pragma: no cover
from importlib.metadata import version
import logging

logging.basicConfig(level=logging.INFO)

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
