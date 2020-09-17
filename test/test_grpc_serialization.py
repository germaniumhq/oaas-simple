import unittest
from typing import Dict, Optional

import oaas
import oaas.registry

from oaas_simple.client.client import OaasGrpcTransportClient
from oaas_simple.server.server import OaasGrpcTransportServer


def service_definition_key(service_definition: oaas.registry.ServiceDefinition) -> str:
    return (
        service_definition.get("protocol", "")
        + ":"
        + service_definition.get("namespace", "")
        + ":"
        + service_definition.get("name", "")
        + ":"
        + service_definition.get("version", "")
    )


@oaas.service("oaas-registry")
class OaasRegistryService(oaas.registry.OaasRegistry):
    # FIXME: externalize into its own package? or move to core OaaS?
    def __init__(self) -> None:
        self._services: Dict[str, oaas.registry.ServiceAddress] = dict()

    def resolve_service(
        self, service_definition: oaas.registry.ServiceDefinition
    ) -> Optional[oaas.registry.ServiceAddress]:
        return self._services.get(service_definition_key(service_definition), None)

    def register_service(
        self,
        service_definition: oaas.registry.ServiceDefinition,
        service_address: oaas.registry.ServiceAddress,
    ) -> None:
        self._services[service_definition_key(service_definition)] = service_address


@oaas.service("test-service")
class TestCallService:
    def echo_data(self, *, data: str) -> str:
        return data


@oaas.client("test-service")
class TestCallClient:
    def echo_data(self, *, data: str) -> str:
        ...


oaas.register_server_provider(OaasGrpcTransportServer())
oaas.register_client_provider(OaasGrpcTransportClient())

oaas.serve()


class TestGrpcSerialization(unittest.TestCase):
    def test_serialization(self) -> None:
        client = oaas.get_client(TestCallClient)
        self.assertEqual("abc", client.echo_data(data="abc"))
