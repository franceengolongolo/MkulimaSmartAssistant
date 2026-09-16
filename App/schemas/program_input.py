from pydantic import BaseModel


class ProgramInputBase(BaseModel):
    task_id: int
    jina: str
    aina: str
    kiasi: str | None = None
    unit: str | None = None
    njia_ya_matumizi: str | None = None
    maelezo: str | None = None


class ProgramInputCreate(ProgramInputBase):
    pass


class ProgramInputResponse(ProgramInputBase):
    id: int

    class Config:
        from_attributes = True