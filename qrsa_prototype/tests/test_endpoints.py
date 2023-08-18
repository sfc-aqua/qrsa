from typing import Any


class TestEndpoints:
    def test_heart_beat(self, test_client: Any) -> None:
        with test_client as client:
            response = client.get("/heartbeat")
            assert response.status_code == 200
            assert response.json() == {"message": "Alive"}

    def test_handle_connection_setup_request(
        self, test_client: Any, base_connection_setup_request: Any
    ) -> None:
        with test_client as client:
            response = client.post(
                "/connection_setup_request",
                data=base_connection_setup_request.model_dump_json(),
                headers={"Content-Type": "application/json"},
            )
            assert response.status_code == 200
            assert response.json() == {"message": "Received connection setup request"}
