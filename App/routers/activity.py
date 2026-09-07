from fastapi import APIRouter, Depends
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


# GET ALL ACTIVITIES ZA FARMER ALIYE-LOGIN
@router.get("/")
def get_activities(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    return (
        db.query(Activity)
        .join(Crop, Activity.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(Farm.farmer_id == current_farmer_id)
        .all()
    )


# CREATE ACTIVITY
@router.post("/")
def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    # Hakikisha crop ni ya farmer aliye-login
    crop = (
        db.query(Crop)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Crop.id == activity.crop_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if crop is None:
        return {
            "ujumbe": "Zao halikupatikana au si lako"
        }

    new_activity = Activity(
        jina=activity.jina,
        maelezo=activity.maelezo,
        tarehe=activity.tarehe,
        hali=activity.hali,
        crop_id=activity.crop_id
    )

    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)

    return new_activity


# GET ACTIVITY MOJA
@router.get("/{activity_id}")
def get_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    activity = (
        db.query(Activity)
        .join(Crop, Activity.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Activity.id == activity_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if activity is None:
        return {
            "ujumbe": "Shughuli haikupatikana"
        }

    return activity


# UPDATE ACTIVITY
@router.put("/{activity_id}")
def update_activity(
    activity_id: int,
    activity: ActivityCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    existing_activity = (
        db.query(Activity)
        .join(Crop, Activity.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Activity.id == activity_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if existing_activity is None:
        return {
            "ujumbe": "Shughuli haikupatikana"
        }

    # Hakikisha crop mpya pia ni ya farmer huyu
    crop = (
        db.query(Crop)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Crop.id == activity.crop_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if crop is None:
        return {
            "ujumbe": "Zao jipya halikupatikana au si lako"
        }

    existing_activity.jina = activity.jina
    existing_activity.maelezo = activity.maelezo
    existing_activity.tarehe = activity.tarehe
    existing_activity.hali = activity.hali
    existing_activity.crop_id = activity.crop_id

    db.commit()
    db.refresh(existing_activity)

    return existing_activity


# KUKAMILISHA ACTIVITY
@router.patch("/{activity_id}/complete")
def complete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    activity = (
        db.query(Activity)
        .join(Crop, Activity.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Activity.id == activity_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if activity is None:
        return {
            "ujumbe": "Shughuli haikupatikana"
        }

    activity.hali = "imekamilika"

    db.commit()
    db.refresh(activity)

    return {
        "ujumbe": "Shughuli imekamilika",
        "activity": activity
    }


# DELETE ACTIVITY
@router.delete("/{activity_id}")
def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    activity = (
        db.query(Activity)
        .join(Crop, Activity.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Activity.id == activity_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if activity is None:
        return {
            "ujumbe": "Shughuli haikupatikana"
        }

    db.delete(activity)
    db.commit()

    return {
        "ujumbe": "Shughuli imefutwa kikamilifu"
    }