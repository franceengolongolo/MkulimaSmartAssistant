from pydantic import BaseModel
from datetime import date


class HarvestCreate(BaseModel):

    kiasi: float
    unit: str
    tarehe: date
    maelezo: str | None = None
    crop_id: int


class HarvestResponse(BaseModel):

    id: int
    kiasi: float
    unit: str
    tarehe: date
    maelezo: str | None = None
    crop_id: int