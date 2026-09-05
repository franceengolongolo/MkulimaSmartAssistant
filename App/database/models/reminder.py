from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from App.database.database import Base


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)

    ujumbe = Column(String, nullable=False)

    tarehe = Column(Date, nullable=False)

    hali = Column(
        String,
        nullable=False,
        default="haijakamilika"
    )

    crop_id = Column(
        Integer,
        ForeignKey("crops.id"),
        nullable=False
    )

    crop = relationship(
        "Crop",
        back_populates="reminders"
    )