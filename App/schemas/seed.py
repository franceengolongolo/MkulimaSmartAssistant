from pydantic import BaseModel


class SeedCreate(BaseModel):

    jina: str

    aina: str

    kampuni: str | None = None

    kiasi: float

    unit: str = "kg"

    gharama: float | None = None

    crop_id: int


class SeedResponse(BaseModel):

    id: int

    jina: str

    aina: str

    kampuni: str | None = None

    kiasi: float

    unit: str

    gharama: float | None = None

    crop_id: int