from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from App.database.database import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)

    jina = Column(String, nullable=False)

    maelezo = Column(String, nullable=True)

    tarehe = Column(Date, nullable=False)

    hali = Column(String, nullable=False, default="haijakamilika")

    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)

    crop = relationship("Crop", back_populates="activities")