from concurrent import futures
from typing import Dict, Any, Set, Optional

import grpc
import oaas
import oaas._registrations as registrations
from oaas import ClientDefinition

from oaas_transport_grpc.registry import OaasRegistry
from oaas_transport_grpc.rpc import call_pb2_grpc, call_pb2
from oaas_transport_grpc.rpc.call_pb2_grpc import ServiceInvokerStub


@oaas.service("oaas-registry")
class OaasRegistryService:
    def __init__(self) -> None:
        self._services: Dict[str, str] = dict()

    def resolve_service(self, name: str) -> str:
        return self._services.get(name, None)

    def register_service(self, name: str, address: str) -> None:
        self._services[name] = address


class OaasTransportGrpc(call_pb2_grpc.ServiceInvokerServicer):
    """
    The server router
    """
    def InvokeMethod(self,
                     request: call_pb2.ServiceCall,
                     context) -> call_pb2.Data:
        return call_pb2.Data(s="abc")


class OaasTransportGrpcClientProxy:
    def __init__(self,
                 grpc_service_invoker_stub: ServiceInvokerStub) -> None:
        self._grpc_service_invoker_stub = grpc_service_invoker_stub


class OaasGrpcSerializer(oaas.SerializationProvider):
    def __init__(self) -> None:
        self._channels: Dict[str, Any] = dict()
        self._channel_to_service: Dict[str, Set[ServiceInvokerStub]] = dict()

        self._oaas_registry: Optional[OaasRegistry] = None

    def serve(self) -> None:
        server_address: str = '[::]:8999'
        server = grpc.server(futures.ThreadPoolExecutor())
        call_pb2_grpc.add_ServiceInvokerServicer_to_server(OaasTransportGrpc(), server)
        port = server.add_insecure_port(server_address)

        server.start()

        self_address = self._find_self_address()
        for service_definition, _ in registrations.services:
            self.oaas_registry.register_service(service_definition.name, self_address)

        server.wait_for_termination()

    def create_client(self, cd: ClientDefinition) -> Any:
        if cd.name == "oaas-registry":
            service_address = 'localhost:8999'
        else:
            service_address = self.oaas_registry.resolve_service(cd.name)

        channel = self._channels.get(service_address, None)

        if not channel:
            channel = grpc.insecure_channel('localhost:8999')
            self._channels[service_address] = channel
            self._channel_to_service[service_address] = set()



    def can_handle(self, cd: ClientDefinition) -> bool:
        # FIXME: should at least check the registered types
        return True

    @property
    def oaas_registry(self) -> OaasRegistry:
        if self._oaas_registry:
            return self._oaas_registry

        self._oaas_registry = oaas.get_client(OaasRegistry)

        return self._oaas_registry

    def _find_self_address(self) -> str:
        # FIXME: solve decently.
        return "localhost:8999"
