from pydantic import BaseModel
from datetime import date


class CropCreate(BaseModel):
    jina: str
    aina: str
    msimu: str
    farm_id: int
    tarehe_ya_kupanda: date | None = None