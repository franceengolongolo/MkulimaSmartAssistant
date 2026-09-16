from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.reminder import Reminder
from App.database.models.crop import Crop
from App.database.models.farm import Farm
from App.schemas.reminder import ReminderCreate
from App.services.auth_service import get_current_farmer

from App.services.notification_service import (
    get_today_notifications,
    get_overdue_notifications,
    get_upcoming_notifications
)


router = APIRouter(
    prefix="/reminders",
    tags=["Reminders"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# =========================================================
# HELPER: REMINDER + TAARIFA ZA ZAO NA SHAMBA
# =========================================================

def reminder_to_dict(reminder: Reminder):
    """
    Badilisha Reminder ORM kuwa dictionary.
    """

    crop = reminder.crop
    farm = crop.farm if crop else None

    return {
        "id": reminder.id,
        "tarehe": reminder.tarehe,
        "ujumbe": reminder.ujumbe,
        "hali": reminder.hali,

        "crop_id": reminder.crop_id,
        "zao": getattr(crop, "jina", None) if crop else None,

        "farm_id": getattr(crop, "farm_id", None) if crop else None,
        "shamba": getattr(farm, "jina", None) if farm else None,

        "schedule_id": reminder.schedule_id
    }


def reminders_to_dict(reminders):
    """
    Badilisha list ya Reminder ORM kuwa list ya dictionaries.
    """

    return [
        reminder_to_dict(reminder)
        for reminder in reminders
    ]


# =========================================================
# CREATE REMINDER
# =========================================================

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def create_reminder(
    reminder: ReminderCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = (
        db.query(Crop)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Crop.id == reminder.crop_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if crop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zao halikupatikana au si lako"
        )

    new_reminder = Reminder(
        ujumbe=reminder.ujumbe,
        tarehe=reminder.tarehe,
        hali="haijakamilika",
        crop_id=reminder.crop_id
    )

    db.add(new_reminder)

    try:
        db.commit()
        db.refresh(new_reminder)

    except Exception:
        db.rollback()
        raise

    return reminder_to_dict(new_reminder)


# =========================================================
# GET REMINDERS ZOTE
# =========================================================

@router.get("/")
def get_reminders(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    reminders = (
        db.query(Reminder)
        .join(Crop, Reminder.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Farm.farmer_id == current_farmer_id
        )
        .order_by(Reminder.tarehe.asc())
        .all()
    )

    return reminders_to_dict(reminders)


# =========================================================
# GET REMINDERS ZA LEO
# =========================================================

@router.get("/today")
def get_today_reminders(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    notifications = get_today_notifications(
        db,
        current_farmer_id
    )

    return notifications


# =========================================================
# GET REMINDERS ZINAZOFUATA
# =========================================================

@router.get("/upcoming")
def get_upcoming_reminders(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    notifications = get_upcoming_notifications(
        db,
        current_farmer_id
    )

    return notifications


# =========================================================
# GET REMINDERS ZISIZOKAMILIKA
# =========================================================

@router.get("/pending")
def get_pending_reminders(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    reminders = (
        db.query(Reminder)
        .join(Crop, Reminder.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Farm.farmer_id == current_farmer_id,
            Reminder.hali != "imekamilika"
        )
        .order_by(Reminder.tarehe.asc())
        .all()
    )

    return reminders_to_dict(reminders)


# =========================================================
# REMINDER DASHBOARD
# =========================================================

@router.get("/dashboard")
def get_reminder_dashboard(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    leo = get_today_notifications(
        db,
        current_farmer_id
    )

    zilizopita = get_overdue_notifications(
        db,
        current_farmer_id
    )

    zinazokuja = get_upcoming_notifications(
        db,
        current_farmer_id
    )

    zilizokamilika = (
        db.query(Reminder)
        .join(Crop, Reminder.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Farm.farmer_id == current_farmer_id,
            Reminder.hali == "imekamilika"
        )
        .order_by(Reminder.tarehe.desc())
        .all()
    )

    return {
        "tarehe_ya_leo": date.today(),

        "idadi": {
            "leo": len(leo),
            "zinazokuja": len(zinazokuja),
            "zilizopita": len(zilizopita),
            "zilizokamilika": len(zilizokamilika)
        },

        "reminders": {
            "leo": leo,
            "zinazokuja": zinazokuja,
            "zilizopita": zilizopita,
            "zilizokamilika": reminders_to_dict(zilizokamilika)
        }
    }


# =========================================================
# AUTOMATIC NOTIFICATIONS
# =========================================================

@router.get("/notifications/automatic")
def get_automatic_notifications(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    leo = get_today_notifications(
        db,
        current_farmer_id
    )

    zilizopita = get_overdue_notifications(
        db,
        current_farmer_id
    )

    zinazokuja = get_upcoming_notifications(
        db,
        current_farmer_id
    )

    return {
        "tarehe_ya_leo": date.today(),

        "idadi": {
            "leo": len(leo),
            "zilizopita": len(zilizopita),
            "zinazokuja": len(zinazokuja),
            "jumla": (
                len(leo)
                + len(zilizopita)
                + len(zinazokuja)
            )
        },

        "notifications": {
            "leo": leo,
            "zilizopita": zilizopita,
            "zinazokuja": zinazokuja
        }
    }


# =========================================================
# NOTIFICATIONS ZA LEO
# =========================================================

@router.get("/notifications/today")
def get_today_notifications_endpoint(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    notifications = get_today_notifications(
        db,
        current_farmer_id
    )

    return notifications


# =========================================================
# NOTIFICATIONS ZILIZOCHELEWA
# =========================================================

@router.get("/notifications/overdue")
def get_overdue_notifications_endpoint(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    notifications = get_overdue_notifications(
        db,
        current_farmer_id
    )

    return notifications


# =========================================================
# NOTIFICATIONS ZINAZOKUJA
# =========================================================

@router.get("/notifications/upcoming")
def get_upcoming_notifications_endpoint(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    notifications = get_upcoming_notifications(
        db,
        current_farmer_id
    )

    return notifications


# =========================================================
# GET REMINDER MOJA
# =========================================================

@router.get("/{reminder_id}")
def get_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    reminder = (
        db.query(Reminder)
        .join(Crop, Reminder.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Reminder.id == reminder_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if reminder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kikumbusho hakikupatikana"
        )

    return reminder_to_dict(reminder)


# =========================================================
# KUKAMILISHA REMINDER
# =========================================================

@router.patch("/{reminder_id}/complete")
def complete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    reminder = (
        db.query(Reminder)
        .join(Crop, Reminder.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Reminder.id == reminder_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if reminder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kikumbusho hakikupatikana"
        )

    if reminder.hali == "imekamilika":
        return {
            "ujumbe": "Kikumbusho hiki tayari kimekamilika",
            "kikumbusho": reminder_to_dict(reminder)
        }

    reminder.hali = "imekamilika"

    try:
        db.commit()
        db.refresh(reminder)

    except Exception:
        db.rollback()
        raise

    return {
        "ujumbe": "Kikumbusho kimekamilika",
        "kikumbusho": reminder_to_dict(reminder)
    }


# =========================================================
# DELETE REMINDER
# =========================================================

@router.delete("/{reminder_id}")
def delete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    reminder = (
        db.query(Reminder)
        .join(Crop, Reminder.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Reminder.id == reminder_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if reminder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kikumbusho hakikupatikana"
        )

    reminder_info = reminder_to_dict(reminder)

    try:
        db.delete(reminder)
        db.commit()

    except Exception:
        db.rollback()
        raise

    return {
        "ujumbe": "Kikumbusho kimefutwa",
        "kikumbusho": reminder_info
    }


# =========================================================
# UPDATE REMINDER
# =========================================================

@router.put("/{reminder_id}")
def update_reminder(
    reminder_id: int,
    reminder_data: ReminderCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    reminder = (
        db.query(Reminder)
        .join(Crop, Reminder.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Reminder.id == reminder_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if reminder is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kikumbusho hakikupatikana"
        )

    crop = (
        db.query(Crop)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Crop.id == reminder_data.crop_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if crop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Zao jipya halikupatikana au si lako"
        )

    reminder.ujumbe = reminder_data.ujumbe
    reminder.tarehe = reminder_data.tarehe
    reminder.crop_id = reminder_data.crop_id

    try:
        db.commit()
        db.refresh(reminder)

    except Exception:
        db.rollback()
        raise

    return {
        "ujumbe": "Kikumbusho kimesasishwa",
        "kikumbusho": reminder_to_dict(reminder)
    }