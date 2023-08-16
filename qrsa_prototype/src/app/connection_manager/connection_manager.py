from typing import Union
from ipaddress import IPv4Address, IPv6Address

from common.models.ruleset import RuleSet
from common.models.connection_setup_request import ConnectionSetupRequest
from common.models.performance_indicator import PerformanceIndicator
from .ruleset_factory import RuleSetFactory


class ConnectionManager:
    def __init__(self):
        self.ruleset_factory = RuleSetFactory()
        # application id -> connection id
        self.running_connection = {}

    async def respond_to_connection_setup_request(
        self, request: ConnectionSetupRequest
    ) -> RuleSet:
        """
        Respond to a connection setup request.
        This function distributes RuleSets to intermediate nodes.

        """
        # Connection id is filled when the connection setup response is received
        self.running_connection[request.application_id] = None
        print(self.running_connection)
        return {"test": "test"}

    def link_connection_id_to_application_id(self,
                                             application_id: str,
                                             connection_id: str):
        if application_id not in self.running_connection:
            raise ValueError(f"Application id {application_id} not found")
        self.running_connection[application_id] = connection_id

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
