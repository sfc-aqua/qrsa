import pytest
from typing import List, Any
from fastapi.testclient import TestClient

from qnode import server
from qnode.real_time_controller.real_time_controller import RealtimeController
from qnode.containers import Container

from common.models.connection_setup_request import ConnectionSetupRequest
from common.models.connection_setup_response import ConnectionSetupResponse
from common.models.app_performance_requirement import ApplicationPerformanceRequirement
from common.models.header import Header
from common.models.performance_indicator import PerformanceIndicator
from common.models.ruleset import RuleSet


@pytest.fixture
def test_client():
    app = server.create_server()
    return TestClient(app)


@pytest.fixture
def base_header() -> Header:
    return Header(src="192.168.0.2", dst="192.168.0.3")


@pytest.fixture
def base_app_performance_requirement() -> ApplicationPerformanceRequirement:
    """
    performance requirement scheme could change
    frequently so that this function generate
    latest app performace requirements
    """
    return ApplicationPerformanceRequirement(
        minimum_fidelity=0.9, minimum_bell_pair_bandwidth=100
    )


@pytest.fixture
def base_performance_indicators() -> List[PerformanceIndicator]:
    def _gen_performance_indicator(size: int):
        return [
            PerformanceIndicator(
                local_op_fidelity=0.9,
            )
            for _ in range(size)
        ]

    return _gen_performance_indicator


@pytest.fixture
def base_hosts() -> List[str]:
    def _gen_hosts(size: int):
        if size > 253:
            raise ValueError("Too many hosts")
        return [f"192.168.0.{i+2}" for i in range(size)]

    return _gen_hosts


@pytest.fixture
def base_connection_setup_request(
    base_header,
    base_app_performance_requirement,
    base_hosts,
    base_performance_indicators,
) -> ConnectionSetupRequest:
    def _gen_connection_setup_request(size: int, position: int = 0):
        """
        Generate a connection setup request
        size: The number of hosts in the network
        position: The position of this node in the network (initiator is 0)
        """
        host_list = base_hosts(size)[:position]
        performance_indicators = {
            i: j for i, j in zip(host_list, base_performance_indicators(position))
        }

        # The first record of host should correspond to the source
        # and the last record should correspond to the destination
        header = Header(src=base_hosts(size)[0], dst=base_hosts(size)[-1])

        csr = ConnectionSetupRequest(
            header=header,
            application_id="application_id",
            app_performance_requirement=base_app_performance_requirement,
            performance_indicators=performance_indicators,
            host_list=host_list,
        )
        return csr

    return _gen_connection_setup_request


@pytest.fixture
def base_connection_setup_response(
    base_header, base_app_performance_requirement, base_rulesets
) -> ConnectionSetupResponse:
    def _gen_connection_setup_response(
        src: str = "192.168.0.2", dst: str = "192.168.0.4"
    ):
        """
        Generate a connection setup response
        """
        return ConnectionSetupResponse(
            header=Header(src=src, dst=dst),
            application_id="application_id",
            connection_id="connection_id",
            ruleset=RuleSet(ruleset_id="ruleset_id", stages=[]),
        )

    return _gen_connection_setup_response


@pytest.fixture
def base_rulesets(mocker: Any, base_hosts: Any) -> List[RuleSet]:
    def _gen_rulesets(size: int, ruleset_id: str = "ruleset_id"):
        return {
            host: RuleSet(ruleset_id=ruleset_id, stages=[]) for host in base_hosts(size)
        }

    return _gen_rulesets


@pytest.fixture
def base_container_config():
    def _create_container(
        host_name: str = "test node", ip_address: str = "192.168.0.2"
    ):
        container = Container()
        container.config.from_dict(
            {"meta": {"hostname": host_name, "ip_address": ip_address}}
        )
        return container

    return _create_container


@pytest.fixture
def mock_rtc(mocker: Any):
    """
    Mock RealtimeController that patches rtc functions and return dummy rtc object.
    """
    mocker.patch(
        "qnode.real_time_controller.real_time_controller.RealtimeController.start_link_entanglement_generation"  # noqa
    )
    mocker.patch(
        "qnode.real_time_controller.real_time_controller.RealtimeController.stop_link_entanglement_generation"  # noqa
    )
    mocker.patch(
        "qnode.real_time_controller.real_time_controller.RealtimeController.fetch_link_entanglement"  # noqa
    )

    return RealtimeController()


@pytest.fixture
def mock_hm(mocker: Any, base_performance_indicators: Any) -> None:
    """
    Mock HardwareMonitor that patches hm functions.
    """
    mocker.patch(
        "qnode.hardware_monitor.hardware_monitor.HardwareMonitor.get_performance_indicator",  # noqa
        return_value=base_performance_indicators(1)[0],
    )


@pytest.fixture
def mock_cm(mocker: Any) -> None:
    """
    Mock ConnectionManager that patches cm functions.
    """
    mocker.patch(
        "qnode.connection_manager.connection_manager.ConnectionManager.send_connection_setup_request",  # noqa
        return_value=(None, 200),
    )
    mocker.patch(
        "qnode.connection_manager.connection_manager.ConnectionManager.respond_to_connection_setup_request",  # noqa
        return_value=(None, 200),
    )
    mocker.patch(
        "qnode.connection_manager.connection_manager.ConnectionManager.forward_connection_setup_request",  # noqa
        return_value=(None, 200),
    )
    mocker.patch(
        "qnode.connection_manager.connection_manager.ConnectionManager.update_pending_connection_to_running_connection",  # noqa
    )
    mocker.patch(
        "qnode.connection_manager.connection_manager.ConnectionManager.send_link_allocation_update",  # noqa
        return_value=(None, 200),
    )
    mocker.patch(
        "qnode.connection_manager.connection_manager.ConnectionManager.send_barrier",  # noqa
    )
    mocker.patch(
        "qnode.connection_manager.connection_manager.ConnectionManager.send_barrier_response",  # noqa
    )
    mocker.patch(
        "qnode.connection_manager.connection_manager.ConnectionManager.send_message",  # noqa
    )


@pytest.fixture
def mock_rd(mocker: Any) -> None:
    """
    Mock RoutingDaemon that patches rd functions.
    """
    mocker.patch(
        "qnode.routing_daemon.routing_daemon.RoutingDaemon.get_next_hop",
        return_value="192.168.0.3",
    )
    mocker.patch(
        "qnode.routing_daemon.routing_daemon.RoutingDaemon.get_neighbor_nodes",
        return_value=["192.168.0.5", "192.168.0.6"],
    )


@pytest.fixture
def mock_re(mocker: Any) -> None:
    """
    Mock RuleEngine that patches re functions.
    """
    mocker.patch(
        "qnode.rule_engine.rule_engine.RuleEngine.accept_ruleset",
        return_value=("connection_id", RuleSet(ruleset_id="ruleset_id", stages=[])),
    )
    mocker.patch(
        "qnode.rule_engine.rule_engine.RuleEngine.get_pptsns_with_buffer",
        return_value=10,
    )
    mocker.patch(
        "qnode.rule_engine.rule_engine.RuleEngine.get_switching_pptsns",
        return_value={"192.168.0.2": 10},
    )


@pytest.fixture
def mock_qrsa(mock_cm: Any, mock_hm: Any, mock_rd: Any, mock_re: Any) -> None:
    """
    integrate qrsa mocks
    """
    pass
