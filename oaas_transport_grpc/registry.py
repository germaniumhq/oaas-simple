from typing import Optional

import oaas


@oaas.client("oaas-registry")
class OaasRegistry:
    def resolve_service(self, name: str) -> str:
        ...

    def register_service(self, name: str, address: str) -> None:
        ...


_oaas_registry: Optional[OaasRegistry] = None


def oaas_registry() -> OaasRegistry:
    global _oaas_registry

    if _oaas_registry:
        return _oaas_registry

    _oaas_registry = oaas.get_client(OaasRegistry)

    return _oaas_registry