import pytest
from pydantic import ValidationError

from app.core.config import Environment, Settings

DATABASE_URL = "postgresql+psycopg://user:pass@localhost:5432/db"


def test_cors_origins_are_split_from_a_comma_separated_string() -> None:
    settings = Settings(
        database_url=DATABASE_URL,
        cors_origins="http://localhost:5173, https://desk.example.com ,",
    )

    assert settings.cors_origins == ["http://localhost:5173", "https://desk.example.com"]


def test_environment_defaults_to_production(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ENVIRONMENT", raising=False)

    settings = Settings(
        _env_file=None, database_url=DATABASE_URL, cors_origins="http://localhost:5173"
    )

    assert settings.environment is Environment.PRODUCTION


def test_database_password_is_hidden_from_repr_and_str() -> None:
    settings = Settings(database_url=DATABASE_URL, cors_origins="http://localhost:5173")

    assert "pass" not in repr(settings)
    assert "pass" not in str(settings)
    assert settings.database_url.get_secret_value() == DATABASE_URL


def test_missing_database_url_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(ValidationError):
        Settings(_env_file=None, cors_origins="http://localhost:5173")
