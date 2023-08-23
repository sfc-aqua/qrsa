from typing import Union
from ipaddress import IPv4Address, IPv6Address


class RoutingDaemon:
    def __init__(self, config: dict):
        self.config = config
        # destination -> next_hop
        self.routing_table = {}
        if self.config.get("routing_daemon").get("routing_type") == "static":
            self.setup_static_route(
                self.config.get("routing_daemon")
                .get("routing_table")
                .get(self.config["meta"]["hostname"])
            )
        else:
            raise NotImplementedError("Only static routing is supported now")

    def setup_static_route(self, routing_info: dict):
        for route in routing_info:
            self.routing_table[route["destination"]] = route["next_hop"]

    def get_next_hop(
        self, destination: Union[IPv4Address, IPv6Address]
    ) -> Union[IPv4Address, IPv6Address]:
        pass
