import os
import re

from oaas.registry import ServiceAddress

IP_PORT_ADDRESS = re.compile("^(.+)(:\d+)?$")


def find_registry() -> ServiceAddress:
    if "OAAS_REGISTRY" in os.environ:
        return read_oaas_registry_from_environ()

    return create_static_search_list()


def read_oaas_registry_from_environ() -> ServiceAddress:
    oaas_registry = os.environ["OAAS_REGISTRY"]
    m = IP_PORT_ADDRESS.match(oaas_registry)

    if not m:
        raise Exception(
            f"Unable to parse OAAS_REGISTRY " f"environment variable: {oaas_registry}"
        )

    return {"port": int(m.group(2)), "addresses": [m.group(1)]}


def create_static_search_list() -> ServiceAddress:
    return {
        "port": 8999,
        "addresses": [
            "localhost",
            # docker
            "172.17.0.1",
            # kubernetes
            "oaas-registry",
            "oaas-registry.oaas-registry.svc.cluster.local",
        ],
    }
