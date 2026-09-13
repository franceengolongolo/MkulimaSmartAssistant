from pydantic import BaseModel


class SeasonData(BaseModel):
    crop_id: int
    zao: str
    msimu: str | None = None
    jumla_ya_gharama: float
    jumla_ya_mavuno: float
    unit_ya_mavuno: str | None = None
    jumla_ya_mauzo: float
    unit_ya_mauzo: str | None = None
    jumla_ya_mapato: float
    faida_au_hasara: float
    hali: str


class SeasonDifference(BaseModel):
    gharama: float
    mavuno: float
    mauzo: float
    mapato: float
    faida_au_hasara: float


class SeasonComparisonResponse(BaseModel):
    msimu_wa_kwanza: SeasonData
    msimu_wa_pili: SeasonData
    tofauti: SeasonDifference
    msimu_bora: str