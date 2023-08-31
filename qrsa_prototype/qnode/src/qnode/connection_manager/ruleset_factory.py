from typing import Dict

from common.models import RuleSet, PerformanceIndicator
from common.type_utils import IpAddressType


class RuleSetFactory:
    """
    Factory for creating RuleSets
    """

    def __init__(self) -> None:
        pass

    def create_ruleset(
        self,
        connection_id: str,
        host_lists: IpAddressType,
        performance_indicators: Dict[IpAddressType, PerformanceIndicator],
    ) -> Dict[IpAddressType, RuleSet]:
        """
        Get performance information and create rulesets optimized for each host.
        """
        rulesets = {}

        for host in host_lists:
            # pi_for_this_host = performance_indicators[host]

            # process performance indicator here
            ruleset = RuleSet(ruleset_id=connection_id, stages=[])
            rulesets[host] = ruleset
        return rulesets
