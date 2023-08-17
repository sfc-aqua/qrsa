import pytest
from fastapi.testclient import TestClient
from qnode import server


@pytest.fixture()
def test_client():
    app = server.create_server()
    return TestClient(app)
