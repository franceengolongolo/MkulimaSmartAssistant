from pydantic import BaseModel
from datetime import date


class CostCreate(BaseModel):

    jina: str
    aina: str
    kiasi: float | None = None
    unit: str | None = None
    gharama: float
    tarehe: date
    maelezo: str | None = None
    crop_id: int


class CostResponse(BaseModel):

    id: int
    jina: str
    aina: str
    kiasi: float | None = None
    unit: str | None = None
    gharama: float
    tarehe: date
    maelezo: str | None = None
    crop_id: int