from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.services.auth_service import get_current_farmer
from App.services.profit_loss_service import get_crop_profit_loss


router = APIRouter(
    prefix="/profit-loss",
    tags=["Profit & Loss"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/crop/{crop_id}")
def get_crop_profit_loss_report(
    crop_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    report = get_crop_profit_loss(
        db=db,
        crop_id=crop_id,
        current_farmer_id=current_farmer_id
    )

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Zao halikupatikana"
        )

    return report