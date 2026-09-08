from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from App.database.database import Base


class Pesticide(Base):
    __tablename__ = "pesticides"

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

    kampuni = Column(
        String,
        nullable=True
    )

    kiasi = Column(
        Float,
        nullable=False
    )

    unit = Column(
        String,
        nullable=False,
        default="L"
    )

    gharama = Column(
        Float,
        nullable=True
    )

    crop_id = Column(
        Integer,
        ForeignKey("crops.id"),
        nullable=False
    )

    crop = relationship(
        "Crop",
        back_populates="pesticides"
    )