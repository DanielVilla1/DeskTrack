import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from app.core.config import Settings
from app.core.exceptions import AppError, ErrorCode, ErrorDetail
from app.main import create_app

SECRET_INPUT = "secret-value-that-must-not-be-echoed"
SECRET_ERROR_TEXT = "secret internal detail"


class ConflictTestError(AppError):
    code = ErrorCode.CONFLICT
    status_code = 409


class NewItem(BaseModel):
    title: str = Field(min_length=1)


@pytest.fixture
def app(settings: Settings) -> FastAPI:
    app = create_app(settings)

    @app.post("/test/items")
    def create_item(item: NewItem) -> dict[str, str]:
        return {"title": item.title}

    @app.get("/test/page")
    def get_page(page: int) -> dict[str, int]:
        return {"page": page}

    @app.get("/test/conflict")
    def raise_app_error() -> None:
        raise ConflictTestError(
            "Already exists.", [ErrorDetail(field="body.title", message="Must be unique.")]
        )

    @app.get("/test/http-error/{status_code}")
    def raise_http_error(status_code: int) -> None:
        raise HTTPException(status_code=status_code, detail="Something went wrong.")

    @app.get("/test/crash")
    def crash() -> None:
        raise RuntimeError(SECRET_ERROR_TEXT)

    return app


@pytest.fixture
def test_client(app: FastAPI) -> TestClient:
    # A crashing route must come back as a 500 response instead of re-raising in the test.
    return TestClient(app, raise_server_exceptions=False)


def error_body(code: str, message: str, details: list[dict[str, str]] | None = None) -> dict:
    return {"error": {"code": code, "message": message, "details": details or []}}


def test_error_codes_match_the_architecture_list() -> None:
    assert {code.value for code in ErrorCode} == {
        "UNAUTHENTICATED",
        "FORBIDDEN",
        "NOT_FOUND",
        "METHOD_NOT_ALLOWED",
        "VALIDATION_ERROR",
        "INVALID_TRANSITION",
        "CONFLICT",
        "INTERNAL_ERROR",
    }


def test_unknown_route_returns_the_not_found_envelope(test_client: TestClient) -> None:
    response = test_client.get("/does-not-exist")

    assert response.status_code == 404
    assert response.json() == error_body("NOT_FOUND", "Not Found")


def test_wrong_method_returns_the_method_not_allowed_envelope(test_client: TestClient) -> None:
    response = test_client.post("/api/v1/health")

    assert response.status_code == 405
    assert response.json() == error_body("METHOD_NOT_ALLOWED", "Method Not Allowed")
    assert response.headers["allow"] == "GET"


def test_invalid_body_returns_a_dotted_field_path(test_client: TestClient) -> None:
    response = test_client.post("/test/items", json={"title": ""})

    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert [detail["field"] for detail in body["error"]["details"]] == ["body.title"]


def test_invalid_query_parameter_names_its_source(test_client: TestClient) -> None:
    response = test_client.get("/test/page", params={"page": "abc"})

    assert response.status_code == 422
    assert [d["field"] for d in response.json()["error"]["details"]] == ["query.page"]


def test_validation_errors_never_echo_the_submitted_input(test_client: TestClient) -> None:
    response = test_client.post("/test/items", json={"title": [SECRET_INPUT]})

    assert response.status_code == 422
    assert SECRET_INPUT not in response.text


def test_app_error_uses_its_own_code_status_and_details(test_client: TestClient) -> None:
    response = test_client.get("/test/conflict")

    assert response.status_code == 409
    assert response.json() == error_body(
        "CONFLICT", "Already exists.", [{"field": "body.title", "message": "Must be unique."}]
    )


@pytest.mark.parametrize(
    ("status_code", "expected_code"),
    [
        (401, "UNAUTHENTICATED"),
        (403, "FORBIDDEN"),
        (400, "VALIDATION_ERROR"),
        (503, "INTERNAL_ERROR"),
    ],
)
def test_http_exceptions_are_mapped_to_error_codes(
    test_client: TestClient, status_code: int, expected_code: str
) -> None:
    response = test_client.get(f"/test/http-error/{status_code}")

    assert response.status_code == status_code
    assert response.json() == error_body(expected_code, "Something went wrong.")


def test_unhandled_error_returns_a_generic_internal_error(test_client: TestClient) -> None:
    response = test_client.get("/test/crash")

    assert response.status_code == 500
    assert response.json() == error_body("INTERNAL_ERROR", "An unexpected error occurred.")
    assert SECRET_ERROR_TEXT not in response.text
