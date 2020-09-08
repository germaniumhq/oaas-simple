from typing import Any, Dict

import grpc
import oaas
from oaas import ClientDefinition

from oaas_transport_grpc.client.service_client_proxy import ServiceClientProxy
from oaas_transport_grpc.registry import oaas_registry


class OaasGrpcTransportClient(oaas.ClientMiddleware):
    def __init__(self) -> None:
        self._channels: Dict[str, Any] = dict()

    def create_client(self, cd: ClientDefinition) -> Any:
        if cd.name == "oaas-registry":
            service_address = 'localhost:8999'
        else:
            service_address = oaas_registry().resolve_service(cd.name)

        channel = self._channels.get(service_address, None)

        if not channel:
            channel = grpc.insecure_channel(service_address)
            self._channels[service_address] = channel

        channel = self._channels[service_address]

        return ServiceClientProxy(client_definition=cd,
                                  channel=channel)

    def can_handle(self, cd: ClientDefinition) -> bool:
        # FIXME: should at least check the registered types
        return True
