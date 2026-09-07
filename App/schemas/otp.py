from pydantic import BaseModel


class OTPRequest(BaseModel):
    simu: str


class OTPVerify(BaseModel):
    simu: str
    code: str