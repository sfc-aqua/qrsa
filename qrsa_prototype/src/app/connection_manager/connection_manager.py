from typing import Dict, Union
from ipaddress import IPv4Address, IPv6Address

from common.models.ruleset import RuleSet
from common.models.connection_setup_request import ConnectionSetupRequest
from common.models.performance_indicator import PerformanceIndicator
from connection_manager.ruleset_factory import RuleSetFactory


class ConnectionManager:
    def __init__(self):
        self.ruleset_factory = RuleSetFactory()

    async def respond_to_connection_setup_request(
        self, request: ConnectionSetupRequest
    ) -> Dict[Union[IPv4Address, IPv6Address], RuleSet]:
        print(request)
        return {"test": "test"}

    async def forward_connection_setup_request(
        self,
        given_request: ConnectionSetupRequest,
        performance_indicator: PerformanceIndicator,
        next_hop: Union[IPv4Address, IPv6Address],
    ):
        pass
