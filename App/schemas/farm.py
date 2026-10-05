from pydantic import BaseModel


class FarmCreate(BaseModel):
    jina: str
    eneo: str
    ukubwa: float
    farmer_id: int | None = None


class FarmResponse(BaseModel):
    id: int
    jina: str
    eneo: str
    ukubwa: float
    farmer_id: int


class FarmUpdate(BaseModel):
    jina: str
    eneo: str
    ukubwa: float
    farmer_id: int