from typing import Any, Dict, Callable

from oaas import ClientDefinition

from oaas_transport_grpc.client.single_method import SingleMethod
from oaas_transport_grpc.rpc import call_pb2_grpc, call_pb2


class ServiceClientProxy:
    """
    Makes it so any call invoked on it, is being forwarded
    to the service.
    """
    def __init__(self,
                 *,
                 client_definition: ClientDefinition,
                 channel: Any) -> None:
        self._methods: Dict[str, Callable] = dict()
        self.client_definition = client_definition

        self.stub = call_pb2_grpc.ServiceInvokerStub(channel)

    def __getattr__(self, method_name: str):
        result = self._methods.get(method_name, None)

        if result:
            return result

        invoker = SingleMethod(
            stub=self.stub,
            client_definition=self.client_definition,
            method_name=method_name,
        )

        self._methods[method_name] = invoker

        return invoker