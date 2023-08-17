from typing import Any


class TestEndpoints:
    def test_heart_beat(self, test_client: Any):
        response = test_client.get("/heartbeat", headers={"accept": "application/json"})
        assert response.status_code == 200
        assert response.json() == {"message": "Alive"}

    # def test_handle_connection_setup_request(self, test_client):
        # test_client.post()
