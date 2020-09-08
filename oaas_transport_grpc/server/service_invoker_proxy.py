from typing import Any, Dict

import oaas._registrations as registrations

from oaas_transport_grpc.data import from_data, create_data
from oaas_transport_grpc.rpc import call_pb2
from oaas_transport_grpc.rpc import call_pb2_grpc


class ServiceInvokerProxy(call_pb2_grpc.ServiceInvokerServicer):
    def __init__(self) -> None:
        self._service_instances: Dict[str, Any] = dict()

        # we keep a live instance of the service
        for service_definition in registrations.services:
            self._service_instances[service_definition.name] = service_definition.code()

    """
    Invokes the service on this server.
    """
    def InvokeMethod(self, request: call_pb2.ServiceCall, context) -> call_pb2.Data:
        service_instance = self._service_instances[request.service]

        service_method = getattr(service_instance, request.method)

        args = []
        kw = {}

        for param in request.parameters:
            value = from_data(param.data)

            if param.name:
                kw[param.name] = value
            else:
                args.append(value)

        result = service_method(*args, **kw)

        return create_data(result)
