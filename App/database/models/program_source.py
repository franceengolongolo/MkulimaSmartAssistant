from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship

from App.database.database import Base


class ProgramSource(Base):
    __tablename__ = "program_sources"

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

    jina_la_chanzo = Column(
        String,
        nullable=False
    )

    taasisi = Column(
        String,
        nullable=True
    )

    url = Column(
        String,
        nullable=True
    )

    tarehe_ya_chanzo = Column(
        Date,
        nullable=True
    )

    maelezo = Column(
        Text,
        nullable=True
    )

    program = relationship(
        "CropProgram",
        back_populates="sources"
    )