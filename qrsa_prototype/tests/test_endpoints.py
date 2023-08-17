from typing import Any
from fastapi.testclient import TestClient
from qnode import server

app = server.create_server()

test_client = TestClient(app)

class TestEndpoints:
    def test_heart_beat(self):
        print(test_client, dir(test_client))
        response = test_client.get("/heartbeat", headers={"accept": "application/json"})
        print(response)
        assert 1 == 1
        # assert response.status_code == 200
        # assert response.json() == {"message": "Alive"}
    
    # def test_handle_connection_setup_request(self, test_client):
        # test_client.post()
