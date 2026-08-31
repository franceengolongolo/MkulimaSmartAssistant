from pydantic import BaseModel


class ScheduleCreate(BaseModel):
    jina: str
    maelezo: str | None = None
    siku: int | None = None
    crop_id: int