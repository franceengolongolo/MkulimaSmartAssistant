from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from App.database.database import Base


class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    jina = Column(String, nullable=False)
    eneo = Column(String, nullable=False)
    ukubwa = Column(Float, nullable=False)

    farmer_id = Column(Integer, ForeignKey("farmers.id"), nullable=False)

    farmer = relationship("Farmer", back_populates="farms")
    crops = relationship("Crop", back_populates="farm")