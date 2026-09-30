from pydantic import BaseModel, field_validator


class ScheduleCreate(BaseModel):
    jina: str
    maelezo: str | None = None
    siku: int
    crop_id: int

    @field_validator("jina")
    @classmethod
    def validate_jina(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Jina la ratiba haliwezi kuwa tupu")

        return value

    @field_validator("maelezo")
    @classmethod
    def validate_maelezo(cls, value):
        if value is None:
            return value

        value = value.strip()

        return value if value else None

    @field_validator("siku")
    @classmethod
    def validate_siku(cls, value):
        if value < 0:
            raise ValueError(
                "Idadi ya siku za ratiba haiwezi kuwa hasi"
            )

        return value

    @field_validator("crop_id")
    @classmethod
    def validate_crop_id(cls, value):
        if value <= 0:
            raise ValueError(
                "Crop ID lazima iwe namba chanya"
            )

        return value