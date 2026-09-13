from pydantic import BaseModel
from datetime import date


class SaleCreate(BaseModel):

    kiasi: float
    unit: str
    bei_kwa_unit: float
    tarehe: date
    maelezo: str | None = None
    harvest_id: int


class SaleResponse(BaseModel):

    id: int
    kiasi: float
    unit: str
    bei_kwa_unit: float
    jumla: float
    tarehe: date
    maelezo: str | None = None
    harvest_id: int