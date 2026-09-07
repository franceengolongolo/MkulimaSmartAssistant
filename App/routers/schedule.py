from datetime import date, timedelta

from fastapi import APIRouter, Depends
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
        db.query(Schedule, Crop)
        .join(Crop, Schedule.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Farm.farmer_id == current_farmer_id
        )
        .all()
    )

    for schedule, crop in schedules:

        if (
            crop.tarehe_ya_kupanda is None
            or schedule.siku is None
        ):
            continue

        if schedule.status == "imekamilika":
            continue

        tarehe_ratiba = (
            crop.tarehe_ya_kupanda
            + timedelta(days=schedule.siku)
        )

        if tarehe_ratiba == leo:
            schedule.status = "leo"

        elif tarehe_ratiba > leo:
            schedule.status = "inayofuata"

        else:
            schedule.status = "imepita"

    db.commit()

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
    schedule = (
        db.query(Schedule)
        .join(Crop, Schedule.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Schedule.id == schedule_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if schedule is None:
        return {
            "ujumbe": "Ratiba haikupatikana"
        }

    schedule.status = "imekamilika"

    # Kama kuna reminder inayohusiana na ratiba hii,
    # nayo iwekwe imekamilika.
    reminder = (
        db.query(Reminder)
        .filter(
            Reminder.schedule_id == schedule.id
        )
        .first()
    )

    if reminder is not None:
        reminder.hali = "imekamilika"

    db.commit()
    db.refresh(schedule)

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
        .all()
    )

    return schedules


# =========================================================
# CREATE RATIBA
# =========================================================

@router.post("/")
def create_schedule(
    schedule: ScheduleCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    # Hakikisha crop ni ya farmer aliye-login
    crop = (
        db.query(Crop)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Crop.id == schedule.crop_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if crop is None:
        return {
            "ujumbe": "Zao halikupatikana au si lako"
        }

    if schedule.siku is None:
        return {
            "ujumbe": "Idadi ya siku za ratiba inahitajika"
        }

    new_schedule = Schedule(
        jina=schedule.jina,
        maelezo=schedule.maelezo,
        siku=schedule.siku,
        crop_id=schedule.crop_id,
        status="inayofuata"
    )

    db.add(new_schedule)

    try:
        # Schedule ipate ID kwanza
        db.flush()

        # Tengeneza Reminder automatically
        if crop.tarehe_ya_kupanda:

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
    schedule = (
        db.query(Schedule)
        .join(Crop, Schedule.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Schedule.id == schedule_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if schedule is None:
        return {
            "ujumbe": "Ratiba haikupatikana"
        }

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
    existing_schedule = (
        db.query(Schedule)
        .join(Crop, Schedule.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Schedule.id == schedule_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if existing_schedule is None:
        return {
            "ujumbe": "Ratiba haikupatikana"
        }

    if schedule.siku is None:
        return {
            "ujumbe": "Idadi ya siku za ratiba inahitajika"
        }

    # Hakikisha crop mpya ni ya farmer huyu
    crop = (
        db.query(Crop)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Crop.id == schedule.crop_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if crop is None:
        return {
            "ujumbe": "Zao jipya halikupatikana au si lako"
        }

    existing_schedule.jina = schedule.jina
    existing_schedule.maelezo = schedule.maelezo
    existing_schedule.siku = schedule.siku
    existing_schedule.crop_id = schedule.crop_id

    # Update status kulingana na tarehe mpya
    if existing_schedule.status != "imekamilika":

        if crop.tarehe_ya_kupanda:

            tarehe_ratiba = (
                crop.tarehe_ya_kupanda
                + timedelta(days=schedule.siku)
            )

            leo = date.today()

            if tarehe_ratiba == leo:
                existing_schedule.status = "leo"

            elif tarehe_ratiba > leo:
                existing_schedule.status = "inayofuata"

            else:
                existing_schedule.status = "imepita"

        else:
            existing_schedule.status = "inayofuata"

    try:
        # Tafuta reminder inayohusiana moja kwa moja
        # na schedule hii.
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

            if crop.tarehe_ya_kupanda:

                reminder.tarehe = (
                    crop.tarehe_ya_kupanda
                    + timedelta(days=schedule.siku)
                )

            else:
                # Kama hakuna tarehe ya kupanda,
                # hatuwezi kuhesabu tarehe ya reminder.
                reminder.tarehe = reminder.tarehe

        elif crop.tarehe_ya_kupanda:

            # Kama schedule ya zamani haina reminder,
            # tengeneza mpya.
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
    schedule = (
        db.query(Schedule)
        .join(Crop, Schedule.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Schedule.id == schedule_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if schedule is None:
        return {
            "ujumbe": "Ratiba haikupatikana"
        }

    try:
        # Futa reminder inayohusiana kwanza
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