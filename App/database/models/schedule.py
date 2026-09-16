from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from App.database.database import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    jina = Column(
        String,
        nullable=False
    )

    maelezo = Column(
        String,
        nullable=True
    )

    siku = Column(
        Integer,
        nullable=True
    )

    status = Column(
        String,
        nullable=False,
        default="inayofuata"
    )

    crop_id = Column(
        Integer,
        ForeignKey("crops.id"),
        nullable=False
    )

    program_task_id = Column(
        Integer,
        ForeignKey("program_tasks.id"),
        nullable=True
    )

    crop = relationship(
        "Crop",
        back_populates="schedules"
    )

    program_task = relationship(
        "ProgramTask",
        back_populates="schedules"
    )

    reminder = relationship(
        "Reminder",
        back_populates="schedule",
        uselist=False
    )