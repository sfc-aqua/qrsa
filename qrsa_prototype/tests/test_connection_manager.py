import pytest
from typing import Any
from qnode.connection_manager.connection_manager import ConnectionManager


@pytest.fixture
def init_connection_manager() -> Any:
    def _inject_config(config: dict = None) -> ConnectionManager:
        if config is None:
            # default configuration
            config = {"meta": {"hostname": "test", "ip_address": "192.168.0.2"}}
        return ConnectionManager(config)

    return _inject_config


class TestConnectionManager:
    @pytest.fixture
    def shared_mock(self, mocker: Any) -> None:
        mocker.patch(
            "qnode.connection_manager.connection_manager.ConnectionManager.send_message",  # noqa
            return_value=(None, 200),
        )

    @pytest.mark.asyncio
    async def test_send_connection_setup_request(
        self,
        init_connection_manager: Any,
        mocker: Any,
        shared_mock: Any,
        base_app_performance_requirement: Any,
        base_performance_indicators: Any,
    ) -> None:
        """
        Send connection setup request to neighbor node
        """
        # This node must be an initiator to send a connection setup request
        cm = init_connection_manager()
        mocker.patch("uuid.uuid4", return_value="application_id")
        # This test won't send message but track the states
        destination = "192.168.0.4"
        next_hop = "192.168.0.3"
        performance_indicator = base_performance_indicators(1)[0]
        await cm.send_connection_setup_request(
            destination,
            next_hop,
            base_app_performance_requirement,
            performance_indicator,
        )
        assert len(cm.running_connections) == 0
        assert len(cm.pending_connections) == 1
        assert cm.pending_connections.get("application_id") is not None
        assert cm.pending_connections.get("application_id").next_hop == next_hop
        assert cm.pending_connections.get("application_id").prev_hop is None
        assert cm.pending_connections.get("application_id").source == "192.168.0.2"
        assert cm.pending_connections.get("application_id").destination == destination

    @pytest.mark.asyncio
    async def test_respond_to_connection_setup_request(
        self,
        init_connection_manager: Any,
        mocker: Any,
        shared_mock: Any,
        base_rulesets: Any,
        base_connection_setup_request: Any,
    ) -> None:
        """
        Test ruleset is properly generated and send connection setup resuponse
        """
        # There are three nodes in this network
        # (0)192.168.0.2, (1)192.168.0.3, (2)192.168.0.4 (this node)
        csr = base_connection_setup_request(3, 2, True)  # 3 hosts, at 2 as responder
        responder_performance_indicator = csr.performance_indicators[csr.header.src]
        cm = init_connection_manager({"meta": {"ip_address": "192.168.0.4"}})

        mocker.patch("uuid.uuid4", return_value="connection_id")
        mocker.patch(
            "qnode.connection_manager.ruleset_factory.RuleSetFactory.create_ruleset",  # noqa
            return_value=base_rulesets(3, "connection_id"),
        )

        connection_id, ruleset = await cm.respond_to_connection_setup_request(
            csr, responder_performance_indicator
        )
        # current running connection must be 1
        assert len(cm.running_connections) == 1
        assert cm.running_connections["connection_id"].prev_hop == "192.168.0.3"
        assert cm.running_connections["connection_id"].next_hop is None
        assert cm.running_connections["connection_id"].source == "192.168.0.2"
        assert cm.running_connections["connection_id"].destination == "192.168.0.4"

        assert connection_id == "connection_id"
        assert ruleset.ruleset_id == "connection_id"
        assert ruleset.stages == []

    @pytest.mark.asyncio
    async def test_forward_connection_setup_request(
        self,
        init_connection_manager: Any,
        mocker: Any,
        shared_mock: Any,
        base_connection_setup_request: Any,
        base_performance_indicators: Any,
    ) -> None:
        """
        Test connection setup request is forwarded to the next hop
        """
        # Situation
        # Three nodes in the network
        # (0)192.168.0.2, (1)192.168.0.3, (2)192.168.0.4 (this node)
        # This not is (1) and get request from (0) and forward it to (2)
        csr = base_connection_setup_request(3, 1, False)  # 3 hosts, at 1
        cm = init_connection_manager(
            {"meta": {"hostname": "test(1)", "ip_address": "192.168.0.3"}}
        )
        performance_indictor = base_performance_indicators(1)[0]
        next_hop = "192.168.0.4"
        await cm.forward_connection_setup_request(csr, performance_indictor, next_hop)
        assert len(cm.pending_connections) == 1
        assert cm.pending_connections.get("application_id").next_hop == next_hop
        assert cm.pending_connections.get("application_id").prev_hop == "192.168.0.2"
        assert cm.pending_connections.get("application_id").source == "192.168.0.2"
        assert cm.pending_connections.get("application_id").destination == "192.168.0.4"
