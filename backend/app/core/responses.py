from pydantic import BaseModel


class SuccessResponse[DataT](BaseModel):
    """Success envelope shared by every endpoint: { "data": ... }."""

    data: DataT
