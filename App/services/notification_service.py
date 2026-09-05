from sqlalchemy.orm import Session
from datetime import date

from App.database.models.reminder import Reminder


def get_today_notifications(
    db: Session
):
    leo = date.today()

    reminders = db.query(Reminder).filter(
        Reminder.tarehe == leo,
        Reminder.hali != "imekamilika"
    ).order_by(
        Reminder.tarehe.asc()
    ).all()

    return reminders


def get_overdue_notifications(
    db: Session
):
    leo = date.today()

    reminders = db.query(Reminder).filter(
        Reminder.tarehe < leo,
        Reminder.hali != "imekamilika"
    ).order_by(
        Reminder.tarehe.asc()
    ).all()

    return reminders


def get_upcoming_notifications(
    db: Session
):
    leo = date.today()

    reminders = db.query(Reminder).filter(
        Reminder.tarehe > leo,
        Reminder.hali != "imekamilika"
    ).order_by(
        Reminder.tarehe.asc()
    ).all()

    return reminders