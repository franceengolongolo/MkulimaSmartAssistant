from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from App.database.database import Base


class Harvest(Base):
    __tablename__ = "harvests"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    kiasi = Column(
        Float,
        nullable=False
    )

    unit = Column(
        String,
        nullable=False
    )

    tarehe = Column(
        Date,
        nullable=False
    )

    maelezo = Column(
        String,
        nullable=True
    )

    crop_id = Column(
        Integer,
        ForeignKey("crops.id"),
        nullable=False
    )

    crop = relationship(
        "Crop",
        back_populates="harvests"
    )