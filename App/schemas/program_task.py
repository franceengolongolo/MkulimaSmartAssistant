from pydantic import BaseModel


class ProgramTaskBase(BaseModel):
    stage_id: int
    jina: str
    aina: str
    maelezo: str | None = None
    muhimu: bool = True


class ProgramTaskCreate(ProgramTaskBase):
    pass


class ProgramTaskResponse(ProgramTaskBase):
    id: int

    class Config:
        from_attributes = True