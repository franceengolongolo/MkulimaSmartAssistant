from pydantic import BaseModel, field_validator


class ProgramRuleBase(BaseModel):

    task_id: int

    trigger_type: str

    offset_value: int | None = None

    offset_unit: str | None = None

    stage_id: int | None = None

    maelezo: str | None = None

    @field_validator("trigger_type")
    @classmethod
    def validate_trigger_type(cls, value: str) -> str:
        value = value.strip().lower()

        if not value:
            raise ValueError(
                "trigger_type haiwezi kuwa tupu"
            )

        allowed_triggers = {
            "planting",
            "harvest"
        }

        if value not in allowed_triggers:
            raise ValueError(
                "trigger_type lazima iwe planting au harvest"
            )

        return value

    @field_validator("offset_value")
    @classmethod
    def validate_offset_value(
        cls,
        value: int | None
    ) -> int | None:

        if value is not None and value < 0:
            raise ValueError(
                "offset_value haiwezi kuwa hasi"
            )

        return value

    @field_validator("offset_unit")
    @classmethod
    def validate_offset_unit(
        cls,
        value: str | None
    ) -> str | None:

        if value is None:
            return None

        value = value.strip().lower()

        if not value:
            raise ValueError(
                "offset_unit haiwezi kuwa tupu"
            )

        allowed_units = {
            "days",
            "weeks"
        }

        if value not in allowed_units:
            raise ValueError(
                "offset_unit lazima iwe days au weeks"
            )

        return value


class ProgramRuleCreate(ProgramRuleBase):

    pass


class ProgramRuleResponse(ProgramRuleBase):

    id: int

    class Config:
        from_attributes = True