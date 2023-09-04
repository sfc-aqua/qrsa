from typing import List
from ipaddress import IPv4Address, IPv6Address

from common.type_utils import IpAddressType


class RoutingDaemon:
    def __init__(self, config: dict):
        self.config = config
        # destination -> next_hop
        self.routing_table = {}
        if self.config.get("routing_daemon") is not None:
            route_config = self.config["routing_daemon"]
            if route_config["routing_type"] == "static":
                self.setup_static_route(
                    route_config["routing_table"][self.config["meta"]["hostname"]]
                )
            else:
                raise NotImplementedError("Only static routing is supported now")

    def setup_static_route(self, routing_info: dict):
        for route in routing_info:
            self.routing_table[route["destination"]] = route["next_hop"]

    def get_neighbor_nodes(self) -> List[IpAddressType]:
        neighbors = []
        for dest, next_hop in self.routing_table.items():
            # When next hop is the destination, it means this destination is neighbor
            if next_hop == dest:
                neighbors.append(dest)
        return neighbors

    def get_next_hop(self, destination: IpAddressType) -> IpAddressType:
        if isinstance(destination, IPv4Address) or isinstance(destination, IPv6Address):
            destination = str(destination)
        if self.routing_table.get(destination) is None:
            raise Exception("No route to the destination")
        else:
            return self.routing_table[destination]
