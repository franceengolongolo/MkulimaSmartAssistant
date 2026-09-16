from pydantic import BaseModel


class ProgramRuleBase(BaseModel):
    task_id: int
    trigger_type: str
    offset_value: int | None = None
    offset_unit: str | None = None
    stage_id: int | None = None
    maelezo: str | None = None


class ProgramRuleCreate(ProgramRuleBase):
    pass


class ProgramRuleResponse(ProgramRuleBase):
    id: int

    class Config:
        from_attributes = True