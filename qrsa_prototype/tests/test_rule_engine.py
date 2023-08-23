import pytest
from typing import Any

from qnode.rule_engine.rule_engine import RuleEngine


@pytest.fixture
def init_rule_engine(mock_rtc: Any) -> Any:
    def _inject_config(config: dict = None) -> RuleEngine:
        if config is None:
            # default configuration
            pass
        return RuleEngine(config, mock_rtc)

    return _inject_config


class TestRuleEngine:
    def test_accept_resource(self, init_rule_engine: Any) -> None:
        rule_engine = init_rule_engine()
        assert rule_engine.available_link_resource.empty()
        rule_engine.accept_resource("dummy")
        assert not rule_engine.available_link_resource.empty()
        assert rule_engine.get_available_link_resource() == "dummy"

    def test_accept_ruleset(self, init_rule_engine: Any) -> None:
        rule_engine = init_rule_engine()
        assert rule_engine.available_link_resource.empty()
        rule_engine.accept_resource("dummy")
        assert not rule_engine.available_link_resource.empty()
        assert rule_engine.get_available_link_resource() == "dummy"
