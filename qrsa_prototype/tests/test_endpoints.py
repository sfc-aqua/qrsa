from typing import Any
import pytest

from common.models.application_bootstrap import ApplicationBootstrap


@pytest.mark.usefixtures("mock_rd", "mock_cm", "mock_hm")
class TestEndpoints:
    def test_heart_beat(self, test_client: Any) -> None:
        with test_client as client:
            response = client.get("/heartbeat")
            assert response.status_code == 200
            assert response.json() == {"message": "Alive"}

    @pytest.mark.asyncio
    async def test_send_connection_setup_request(
        self, test_client: Any, mocker: Any, base_app_performance_requirement: Any
    ) -> None:
        app_bootstrap = ApplicationBootstrap(
            destination="192.168.0.4",
            application_performance_requirement=base_app_performance_requirement,
        )
        with test_client as client:
            response = client.post(
                "/start_connection_setup",
                data=app_bootstrap.model_dump_json(),
                headers={"Content-Type": "application/json"},
            )
            assert response.status_code == 200
            assert response.json() == {"message": "Connection setup done"}

    def test_handle_connection_setup_request_responder(
        self,
        test_client: Any,
        mock_qrsa: Any,
        base_container_config: Any,
        base_connection_setup_request: Any,
    ) -> None:
        """
        Handle connection setup request as a responder
        """
        # Three nodes
        # 192.168.0.2 <--> 192.168.0.3 <--> 192.168.0.4
        _ = base_container_config("responder node", "192.168.0.4")
        csr = base_connection_setup_request(3, 2)  # three nodes and responder

        with test_client as client:
            response = client.post(
                "/connection_setup_request",
                data=csr.model_dump_json(),
                headers={"Content-Type": "application/json"},
            )
            assert response.status_code == 200
            assert response.json() == {"message": "Received connection setup request"}

    def test_handle_connection_setup_request_intermediate_repeater(
        self,
        test_client: Any,
        mock_qrsa: Any,
        base_container_config: Any,
        base_connection_setup_request: Any,
    ) -> None:
        """
        Handle connection setup request as an intermediate repeater
        """
        _ = base_container_config("repeater", "192.168.0.3")
        csr = base_connection_setup_request(3, 1)  # three nodes and repeater

        with test_client as client:
            response = client.post(
                "/connection_setup_request",
                data=csr.model_dump_json(),
                headers={"Content-Type": "application/json"},
            )
            assert response.status_code == 200
            assert response.json() == {"message": "Received connection setup request"}

    def test_handle_connection_setup_response(
        self,
        test_client: Any,
        mock_qrsa: Any,
        base_container_config: Any,
        base_connection_setup_response: Any,
    ) -> None:
        """
        Handle connection setup response
        """
        _ = base_container_config("initiator", "192.168.0.2")

        with test_client as client:
            response = client.post(
                "/connection_setup_response",
                data=base_connection_setup_response.model_dump_json(),
                headers={"Content-Type": "application/json"},
            )
            assert response.status_code == 200
            assert response.json() == {"message": "Received connection setup response"}

    def test_handle_link_allocation_update(
        self,
        test_client: Any,
        mock_qrsa: Any,
        base_container_config: Any,
        base_link_allocation_update: Any,
    ) -> None:
        _ = base_container_config("repeater", "192.168.0.3")

        with test_client as client:
            response = client.post(
                "/link_allocation_update",
                data=base_link_allocation_update.model_dump_json(),
                headers={"Content-Type": "application/json"},
            )
            assert response.status_code == 200
            assert response.json() == {"message": "Link Allocation Update Accepted"}

    def test_handle_barrier(
        self,
        test_client: Any,
        mock_qrsa: Any,
        base_container_config: Any,
        base_barrier: Any,
    ) -> None:
        _ = base_container_config("repeater", "192.168.0.3")

        with test_client as client:
            response = client.post(
                "/barrier",
                data=base_barrier.model_dump_json(),
                headers={"Content-Type": "application/json"},
            )
            assert response.status_code == 200
            assert response.json() == {"message": "Received barrier"}

    def test_handle_barrier_response(
            self,
            test_client: Any,
            mock_qrsa: Any,
            base_container_config: Any,
            base_barrier: Any,
    ) -> None:
        _ = base_container_config("repeater", "192.168.0.3")

        with test_client as client:
            response = client.post(
                "/barrier_response",
                data=base_barrier.model_dump_json(),
                headers={"Content-Type": "application/json"},
            )
            assert response.status_code == 200
            assert response.json() == {"message": "Received barrier response"}
