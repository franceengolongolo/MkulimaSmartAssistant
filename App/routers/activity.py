from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.activity import Activity
from App.schemas.activity import ActivityCreate

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


@router.get("/")
def get_activities(db: Session = Depends(get_db)):
    return db.query(Activity).all()


@router.post("/")
def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db)
):
    new_activity = Activity(
        jina=activity.jina,
        maelezo=activity.maelezo,
        tarehe=activity.tarehe,
        crop_id=activity.crop_id
    )

    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)

    return new_activity
@router.get("/{activity_id}")
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()

    if activity is None:
        return {
            "ujumbe": "Shughuli haikupatikana"
        }

    return activity
@router.put("/{activity_id}")
def update_activity(
    activity_id: int,
    activity: ActivityCreate,
    db: Session = Depends(get_db)
):
    existing_activity = db.query(Activity).filter(
        Activity.id == activity_id
    ).first()

    if existing_activity is None:
        return {
            "ujumbe": "Shughuli haikupatikana"
        }

    existing_activity.jina = activity.jina
    existing_activity.maelezo = activity.maelezo
    existing_activity.tarehe = activity.tarehe
    existing_activity.crop_id = activity.crop_id

    db.commit()
    db.refresh(existing_activity)

    return existing_activity