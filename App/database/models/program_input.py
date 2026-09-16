from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from App.database.database import Base


class ProgramInput(Base):
    __tablename__ = "program_inputs"

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

    jina = Column(
        String,
        nullable=False
    )

    aina = Column(
        String,
        nullable=False
    )

    kiasi = Column(
        String,
        nullable=True
    )

    unit = Column(
        String,
        nullable=True
    )

    njia_ya_matumizi = Column(
        String,
        nullable=True
    )

    maelezo = Column(
        Text,
        nullable=True
    )

    task = relationship(
        "ProgramTask",
        back_populates="inputs"
    )