from typing import List

import netifaces
import oaas.registry


def find_ips() -> List[oaas.registry.IpLink]:
    result: List[oaas.registry.IpLink] = []

    for interface in netifaces.interfaces():
        ifaddresses = netifaces.ifaddresses(interface)

        if netifaces.AF_INET not in ifaddresses:
            continue

        for link in ifaddresses[netifaces.AF_INET]:
            result.append(link['addr'])

    return result
