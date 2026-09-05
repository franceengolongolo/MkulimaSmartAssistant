from sqlalchemy.orm import Session

from App.database.models.reminder import Reminder


def create_reminder_from_schedule(
    db: Session,
    ujumbe: str,
    tarehe,
    crop_id: int
):
    reminder = Reminder(
        ujumbe=ujumbe,
        tarehe=tarehe,
        crop_id=crop_id
    )

    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    return reminder