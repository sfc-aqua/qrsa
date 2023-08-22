import pytest
from typing import List
from fastapi.testclient import TestClient

from qnode import server
from common.models.connection_setup_request import ConnectionSetupRequest
from common.models.app_performance_requirement import ApplicationPerformanceRequirement
from common.models.header import Header
from common.models.performance_indicator import PerformanceIndicator


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
    def _gen_connection_setup_request(
        size: int, position: int = 0, is_responder: bool = False
    ):
        """
        Generate a connection setup request
        size: The number of hosts in the network
        position: The position of this node in the network (initiator is 0)
        """
        if is_responder:
            # responder node add its own performance indicator
            # when they create a ruleset
            host_list = base_hosts(size)[:position]
        else:
            host_list = base_hosts(size)[: position + 1]
        performance_indicators = {
            i: j for i, j in zip(host_list, base_performance_indicators(position))
        }

        # The first record of host should correspond to the source
        # and the last record should correspond to the destination
        header = Header(src=host_list[0], dst=base_hosts(size)[-1])

        csr = ConnectionSetupRequest(
            header=header,
            application_id="test_app_id",
            app_performance_requirement=base_app_performance_requirement,
            performance_indicators=performance_indicators,
            host_list=host_list,
        )
        return csr

    return _gen_connection_setup_request
