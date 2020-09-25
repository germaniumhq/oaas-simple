from typing import Optional

import oaas
from oaas_grpc.server import OaasGrpcServer
from oaas_grpc.server.find_ips import find_ips
from oaas_registry_api import OaasRegistryStub
from oaas_registry_api.rpc.registry_pb2 import OaasServiceDefinition

from oaas_simple.server.service_invoker_proxy import noop

noop()


class OaasSimpleServer(oaas.ServerMiddleware):
    def __init__(self, *, port=8999):
        super(OaasSimpleServer, self).__init__()

        self.port = port
        self._grpc_server: Optional[OaasGrpcServer] = None

    def serve(self) -> None:
        locations = find_ips(port=self.port)

        # we ensure we're serving with the gRPC server first
        self._oaas_grpc_server.serve()

        # we can get the registry only after the server is servicing
        # in case this _is_ the registry.
        registry = oaas.get_client(OaasRegistryStub)

        # we register the services
        for service_definition in oaas.registrations.services:
            if not self.can_serve(service_definition=service_definition):
                continue

            print(
                f"Added SIMPLE service: {service_definition.gav} as {service_definition.code}"
            )

            registry.register_service(
                OaasServiceDefinition(
                    namespace=service_definition.namespace,
                    name=service_definition.name,
                    version=service_definition.version,
                    tags={
                        "_protocol": "simple",
                    },
                    locations=locations,
                )
            )

    def join(self) -> None:
        self._oaas_grpc_server.join()

    def can_serve(self, service_definition: oaas.ServiceDefinition) -> bool:
        return not hasattr(service_definition.code, "add_to_server")

    @property
    def _oaas_grpc_server(self) -> OaasGrpcServer:
        """
        The simple server is a single service on top of gRPC. This will
        check if there's another server already registered and use it
        first. If there isn't any, it will create one.
        """
        if self._grpc_server:
            return self._grpc_server

        # search in the registration for a gRPC server with the same port
        # as the simple service
        for server in oaas.registrations.servers_middleware:
            if isinstance(server, OaasGrpcServer) and server.port == self.port:
                self._grpc_server = server
                return self._grpc_server

        self._grpc_server = OaasGrpcServer(port=self.port)
        return self._grpc_server
