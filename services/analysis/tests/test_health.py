import pytest
from fastapi.testclient import TestClient

from analysis.app import app

client = TestClient(app)


@pytest.mark.small
def test_health_responds_with_200_and_an_ok_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
