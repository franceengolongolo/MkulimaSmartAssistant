from pydantic import BaseModel


class PesticideCreate(BaseModel):

    jina: str

    aina: str

    kampuni: str | None = None

    kiasi: float

    unit: str = "L"

    gharama: float | None = None

    crop_id: int


class PesticideResponse(BaseModel):

    id: int

    jina: str

    aina: str

    kampuni: str | None = None

    kiasi: float

    unit: str

    gharama: float | None = None

    crop_id: int