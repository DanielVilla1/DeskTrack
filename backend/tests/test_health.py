from fastapi.testclient import TestClient

HEALTH_URL = "/api/v1/health"


def test_health_returns_ok_in_the_success_envelope(client: TestClient) -> None:
    response = client.get(HEALTH_URL)

    assert response.status_code == 200
    assert response.json() == {"data": {"status": "ok"}}


def test_health_rejects_methods_other_than_get(client: TestClient) -> None:
    response = client.post(HEALTH_URL)

    assert response.status_code == 405
    assert response.json()["error"]["code"] == "METHOD_NOT_ALLOWED"
