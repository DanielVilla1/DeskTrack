import os
from collections.abc import Callable

import pytest
from fastapi.testclient import TestClient

from app.core.config import Environment, Settings

TEST_DATABASE_URL = "postgresql+psycopg://test:test@localhost:5432/test"
TEST_CORS_ORIGIN = "http://localhost:5173"

# app.main builds its module-level app when imported, which reads these variables.
os.environ.setdefault("DATABASE_URL", TEST_DATABASE_URL)
os.environ.setdefault("CORS_ORIGINS", TEST_CORS_ORIGIN)


@pytest.fixture
def settings() -> Settings:
    return Settings(
        database_url=TEST_DATABASE_URL,
        environment=Environment.DEVELOPMENT,
        cors_origins=TEST_CORS_ORIGIN,
    )


@pytest.fixture
def build_client() -> Callable[[Settings], TestClient]:
    from app.main import create_app

    def build(settings: Settings) -> TestClient:
        return TestClient(create_app(settings))

    return build


@pytest.fixture
def client(settings: Settings, build_client: Callable[[Settings], TestClient]) -> TestClient:
    return build_client(settings)
