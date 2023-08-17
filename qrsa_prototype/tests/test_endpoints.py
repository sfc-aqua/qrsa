from typing import Any
from common.models.connection_setup_request import ConnectionSetupRequest


class TestEndpoints:
    def test_heart_beat(self, test_client: Any) -> None:
        response = test_client.get("/heartbeat")
        assert response.status_code == 200
        assert response.json() == {"message": "Alive"}

    def test_handle_connection_setup_request(self, test_client: Any) -> None:
        # test_client.post()
        pass
