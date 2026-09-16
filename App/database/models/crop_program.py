from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from App.database.database import Base


class CropProgram(Base):
    __tablename__ = "crop_programs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    jina = Column(
        String,
        nullable=False
    )

    aina_ya_zao = Column(
        String,
        nullable=False
    )

    aina_ya_program = Column(
        String,
        nullable=False
    )

    msimu = Column(
        String,
        nullable=True
    )

    maelezo = Column(
        Text,
        nullable=True
    )

    version = Column(
        Integer,
        nullable=False,
        default=1
    )

    hali = Column(
        String,
        nullable=False,
        default="active"
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    sources = relationship(
        "ProgramSource",
        back_populates="program"
    )

    stages = relationship(
        "ProgramStage",
        back_populates="program"
    )

    crops = relationship(
        "Crop",
        back_populates="program"
    )