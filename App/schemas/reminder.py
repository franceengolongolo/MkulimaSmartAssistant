from pydantic import BaseModel
from datetime import date


class ReminderCreate(BaseModel):
    ujumbe: str
    tarehe: date
    crop_id: int