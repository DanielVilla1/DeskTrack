from collections.abc import Callable

import pytest
from fastapi.testclient import TestClient

from app.core.config import Environment, Settings

DOCS_URLS = ["/docs", "/redoc", "/openapi.json"]
HEALTH_URL = "/api/v1/health"


def test_docs_are_available_in_development(client: TestClient) -> None:
    assert client.get("/docs").status_code == 200


@pytest.mark.parametrize("url", DOCS_URLS)
def test_docs_are_disabled_in_production(
    url: str, settings: Settings, build_client: Callable[[Settings], TestClient]
) -> None:
    production = settings.model_copy(update={"environment": Environment.PRODUCTION})

    assert build_client(production).get(url).status_code == 404


def test_cors_allows_a_configured_origin(client: TestClient, settings: Settings) -> None:
    origin = settings.cors_origins[0]

    response = client.get(HEALTH_URL, headers={"Origin": origin})

    assert response.headers["access-control-allow-origin"] == origin


def test_cors_ignores_an_unknown_origin(client: TestClient) -> None:
    response = client.get(HEALTH_URL, headers={"Origin": "https://evil.example.com"})

    assert "access-control-allow-origin" not in response.headers
