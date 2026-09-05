from pydantic import BaseModel
from datetime import date
from App.schemas.crop import CropReminder


# =========================
# CROP DASHBOARD
# =========================

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
    zao: str
    jina: str
    siku: int | None = None
    tarehe: date
    siku_zimebaki: int
    status: str
    maelezo: str | None = None


class RatibaDashboard(BaseModel):
    inayofuata: RatibaItem | None = None
    zijazo: list[RatibaItem]


class CropDashboard(BaseModel):
    zao: ZaoDashboard
    activities: ActivitySummary
    ratiba: RatibaDashboard
    reminders: list[CropReminder]


# =========================
# FARM DASHBOARD
# =========================

class FarmInfo(BaseModel):
    jina: str
    eneo: str
    ukubwa: float


class CropInfo(BaseModel):
    jina: str
    aina: str
    msimu: str | None = None


class FarmCropSummary(BaseModel):
    jumla: int
    orodha: list[CropInfo]


class FarmDashboard(BaseModel):
    shamba: FarmInfo
    mazao: FarmCropSummary
    activities: ActivitySummary
    ratiba: RatibaDashboard
    ratiba_ya_leo: list[RatibaItem]
    reminders: list[CropReminder]