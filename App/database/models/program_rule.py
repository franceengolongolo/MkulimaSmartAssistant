from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from App.database.database import Base


class ProgramRule(Base):
    __tablename__ = "program_rules"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    task_id = Column(
        Integer,
        ForeignKey("program_tasks.id"),
        nullable=False
    )

    trigger_type = Column(
        String,
        nullable=False
    )

    offset_value = Column(
        Integer,
        nullable=True
    )

    offset_unit = Column(
        String,
        nullable=True
    )

    stage_id = Column(
        Integer,
        ForeignKey("program_stages.id"),
        nullable=True
    )

    maelezo = Column(
        Text,
        nullable=True
    )

    task = relationship(
        "ProgramTask",
        back_populates="rules"
    )

    stage = relationship(
        "ProgramStage"
    )