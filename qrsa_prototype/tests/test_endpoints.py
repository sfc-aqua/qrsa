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
        self,
        test_client: Any,
        mocker: Any,
        base_app_performance_requirement: Any
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

    def test_handle_connection_setup_request(
        self, test_client: Any, base_connection_setup_request: Any
    ) -> None:
        with test_client as client:
            response = client.post(
                "/start_connection_setup",
                data=base_connection_setup_request(2, 0).model_dump_json(),
                headers={"Content-Type": "application/json"},
            )
            assert response.status_code == 200
            assert response.json() == {"message": "Received connection setup request"}
