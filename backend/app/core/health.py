from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.responses import SuccessResponse

router = APIRouter(tags=["system"])


class HealthStatus(BaseModel):
    status: Literal["ok"] = "ok"


# Public on purpose: it is the only endpoint without a role requirement.
@router.get("/health", response_model=SuccessResponse[HealthStatus])
def get_health() -> SuccessResponse[HealthStatus]:
    return SuccessResponse(data=HealthStatus())
