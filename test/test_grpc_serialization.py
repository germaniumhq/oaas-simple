

import unittest

import oaas

from oaas_transport_grpc.client.client import OaasGrpcTransportClient
from oaas_transport_grpc.server.server import OaasGrpcTransportServer


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
