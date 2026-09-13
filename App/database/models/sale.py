from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from App.database.database import Base


class Sale(Base):
    __tablename__ = "sales"

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

    bei_kwa_unit = Column(
        Float,
        nullable=False
    )

    jumla = Column(
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

    harvest_id = Column(
        Integer,
        ForeignKey("harvests.id"),
        nullable=False
    )

    harvest = relationship(
        "Harvest",
        back_populates="sales"
    )