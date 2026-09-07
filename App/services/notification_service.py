from sqlalchemy.orm import Session
from datetime import date

from App.database.models.reminder import Reminder
from App.database.models.crop import Crop
from App.database.models.farm import Farm


def get_today_notifications(
    db: Session,
    current_farmer_id: int
):
    leo = date.today()

    reminders = (
        db.query(Reminder)
        .join(Crop, Reminder.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Farm.farmer_id == current_farmer_id,
            Reminder.tarehe == leo,
            Reminder.hali != "imekamilika"
        )
        .order_by(Reminder.tarehe.asc())
        .all()
    )

    return reminders


def get_overdue_notifications(
    db: Session,
    current_farmer_id: int
):
    leo = date.today()

    reminders = (
        db.query(Reminder)
        .join(Crop, Reminder.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Farm.farmer_id == current_farmer_id,
            Reminder.tarehe < leo,
            Reminder.hali != "imekamilika"
        )
        .order_by(Reminder.tarehe.asc())
        .all()
    )

    return reminders


def get_upcoming_notifications(
    db: Session,
    current_farmer_id: int
):
    leo = date.today()

    reminders = (
        db.query(Reminder)
        .join(Crop, Reminder.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Farm.farmer_id == current_farmer_id,
            Reminder.tarehe > leo,
            Reminder.hali != "imekamilika"
        )
        .order_by(Reminder.tarehe.asc())
        .all()
    )

    return reminders