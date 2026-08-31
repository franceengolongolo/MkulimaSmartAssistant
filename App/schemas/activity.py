from pydantic import BaseModel
from datetime import date


class ActivityCreate(BaseModel):

    jina: str

    maelezo: str | None = None

    tarehe: date

    hali: str = "haijakamilika"

    crop_id: int