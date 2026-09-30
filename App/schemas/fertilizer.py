from pydantic import BaseModel, field_validator


class FertilizerCreate(BaseModel):
    jina: str
    aina: str
    kampuni: str | None = None
    kiasi: float
    unit: str = "kg"
    gharama: float | None = None
    crop_id: int

    @field_validator("jina", "aina", "unit")
    @classmethod
    def validate_text_fields(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Thamani haiwezi kuwa tupu")

        return value

    @field_validator("kampuni")
    @classmethod
    def validate_kampuni(cls, value):
        if value is None:
            return value

        value = value.strip()

        return value if value else None

    @field_validator("kiasi")
    @classmethod
    def validate_kiasi(cls, value):
        if value <= 0:
            raise ValueError("Kiasi lazima kiwe zaidi ya sifuri")

        return value

    @field_validator("gharama")
    @classmethod
    def validate_gharama(cls, value):
        if value is not None and value < 0:
            raise ValueError("Gharama haiwezi kuwa hasi")

        return value

    @field_validator("crop_id")
    @classmethod
    def validate_crop_id(cls, value):
        if value <= 0:
            raise ValueError("Crop ID lazima iwe namba chanya")

        return value


class FertilizerResponse(BaseModel):
    id: int
    jina: str
    aina: str
    kampuni: str | None = None
    kiasi: float
    unit: str
    gharama: float | None = None
    crop_id: int