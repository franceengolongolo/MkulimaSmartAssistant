from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.activity import Activity
from App.database.models.crop import Crop
from App.database.models.farm import Farm
from App.schemas.activity import ActivityCreate
from App.services.auth_service import get_current_farmer


router = APIRouter(
    prefix="/activities",
    tags=["Activities"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_farmer_activity(
    db: Session,
    activity_id: int,
    current_farmer_id: int
):
    return (
        db.query(Activity)
        .join(Crop, Activity.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Activity.id == activity_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )


def get_farmer_crop(
    db: Session,
    crop_id: int,
    current_farmer_id: int
):
    return (
        db.query(Crop)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Crop.id == crop_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )


# =========================================================
# GET ALL ACTIVITIES ZA FARMER ALIYE-LOGIN
# =========================================================

@router.get("/")
def get_activities(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    return (
        db.query(Activity)
        .join(Crop, Activity.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Farm.farmer_id == current_farmer_id
        )
        .order_by(Activity.tarehe.asc(), Activity.id.asc())
        .all()
    )


# =========================================================
# CREATE ACTIVITY
# =========================================================

@router.post("/")
def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = get_farmer_crop(
        db=db,
        crop_id=activity.crop_id,
        current_farmer_id=current_farmer_id
    )

    if crop is None:
        raise HTTPException(
            status_code=404,
            detail="Zao halikupatikana au si lako"
        )

    new_activity = Activity(
        jina=activity.jina,
        maelezo=activity.maelezo,
        tarehe=activity.tarehe,
        hali=activity.hali,
        crop_id=activity.crop_id
    )

    try:
        db.add(new_activity)
        db.commit()
        db.refresh(new_activity)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Imeshindikana kuhifadhi shughuli"
        )

    return new_activity


# =========================================================
# GET ACTIVITY MOJA
# =========================================================

@router.get("/{activity_id}")
def get_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    activity = get_farmer_activity(
        db=db,
        activity_id=activity_id,
        current_farmer_id=current_farmer_id
    )

    if activity is None:
        raise HTTPException(
            status_code=404,
            detail="Shughuli haikupatikana"
        )

    return activity


# =========================================================
# UPDATE ACTIVITY
# =========================================================

@router.put("/{activity_id}")
def update_activity(
    activity_id: int,
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    existing_activity = get_farmer_activity(
        db=db,
        activity_id=activity_id,
        current_farmer_id=current_farmer_id
    )

    if existing_activity is None:
        raise HTTPException(
            status_code=404,
            detail="Shughuli haikupatikana"
        )

    crop = get_farmer_crop(
        db=db,
        crop_id=activity.crop_id,
        current_farmer_id=current_farmer_id
    )

    if crop is None:
        raise HTTPException(
            status_code=404,
            detail="Zao jipya halikupatikana au si lako"
        )

    existing_activity.jina = activity.jina
    existing_activity.maelezo = activity.maelezo
    existing_activity.tarehe = activity.tarehe
    existing_activity.hali = activity.hali
    existing_activity.crop_id = activity.crop_id

    try:
        db.commit()
        db.refresh(existing_activity)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Imeshindikana kusasisha shughuli"
        )

    return existing_activity


# =========================================================
# KUKAMILISHA ACTIVITY
# =========================================================

@router.patch("/{activity_id}/complete")
def complete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    activity = get_farmer_activity(
        db=db,
        activity_id=activity_id,
        current_farmer_id=current_farmer_id
    )

    if activity is None:
        raise HTTPException(
            status_code=404,
            detail="Shughuli haikupatikana"
        )

    activity.hali = "imekamilika"

    try:
        db.commit()
        db.refresh(activity)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Imeshindikana kukamilisha shughuli"
        )

    return {
        "ujumbe": "Shughuli imekamilika",
        "activity": activity
    }


# =========================================================
# DELETE ACTIVITY
# =========================================================

@router.delete("/{activity_id}")
def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    activity = get_farmer_activity(
        db=db,
        activity_id=activity_id,
        current_farmer_id=current_farmer_id
    )

    if activity is None:
        raise HTTPException(
            status_code=404,
            detail="Shughuli haikupatikana"
        )

    try:
        db.delete(activity)
        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Imeshindikana kufuta shughuli"
        )

    return {
        "ujumbe": "Shughuli imefutwa kikamilifu"
    }