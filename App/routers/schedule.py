from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.schedule import Schedule
from App.database.models.crop import Crop
from App.database.models.farm import Farm
from App.database.models.reminder import Reminder
from App.schemas.schedule import ScheduleCreate
from App.services.reminder_service import create_reminder_from_schedule
from App.services.auth_service import get_current_farmer


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


def calculate_schedule_status(
    crop: Crop,
    siku: int | None,
    current_status: str | None = None
) -> str:
    """
    Hesabu status ya schedule kulingana na tarehe ya kupanda.

    Kama schedule tayari imekamilika, status yake inalindwa
    na haibadilishwi.
    """

    if current_status == "imekamilika":
        return "imekamilika"

    if crop.tarehe_ya_kupanda is None or siku is None:
        return "inayofuata"

    tarehe_ratiba = (
        crop.tarehe_ya_kupanda
        + timedelta(days=siku)
    )

    leo = date.today()

    if tarehe_ratiba == leo:
        return "leo"

    if tarehe_ratiba > leo:
        return "inayofuata"

    return "imepita"


def get_farmer_schedule(
    db: Session,
    schedule_id: int,
    current_farmer_id: int
):
    return (
        db.query(Schedule)
        .join(Crop, Schedule.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Schedule.id == schedule_id,
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
# UPDATE STATUS ZA RATIBA
# =========================================================

@router.patch("/update-status")
def update_schedule_status(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    leo = date.today()

    schedules = (
        db.query(Schedule)
        .join(Crop, Schedule.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Farm.farmer_id == current_farmer_id
        )
        .all()
    )

    try:
        for schedule in schedules:
            crop = schedule.crop

            schedule.status = calculate_schedule_status(
                crop=crop,
                siku=schedule.siku,
                current_status=schedule.status
            )

        db.commit()

    except Exception:
        db.rollback()
        raise

    return {
        "ujumbe": "Status za ratiba zimesasishwa",
        "tarehe_ya_leo": leo
    }


# =========================================================
# KUKAMILISHA RATIBA
# =========================================================

@router.patch("/{schedule_id}/complete")
def complete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    schedule = get_farmer_schedule(
        db=db,
        schedule_id=schedule_id,
        current_farmer_id=current_farmer_id
    )

    if schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ratiba haikupatikana"
        )

    if schedule.status == "imekamilika":
        return {
            "ujumbe": "Ratiba hii tayari imekamilika",
            "ratiba": schedule
        }

    schedule.status = "imekamilika"

    reminder = (
        db.query(Reminder)
        .filter(
            Reminder.schedule_id == schedule.id
        )
        .first()
    )

    if reminder is not None:
        reminder.hali = "imekamilika"

    try:
        db.commit()
        db.refresh(schedule)

    except Exception:
        db.rollback()
        raise

    return {
        "ujumbe": "Ratiba imekamilika",
        "ratiba": schedule
    }


# =========================================================
# GET RATIBA ZOTE ZA FARMER
# =========================================================

@router.get("/")
def get_schedules(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    schedules = (
        db.query(Schedule)
        .join(Crop, Schedule.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Farm.farmer_id == current_farmer_id
        )
        .order_by(
            Schedule.siku.asc(),
            Schedule.id.asc()
        )
        .all()
    )

    return schedules


# =========================================================
# CREATE RATIBA
# =========================================================

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def create_schedule(
    schedule: ScheduleCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = get_farmer_crop(
        db=db,
        crop_id=schedule.crop_id,
        current_farmer_id=current_farmer_id
    )

    if crop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zao halikupatikana au si lako"
        )

    new_schedule = Schedule(
        jina=schedule.jina,
        maelezo=schedule.maelezo,
        siku=schedule.siku,
        crop_id=schedule.crop_id,
        status=calculate_schedule_status(
            crop=crop,
            siku=schedule.siku
        )
    )

    db.add(new_schedule)

    try:
        # Schedule ipate ID kwanza.
        db.flush()

        # Tengeneza Reminder automatically kama
        # crop ina tarehe ya kupanda.
        if crop.tarehe_ya_kupanda is not None:
            tarehe_reminder = (
                crop.tarehe_ya_kupanda
                + timedelta(days=schedule.siku)
            )

            create_reminder_from_schedule(
                db=db,
                ujumbe=schedule.jina,
                tarehe=tarehe_reminder,
                crop_id=schedule.crop_id,
                schedule_id=new_schedule.id
            )

        db.commit()
        db.refresh(new_schedule)

    except Exception:
        db.rollback()
        raise

    return new_schedule


# =========================================================
# GET RATIBA MOJA
# =========================================================

@router.get("/{schedule_id}")
def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    schedule = get_farmer_schedule(
        db=db,
        schedule_id=schedule_id,
        current_farmer_id=current_farmer_id
    )

    if schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ratiba haikupatikana"
        )

    return schedule


# =========================================================
# UPDATE RATIBA
# =========================================================

@router.put("/{schedule_id}")
def update_schedule(
    schedule_id: int,
    schedule: ScheduleCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    existing_schedule = get_farmer_schedule(
        db=db,
        schedule_id=schedule_id,
        current_farmer_id=current_farmer_id
    )

    if existing_schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ratiba haikupatikana"
        )

    crop = get_farmer_crop(
        db=db,
        crop_id=schedule.crop_id,
        current_farmer_id=current_farmer_id
    )

    if crop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zao jipya halikupatikana au si lako"
        )

    existing_schedule.jina = schedule.jina
    existing_schedule.maelezo = schedule.maelezo
    existing_schedule.siku = schedule.siku
    existing_schedule.crop_id = schedule.crop_id

    existing_schedule.status = calculate_schedule_status(
        crop=crop,
        siku=schedule.siku,
        current_status=existing_schedule.status
    )

    try:
        # Tafuta Reminder inayohusiana moja kwa moja
        # na Schedule hii.
        reminder = (
            db.query(Reminder)
            .filter(
                Reminder.schedule_id == existing_schedule.id
            )
            .first()
        )

        if reminder is not None:
            reminder.ujumbe = schedule.jina
            reminder.crop_id = schedule.crop_id

            if crop.tarehe_ya_kupanda is not None:
                reminder.tarehe = (
                    crop.tarehe_ya_kupanda
                    + timedelta(days=schedule.siku)
                )

        elif crop.tarehe_ya_kupanda is not None:
            # Schedule haina Reminder lakini sasa inaweza
            # kupata tarehe ya Reminder.
            tarehe_reminder = (
                crop.tarehe_ya_kupanda
                + timedelta(days=schedule.siku)
            )

            create_reminder_from_schedule(
                db=db,
                ujumbe=schedule.jina,
                tarehe=tarehe_reminder,
                crop_id=schedule.crop_id,
                schedule_id=existing_schedule.id
            )

        db.commit()
        db.refresh(existing_schedule)

    except Exception:
        db.rollback()
        raise

    return existing_schedule


# =========================================================
# DELETE RATIBA
# =========================================================

@router.delete("/{schedule_id}")
def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    schedule = get_farmer_schedule(
        db=db,
        schedule_id=schedule_id,
        current_farmer_id=current_farmer_id
    )

    if schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ratiba haikupatikana"
        )

    try:
        # Futa Reminder inayohusiana kwanza.
        reminder = (
            db.query(Reminder)
            .filter(
                Reminder.schedule_id == schedule.id
            )
            .first()
        )

        if reminder is not None:
            db.delete(reminder)

        db.delete(schedule)
        db.commit()

    except Exception:
        db.rollback()
        raise

    return {
        "ujumbe": "Ratiba na kikumbusho chake vimefutwa kikamilifu"
    }