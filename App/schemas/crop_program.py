from pydantic import BaseModel
from datetime import datetime


class CropProgramBase(BaseModel):
    jina: str
    aina_ya_zao: str
    aina_ya_program: str
    msimu: str | None = None
    maelezo: str | None = None


class CropProgramCreate(CropProgramBase):
    version: int = 1
    hali: str = "active"


class CropProgramResponse(CropProgramBase):
    id: int
    version: int
    hali: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True