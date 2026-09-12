from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from App.database.database import Base


class Cost(Base):
    __tablename__ = "costs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
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
        Float,
        nullable=True
    )

    unit = Column(
        String,
        nullable=True
    )

    gharama = Column(
        Float,
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
        back_populates="costs"
    )