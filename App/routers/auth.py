from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.farmer import Farmer
from App.database.models.otp import OTPVerification
from App.schemas.otp import OTPRequest, OTPVerify
from App.services.auth_service import create_access_token

from datetime import datetime, timedelta


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/request-otp")
def request_otp(
    data: OTPRequest,
    db: Session = Depends(get_db)
):
    farmer = db.query(Farmer).filter(
        Farmer.simu == data.simu
    ).first()

    if not farmer:
        return {
            "ujumbe": "Namba ya simu haijasajiliwa kwenye mfumo."
        }

    code = "123456"

    expires_at = datetime.now() + timedelta(minutes=5)

    otp = OTPVerification(
        simu=data.simu,
        code=code,
        expires_at=expires_at,
        farmer_id=farmer.id
    )

    db.add(otp)
    db.commit()

    return {
        "ujumbe": "OTP imetengenezwa kwa ajili ya majaribio.",
        "simu": data.simu,
        "code": code
    }


@router.post("/verify-otp")
def verify_otp(
    data: OTPVerify,
    db: Session = Depends(get_db)
):
    otp = db.query(OTPVerification).filter(
        OTPVerification.simu == data.simu,
        OTPVerification.code == data.code
    ).order_by(
        OTPVerification.id.desc()
    ).first()

    if not otp:
        return {
            "ujumbe": "OTP si sahihi."
        }

    if otp.expires_at < datetime.now():
        return {
            "ujumbe": "OTP imekwisha muda wake."
        }

    farmer = db.query(Farmer).filter(
        Farmer.simu == data.simu
    ).first()

    if not farmer:
        return {
            "ujumbe": "Mkulima hakupatikana."
        }

    access_token = create_access_token(
        data={
            "farmer_id": farmer.id,
            "simu": farmer.simu
        }
    )

    return {
        "ujumbe": "Umeingia kwenye mfumo kwa mafanikio.",
        "access_token": access_token,
        "token_type": "bearer",
        "farmer_id": farmer.id,
        "jina": farmer.jina,
        "simu": farmer.simu
    }