from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.services.auth_service import get_current_farmer
from App.services.pdf_service import generate_crop_pdf


router = APIRouter(
    prefix="/pdf",
    tags=["PDF Reports"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/crop/{crop_id}")
def download_crop_pdf(
    crop_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    pdf = generate_crop_pdf(
        db=db,
        crop_id=crop_id,
        current_farmer_id=current_farmer_id
    )

    if pdf is None:
        raise HTTPException(
            status_code=404,
            detail="Zao halikupatikana"
        )

    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f"attachment; filename=ripoti_zao_{crop_id}.pdf"
            )
        }
    )