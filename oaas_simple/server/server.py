from concurrent import futures

import grpc
import oaas
import oaas._registrations as registrations

from oaas_simple.registry import oaas_registry
from oaas_simple.rpc import call_pb2_grpc
from oaas_simple.server.find_ips import find_ips
from oaas_simple.server.service_invoker_proxy import ServiceInvokerProxy


class OaasGrpcTransportServer(oaas.ServerMiddleware):
    def __init__(self):
        super(OaasGrpcTransportServer, self).__init__()
        self.port = 8999  # FIXME: detect/set the port

    def serve(self) -> None:
        self.server = self.start_server()
        self.register_services_into_registry()

    def join(self) -> None:
        self.server.wait_for_termination()

    def start_server(self):
        server_address: str = f"[::]:{self.port}"
        server = grpc.server(futures.ThreadPoolExecutor())
        call_pb2_grpc.add_ServiceInvokerServicer_to_server(
            ServiceInvokerProxy(), server
        )
        port = server.add_insecure_port(server_address)
        server.start()
        return server

    def register_services_into_registry(self):
        registry = oaas_registry()

        for service_definition, _ in registrations.services.items():
            registry.register_service(
                {
                    "name": service_definition.name,
                    "protocol": "simple",
                },
                {
                    "port": self.port,
                    "addresses": find_ips(),
                },
            )
