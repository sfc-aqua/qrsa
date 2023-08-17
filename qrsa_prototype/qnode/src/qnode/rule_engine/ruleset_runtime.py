from enum import Enum

from common.models.ruleset import RuleSet


class State(Enum):
    IDLE = 1
    RUNNING = 2
    TERMINATED = 3
    ERROR = 4


class RuleSetRuntime:
    def __init__(self, ruleset: RuleSet):
        self.ruleset: RuleSet = ruleset
        self.status: State = State.IDLE
