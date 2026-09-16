from pydantic import BaseModel
from datetime import date


class ProgramSourceBase(BaseModel):
    program_id: int
    jina_la_chanzo: str
    taasisi: str | None = None
    url: str | None = None
    tarehe_ya_chanzo: date | None = None
    maelezo: str | None = None


class ProgramSourceCreate(ProgramSourceBase):
    pass


class ProgramSourceResponse(ProgramSourceBase):
    id: int

    class Config:
        from_attributes = True