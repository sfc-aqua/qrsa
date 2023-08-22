import pytest
from typing import Any
from qnode.connection_manager.connection_manager import ConnectionManager


@pytest.fixture
def init_connection_manager() -> Any:
    def _inject_config(config: dict = None) -> ConnectionManager:
        if config is None:
            # default configuration
            config = {"ip_address": "192.168.0.2"}
        return ConnectionManager(config)

    return _inject_config


class TestConnectionManager:
    @pytest.mark.asyncio
    async def test_respond_to_connection_setup_request(
        self,
        init_connection_manager: Any,
        mocker: Any,
        base_connection_setup_request: Any,
    ) -> None:
        """
        Test ruleset is properly generated.
        """
        # There are three nodes in this network
        # (0)192.168.0.2, (1)192.168.0.3, (2)192.168.0.4 (this node)
        csr = base_connection_setup_request(3, 2, True)  # 3 hosts, at 2 as responder
        responder_performance_indicator = csr.performance_indicators[csr.header.src]
        cm = init_connection_manager({"ip_address": "192.168.0.4"})

        mocker.patch("uuid.uuid4", return_value="connection_id")
        mocker.patch(
            "qnode.connection_manager.connection_manager.ConnectionManager.send_message",
            return_value={},
        )
        ruleset = await cm.respond_to_connection_setup_request(
            csr, responder_performance_indicator
        )
        # current running connection must be 1
        assert len(cm.running_connections) == 1
        assert cm.running_connections["connection_id"].prev_hop == "192.168.0.3"
        assert cm.running_connections["connection_id"].next_hop is None
        assert cm.running_connections["connection_id"].source == "192.168.0.2"
        assert cm.running_connections["connection_id"].destination == "192.168.0.4"

        assert ruleset.ruleset_id == "connection_id"
        assert ruleset.stages == []

    # @pytest.mark.asyncio
    # async def test_forward_connection_setup_request():
    #     pass
