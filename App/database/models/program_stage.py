from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from App.database.database import Base


class ProgramStage(Base):
    __tablename__ = "program_stages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    program_id = Column(
        Integer,
        ForeignKey("crop_programs.id"),
        nullable=False
    )

    jina = Column(
        String,
        nullable=False
    )

    namba_ya_hatua = Column(
        Integer,
        nullable=False
    )

    maelezo = Column(
        Text,
        nullable=True
    )

    program = relationship(
        "CropProgram",
        back_populates="stages"
    )

    tasks = relationship(
        "ProgramTask",
        back_populates="stage"
    )