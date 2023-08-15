from typing import Dict, Union
from ipaddress import IPv4Address, IPv6Address

from common.models.ruleset import RuleSet


class RuleSetFactory:
    """
    Factory for creating RuleSets
    """

    def __init__(self) -> None:
        pass

    def create_ruleset(self) -> Dict[Union[IPv4Address, IPv6Address], RuleSet]:
        rulesets = {}
        return rulesets
