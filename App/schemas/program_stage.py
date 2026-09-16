from pydantic import BaseModel


class ProgramStageBase(BaseModel):
    program_id: int
    jina: str
    namba_ya_hatua: int
    maelezo: str | None = None


class ProgramStageCreate(ProgramStageBase):
    pass


class ProgramStageResponse(ProgramStageBase):
    id: int

    class Config:
        from_attributes = True