from datetime import date

from pydantic import BaseModel, field_validator


class ReminderCreate(BaseModel):
    ujumbe: str
    tarehe: date
    crop_id: int

    @field_validator("ujumbe")
    @classmethod
    def validate_ujumbe(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Ujumbe wa kikumbusho hauwezi kuwa tupu")

        return value

    @field_validator("crop_id")
    @classmethod
    def validate_crop_id(cls, value):
        if value <= 0:
            raise ValueError("Crop ID lazima iwe namba chanya")

        return value