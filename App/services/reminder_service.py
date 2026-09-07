from datetime import date

from sqlalchemy.orm import Session

from App.database.models.reminder import Reminder


def create_reminder_from_schedule(
    db: Session,
    ujumbe: str,
    tarehe: date,
    crop_id: int,
    schedule_id: int
):
    """
    Tengeneza reminder kutoka kwenye schedule.

    Service hii haitumii db.commit().
    Transaction inasimamiwa na router inayoiita.
    """

    reminder = Reminder(
        ujumbe=ujumbe,
        tarehe=tarehe,
        hali="haijakamilika",
        crop_id=crop_id,
        schedule_id=schedule_id
    )

    db.add(reminder)
    db.flush()

    return reminder