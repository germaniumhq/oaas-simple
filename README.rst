A transport for OaaS that uses a single ``grpc`` function. It should
work out of the box for most simple scenarios.

Installation
============

.. code:: sh

    pip install oaas_simple

Usage
=====

To get a process that does both the client and the server:

.. code:: python

    oaas.register_server_provider(OaasGrpcTransportServer(port=9000))
    oaas.register_client_provider(OaasGrpcTransportClient())

    oaas.serve()

Exposing services is done via regular ``oaas`` decorators:

.. code:: python

    @oaas.service("test-service")
    class TestCallService:
        def echo_data(self, *, data: str) -> str:
            return data

Again for consumers:

.. code:: python

    @oaas.client("test-service")
    class TestCallClient:
        def echo_data(self, *, data: str) -> str:
            ...

In order to make the services find each other you need a registry. You
can fire up the embedded registry:

.. code:: sh

    python -m oaas_simple.registry

The only requirement is that the registry listens on port 8999

Minimal Client
==============

.. code:: python

    import oaas
    import oaas_simple


    @oaas.client("swag")
    class Swag:
        def print_stuff(message: str) -> str:
            ...


    oaas.register_client_provider(oaas_simple.OaasSimpleClient())


    swag = oaas.get_client(Swag)

    print(swag.print_stuff("abc"))

Minimal Server
==============

.. code:: python

    import oaas
    import oaas_simple


    @oaas.service("swag")
    class Swag:
        def print_stuff(self, message: str) -> str:
            print(message)
            return f"from server {message}"

    # it needs the client to find the registry, since the registry is also an
    # oaas.service("oaas-registry")
    oaas.register_client_provider(oaas_simple.OaasSimpleClient())
    oaas.register_server_provider(oaas_simple.OaasSimpleServer(port=9000))

    oaas.serve()
    oaas.join()
