from pydantic import BaseModel


class CropCreate(BaseModel):
    jina: str
    aina: str
    msimu: str
    farm_id: int