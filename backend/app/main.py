from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import API_V1_PREFIX, Environment, Settings, get_settings
from app.core.exceptions import register_exception_handlers
from app.core.health import router as health_router

CORS_METHODS = ["GET", "POST", "PATCH"]
CORS_HEADERS = ["Authorization", "Content-Type"]


def create_app(settings: Settings) -> FastAPI:
    docs_enabled = settings.environment is Environment.DEVELOPMENT
    app = FastAPI(
        title="DeskTrack API",
        docs_url="/docs" if docs_enabled else None,
        redoc_url="/redoc" if docs_enabled else None,
        openapi_url="/openapi.json" if docs_enabled else None,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=CORS_METHODS,
        allow_headers=CORS_HEADERS,
    )
    register_exception_handlers(app)
    app.include_router(health_router, prefix=API_V1_PREFIX)
    return app


app = create_app(get_settings())
