import time
from concurrent import futures

import grpc
import oaas
import oaas._registrations as registrations

from oaas_transport_grpc.registry import oaas_registry
from oaas_transport_grpc.rpc import call_pb2_grpc
from oaas_transport_grpc.server.service_invoker_proxy import ServiceInvokerProxy


class OaasGrpcTransportServer(oaas.ServerMiddleware):
    def serve(self) -> None:
        server = self.start_server()
        self.register_services_into_registry()

        server.wait_for_termination()

    def start_server(self):
        server_address: str = '[::]:8999'
        server = grpc.server(futures.ThreadPoolExecutor())
        call_pb2_grpc.add_ServiceInvokerServicer_to_server(ServiceInvokerProxy(), server)
        port = server.add_insecure_port(server_address)
        server.start()
        return server

    def register_services_into_registry(self):
        self_address = self._find_self_address()
        registry = oaas_registry()

        for service_definition, _ in registrations.services.items():
            registry.register_service(service_definition.name, self_address)

    def _find_self_address(self):
        # FIXME: implement
        return "localhost:8999"
