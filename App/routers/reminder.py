from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from App.services.notification_service import (
    get_today_notifications,
    get_overdue_notifications,
    get_upcoming_notifications
)

from App.database.database import SessionLocal
from App.database.models.reminder import Reminder
from App.schemas.reminder import ReminderCreate
from datetime import date


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


@router.post("/")
def create_reminder(
    reminder: ReminderCreate,
    db: Session = Depends(get_db)
):
    new_reminder = Reminder(
        ujumbe=reminder.ujumbe,
        tarehe=reminder.tarehe,
        crop_id=reminder.crop_id
    )

    db.add(new_reminder)
    db.commit()
    db.refresh(new_reminder)

    return new_reminder
@router.get("/")
def get_reminders(db: Session = Depends(get_db)):
    reminders = db.query(Reminder).all()

    return reminders
@router.get("/today")
def get_today_reminders(
    db: Session = Depends(get_db)
):
    leo = date.today()

    reminders = db.query(Reminder).filter(
        Reminder.tarehe == leo,
        Reminder.hali != "imekamilika"
    ).all()

    return reminders
@router.get("/upcoming")
def get_upcoming_reminders(
    db: Session = Depends(get_db)
):
    leo = date.today()

    reminders = db.query(Reminder).filter(
        Reminder.tarehe > leo,
        Reminder.hali != "imekamilika"
    ).order_by(Reminder.tarehe.asc()).all()

    return reminders
@router.get("/pending")
def get_pending_reminders(
    db: Session = Depends(get_db)
):
    reminders = db.query(Reminder).filter(
        Reminder.hali != "imekamilika"
    ).order_by(Reminder.tarehe.asc()).all()

    return reminders
@router.get("/dashboard")
def get_reminder_dashboard(
    db: Session = Depends(get_db)
):
    leo = date.today()

    leo_reminders = db.query(Reminder).filter(
        Reminder.tarehe == leo,
        Reminder.hali != "imekamilika"
    ).all()

    vinavyofuata = db.query(Reminder).filter(
        Reminder.tarehe > leo,
        Reminder.hali != "imekamilika"
    ).order_by(Reminder.tarehe.asc()).all()

    vilivyopita = db.query(Reminder).filter(
        Reminder.tarehe < leo,
        Reminder.hali != "imekamilika"
    ).order_by(Reminder.tarehe.asc()).all()

    vilivyokamilika = db.query(Reminder).filter(
        Reminder.hali == "imekamilika"
    ).order_by(Reminder.tarehe.desc()).all()

    return {
        "leo": leo_reminders,
        "vinavyofuata": vinavyofuata,
        "vilivyopita": vilivyopita,
        "vilivyokamilika": vilivyokamilika
    }
@router.get("/notifications/today")
def get_today_notifications_endpoint(
    db: Session = Depends(get_db)
):
    return get_today_notifications(db)


@router.get("/notifications/overdue")
def get_overdue_notifications_endpoint(
    db: Session = Depends(get_db)
):
    return get_overdue_notifications(db)


@router.get("/notifications/upcoming")
def get_upcoming_notifications_endpoint(
    db: Session = Depends(get_db)
):
    return get_upcoming_notifications(db)
@router.get("/{reminder_id}")
def get_reminder(
    reminder_id: int,
    db: Session = Depends(get_db)
):
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id
    ).first()

    if reminder is None:
        return {
            "ujumbe": "Kikumbusho hakikupatikana"
        }

    return reminder
@router.patch("/{reminder_id}/complete")
def complete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db)
):
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id
    ).first()

    if reminder is None:
        return {
            "ujumbe": "Kikumbusho hakikupatikana"
        }

    reminder.hali = "imekamilika"

    db.commit()
    db.refresh(reminder)

    return {
        "ujumbe": "Kikumbusho kimekamilika",
        "kikumbusho": reminder
    }
@router.delete("/{reminder_id}")
def delete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db)
):
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id
    ).first()

    if reminder is None:
        return {
            "ujumbe": "Kikumbusho hakikupatikana"
        }

    db.delete(reminder)
    db.commit()

    return {
        "ujumbe": "Kikumbusho kimefutwa"
    }
@router.put("/{reminder_id}")
def update_reminder(
    reminder_id: int,
    reminder_data: ReminderCreate,
    db: Session = Depends(get_db)
):
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id
    ).first()

    if reminder is None:
        return {
            "ujumbe": "Kikumbusho hakikupatikana"
        }

    reminder.ujumbe = reminder_data.ujumbe
    reminder.tarehe = reminder_data.tarehe
    reminder.crop_id = reminder_data.crop_id

    db.commit()
    db.refresh(reminder)

    return reminder
@router.get("/today")
def get_today_reminders(
    db: Session = Depends(get_db)
):
    leo = date.today()

    reminders = db.query(Reminder).filter(
        Reminder.tarehe == leo,
        Reminder.hali != "imekamilika"
    ).all()

    return reminders