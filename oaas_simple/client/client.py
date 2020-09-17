from typing import Any, Dict

import grpc
import oaas
import socket
import random

from oaas import ClientDefinition
from oaas.registry import ServiceAddress

from oaas_simple.client import registry_discovery
from oaas_simple.client.service_client_proxy import ServiceClientProxy
from oaas_simple.registry import oaas_registry


def is_port_open(host_address: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as a_socket:
        location = (host_address, port)
        result_of_check = a_socket.connect_ex(location)

        return result_of_check == 0


class OaasGrpcTransportClient(oaas.ClientMiddleware):
    def __init__(self) -> None:
        self._client_to_address: Dict[str, str] = dict()
        self._channels: Dict[str, Any] = dict()

    def create_client(self, cd: ClientDefinition) -> Any:
        if cd.name == "oaas-registry":
            service_address = registry_discovery.find_registry()
        else:
            service_address = oaas_registry().resolve_service(
                {
                    "name": cd.name,
                    "protocol": "simple",
                    "namespace": "",
                    "version": "",
                }
            )

        address = self._client_to_address.get(cd.name, None)

        if address:
            return self._channels[address]

        channel = self.create_channel(cd, service_address)

        return ServiceClientProxy(client_definition=cd, channel=channel)

    def create_channel(self, cd: ClientDefinition, service_address: ServiceAddress):
        port = service_address["port"]
        addresses = service_address["addresses"]
        random.shuffle(addresses)

        for host_address in addresses:
            address = f"{host_address}:{port}"

            # if we already have a channel for this address, we don't need
            # to check if the port is open, and establish the connection,
            # but simply reuse the same channel.
            if address in self._channels:
                self._client_to_address[cd.name] = address
                return self._channels[address]

            if not is_port_open(host_address, port):
                continue

            channel = grpc.insecure_channel(address)
            self._channels[address] = channel
            self._client_to_address[cd.name] = address

            return channel

        raise Exception(
            f"Unable to find port {port} open on any of "
            f"the {service_address['addresses']}"
        )

    def can_handle(self, cd: ClientDefinition) -> bool:
        # FIXME: should at least check the registered types
        return True
