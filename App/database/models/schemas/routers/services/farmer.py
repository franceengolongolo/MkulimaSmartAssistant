from pydantic import BaseModel


class FarmerCreate(BaseModel):
    jina: str
    simu: str
    eneo: str


class FarmerResponse(BaseModel):
    id: int
    jina: str
    simu: str
    eneo: str