from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.schedule import Schedule
from App.schemas.schedule import ScheduleCreate


router = APIRouter(
    prefix="/schedules",
    tags=["Schedules"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_schedules(db: Session = Depends(get_db)):
    return db.query(Schedule).all()


@router.post("/")
def create_schedule(
    schedule: ScheduleCreate,
    db: Session = Depends(get_db)
):
    new_schedule = Schedule(
        jina=schedule.jina,
        maelezo=schedule.maelezo,
        siku=schedule.siku,
        crop_id=schedule.crop_id
    )

    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)

    return new_schedule
@router.get("/{schedule_id}")
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()

    if schedule is None:
        return {
            "ujumbe": "Ratiba haikupatikana"
        }

    return schedule
@router.put("/{schedule_id}")
def update_schedule(
    schedule_id: int,
    schedule: ScheduleCreate,
    db: Session = Depends(get_db)
):
    existing_schedule = db.query(Schedule).filter(
        Schedule.id == schedule_id
    ).first()

    if existing_schedule is None:
        return {
            "ujumbe": "Ratiba haikupatikana"
        }

    existing_schedule.jina = schedule.jina
    existing_schedule.maelezo = schedule.maelezo
    existing_schedule.siku = schedule.siku
    existing_schedule.crop_id = schedule.crop_id

    db.commit()
    db.refresh(existing_schedule)

    return existing_schedule
@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(Schedule).filter(
        Schedule.id == schedule_id
    ).first()

    if schedule is None:
        return {
            "ujumbe": "Ratiba haikupatikana"
        }

    db.delete(schedule)
    db.commit()

    return {
        "ujumbe": "Ratiba imefutwa kikamilifu"
    }