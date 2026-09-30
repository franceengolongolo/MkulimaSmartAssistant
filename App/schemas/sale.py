from datetime import date

from pydantic import BaseModel, field_validator


class SaleCreate(BaseModel):
    kiasi: float
    unit: str
    bei_kwa_unit: float
    tarehe: date
    maelezo: str | None = None
    harvest_id: int

    @field_validator("kiasi")
    @classmethod
    def validate_kiasi(cls, value):
        if value <= 0:
            raise ValueError(
                "Kiasi cha mauzo lazima kiwe zaidi ya sifuri"
            )
        return value

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, value):
        value = value.strip()

        if not value:
            raise ValueError(
                "Unit ya mauzo haiwezi kuwa tupu"
            )

        return value

    @field_validator("bei_kwa_unit")
    @classmethod
    def validate_bei_kwa_unit(cls, value):
        if value <= 0:
            raise ValueError(
                "Bei kwa unit lazima iwe zaidi ya sifuri"
            )
        return value

    @field_validator("harvest_id")
    @classmethod
    def validate_harvest_id(cls, value):
        if value <= 0:
            raise ValueError(
                "Harvest ID lazima iwe namba chanya"
            )
        return value


class SaleResponse(BaseModel):
    id: int
    kiasi: float
    unit: str
    bei_kwa_unit: float
    jumla: float
    tarehe: date
    maelezo: str | None = None
    harvest_id: int