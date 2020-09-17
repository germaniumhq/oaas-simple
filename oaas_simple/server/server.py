from concurrent import futures

import grpc
import oaas
import oaas._registrations as registrations

from oaas_simple.registry import oaas_registry
from oaas_simple.rpc import call_pb2_grpc
from oaas_simple.server.find_ips import find_ips
from oaas_simple.server.service_invoker_proxy import ServiceInvokerProxy


class OaasSimpleServer(oaas.ServerMiddleware):
    def __init__(self, *, port=8999):
        super(OaasSimpleServer, self).__init__()
        self.port = port

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
        for service_definition, _ in registrations.services.items():
            if service_definition.name == "oaas-registry":
                continue

            oaas_registry().register_service(
                {
                    "name": service_definition.name,
                    "protocol": "simple",
                },
                {
                    "port": self.port,
                    "addresses": find_ips(),
                },
            )
