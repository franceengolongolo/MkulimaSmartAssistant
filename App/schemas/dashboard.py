from pydantic import BaseModel
from datetime import date


class ZaoDashboard(BaseModel):
    jina: str
    aina: str
    msimu: str
    tarehe_ya_kupanda: date | None = None


class ActivitySummary(BaseModel):
    jumla: int
    zilizokamilika: int
    ambazo_hazijakamilika: int


class RatibaItem(BaseModel):
    jina: str
    siku: int | None = None
    tarehe: date
    siku_zimebaki: int
    maelezo: str | None = None


class RatibaDashboard(BaseModel):
    inayofuata: RatibaItem | None = None
    zijazo: list[RatibaItem]


class CropDashboard(BaseModel):
    zao: ZaoDashboard
    activities: ActivitySummary
    ratiba: RatibaDashboard