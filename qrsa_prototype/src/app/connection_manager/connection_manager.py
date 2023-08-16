from typing import Union
from ipaddress import IPv4Address, IPv6Address

from common.models.ruleset import RuleSet
from common.models.connection_setup_request import ConnectionSetupRequest
from common.models.performance_indicator import PerformanceIndicator
from .ruleset_factory import RuleSetFactory


class ConnectionManager:
    def __init__(self):
        self.ruleset_factory = RuleSetFactory()
        self.running_connection = []

    async def respond_to_connection_setup_request(
        self, request: ConnectionSetupRequest
    ) -> RuleSet:
        """
        Respond to a connection setup request.
        This function distributes RuleSets to intermediate nodes.

        """
        self.running_connection.append(request)
        print(self.running_connection)
        return {"test": "test"}

    async def forward_connection_setup_request(
        self,
        given_request: ConnectionSetupRequest,
        performance_indicator: PerformanceIndicator,
        next_hop: Union[IPv4Address, IPv6Address],
    ):
        """
        Forward a received connection setup to next hop
        """
        pass
