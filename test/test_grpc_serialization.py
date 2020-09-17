import unittest

import oaas
import oaas.registry

from oaas_simple.client.client import OaasSimpleClient
from oaas_simple.server.server import OaasSimpleServer


@oaas.service("test-service")
class TestCallService:
    def echo_data(self, *, data: str) -> str:
        return data


@oaas.client("test-service")
class TestCallClient:
    def echo_data(self, *, data: str) -> str:
        ...


oaas.register_server_provider(OaasSimpleServer())
oaas.register_client_provider(OaasSimpleClient())

oaas.serve()


class TestGrpcSerialization(unittest.TestCase):
    def test_serialization(self) -> None:
        client = oaas.get_client(TestCallClient)
        self.assertEqual("abc", client.echo_data(data="abc"))
