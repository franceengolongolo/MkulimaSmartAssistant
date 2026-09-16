from datetime import date

from sqlalchemy.orm import Session

from App.database.models.reminder import Reminder
from App.database.models.crop import Crop
from App.database.models.farm import Farm


# =========================================================
# HELPER: TAARIFA ZA NOTIFICATION
# =========================================================

def notification_to_dict(
    reminder: Reminder,
    aina: str
):
    """
    Badilisha Reminder kuwa notification dictionary.

    `aina` inaweza kuwa:
    - leo
    - imepita
    - inayokuja
    """

    crop = reminder.crop
    farm = crop.farm if crop else None

    return {
        "id": reminder.id,
        "aina": aina,
        "title": "Kumbusho la zao",
        "ujumbe": reminder.ujumbe,
        "tarehe": reminder.tarehe,
        "hali": reminder.hali,

        "crop_id": reminder.crop_id,
        "zao": getattr(crop, "jina", None) if crop else None,

        "farm_id": getattr(crop, "farm_id", None) if crop else None,
        "shamba": getattr(farm, "jina", None) if farm else None,

        "schedule_id": reminder.schedule_id
    }


# =========================================================
# NOTIFICATIONS ZA LEO
# =========================================================

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

    return [
        notification_to_dict(
            reminder,
            "leo"
        )
        for reminder in reminders
    ]


# =========================================================
# NOTIFICATIONS ZILIZOPITA
# =========================================================

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

    return [
        notification_to_dict(
            reminder,
            "imepita"
        )
        for reminder in reminders
    ]


# =========================================================
# NOTIFICATIONS ZINAZOKUJA
# =========================================================

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

    return [
        notification_to_dict(
            reminder,
            "inayokuja"
        )
        for reminder in reminders
    ]