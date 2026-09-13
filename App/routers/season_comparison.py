from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.services.auth_service import get_current_farmer
from App.services.season_comparison_service import compare_seasons
from App.schemas.season_comparison import SeasonComparisonResponse


router = APIRouter(
    prefix="/season-comparison",
    tags=["Season Comparison"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get(
    "/{crop_id_ya_kwanza}/{crop_id_ya_pili}",
    response_model=SeasonComparisonResponse
)
def get_season_comparison(
    crop_id_ya_kwanza: int,
    crop_id_ya_pili: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    if crop_id_ya_kwanza == crop_id_ya_pili:
        raise HTTPException(
            status_code=400,
            detail="Chagua misimu miwili tofauti"
        )

    comparison = compare_seasons(
        db=db,
        crop_id_ya_kwanza=crop_id_ya_kwanza,
        crop_id_ya_pili=crop_id_ya_pili,
        current_farmer_id=current_farmer_id
    )

    if comparison is None:
        raise HTTPException(
            status_code=404,
            detail="Moja au zote za misimu hazikupatikana"
        )

    return comparison