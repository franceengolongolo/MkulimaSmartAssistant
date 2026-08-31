from pydantic import BaseModel
from datetime import date


class ActivityCreate(BaseModel):
    jina: str
    maelezo: str | None = None
    tarehe: date
    crop_id: int