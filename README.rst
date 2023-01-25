.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/hydra.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/hydra
    .. image:: https://readthedocs.org/projects/hydra/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://hydra.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/hydra/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/hydra
    .. image:: https://img.shields.io/pypi/v/hydra.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/hydra/
    .. image:: https://img.shields.io/conda/vn/conda-forge/hydra.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/hydra
    .. image:: https://pepy.tech/badge/hydra/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/hydra
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/hydra

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

=====
hydra
=====


    Secure Multi Party Computation (SMPC)l learning tool!


A longer description of your project goes here...


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.


DEVELOPMENT
===


Proto
====
1. For generating the gRPC services. It could be used also for simple objects like tensors.
   ```
   cd src
   mkdir -p hydra/proto
   python -m grpc_tools.protoc -Iproto_src --python_out=. --pyi_out=. --grpc_python_out=. proto_src/*/*/*/*.proto
   ```

   The above will generate the proto files required by the gRPC service and the protobuf schema in the folder "proto"
