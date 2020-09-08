import unittest
from typing import Dict

import oaas

from oaas_transport_grpc.client.client import OaasGrpcTransportClient
from oaas_transport_grpc.server.server import OaasGrpcTransportServer


@oaas.service("oaas-registry")
class OaasRegistryService:
    def __init__(self) -> None:
        self._services: Dict[str, str] = dict()

    def resolve_service(self, name: str) -> str:
        return self._services.get(name, None)

    def register_service(self, name: str, address: str) -> None:
        self._services[name] = address


@oaas.service("test-service")
class TestCallService:
    def echo_data(self, *, data: str) -> str:
        return data


@oaas.client("test-service")
class TestCallClient:
    def echo_data(self, *, data: str) -> str:
        ...


oaas.register_server_provider(OaasGrpcTransportServer())
oaas._registrations.clients_middleware.add(OaasGrpcTransportClient())

oaas.serve()


class TestGrpcSerialization(unittest.TestCase):
    def test_serialization(self):
        client = oaas.get_client(TestCallClient)
        self.assertEqual("abc", client.echo_data(data="abc"))
        print("test succeeded")
