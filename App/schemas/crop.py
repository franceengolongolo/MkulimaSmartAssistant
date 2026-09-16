from pydantic import BaseModel
from datetime import date


class CropCreate(BaseModel):
    jina: str
    aina: str
    msimu: str
    farm_id: int
    tarehe_ya_kupanda: date | None = None
    program_id: int | None = None


class CropReminder(BaseModel):
    id: int
    ujumbe: str
    tarehe: date
    hali: str
    crop_id: int