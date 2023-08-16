from typing import Dict
from common.models.ruleset import RuleSet

from rule_engine.ruleset_runtime import RuleSetRuntime


class RuleEngine:
    def __init__(self):
        # connection_id -> ruleset_runtime
        self.running_runtime: Dict[str, RuleSetRuntime] = {}

    def accept_ruleset(self, connection_id: str, ruleset: RuleSet):
        # TODO: implement policy and pptsn relationship

        # Initialize runtime
        runtime = RuleSetRuntime(ruleset)
        self.running_runtime[connection_id] = runtime
