from typing import Union
from ipaddress import IPv4Address, IPv6Address


class RoutingDaemon:
    def __init__(self):
        pass

    def get_next_hop(
        self,
        destination: Union[IPv4Address, IPv6Address]
    ) -> Union[IPv4Address, IPv6Address]:
        pass
