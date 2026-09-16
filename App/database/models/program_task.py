from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from App.database.database import Base


class ProgramTask(Base):
    __tablename__ = "program_tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    stage_id = Column(
        Integer,
        ForeignKey("program_stages.id"),
        nullable=False
    )

    jina = Column(
        String,
        nullable=False
    )

    aina = Column(
        String,
        nullable=False
    )

    maelezo = Column(
        Text,
        nullable=True
    )

    muhimu = Column(
        Boolean,
        nullable=False,
        default=True
    )

    stage = relationship(
        "ProgramStage",
        back_populates="tasks"
    )

    rules = relationship(
        "ProgramRule",
        back_populates="task"
    )

    inputs = relationship(
        "ProgramInput",
        back_populates="task"
    )

    schedules = relationship(
        "Schedule",
        back_populates="program_task"
    )