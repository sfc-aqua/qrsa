import pytest
from typing import Any

from qnode.rule_engine import RuleEngine


@pytest.fixture
def init_rule_engine(mock_rtc: Any) -> Any:
    def _inject_config(config: dict = None) -> RuleEngine:
        if config is None:
            # default configuration
            pass
        return RuleEngine(config, mock_rtc)

    return _inject_config
