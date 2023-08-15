from typing import Dict, Union
from ipaddress import IPv4Address, IPv6Address

from common.models.ruleset import RuleSet
from common.models.connection_setup_request import ConnectionSetupRequest
from connection_manager.ruleset_factory import RuleSetFactory


class ConnectionManager:
    def __init__(self):
        self.ruleset_factory = RuleSetFactory()

    def create_ruleset(self, request: ConnectionSetupRequest) -> Dict[Union[IPv4Address, IPv6Address], RuleSet]:
        print(request)
        return {"test": "test"}
