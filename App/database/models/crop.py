from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from App.database.database import Base


class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    jina = Column(String, nullable=False)
    aina = Column(String, nullable=False)
    msimu = Column(String, nullable=True)
    tarehe_ya_kupanda = Column(Date, nullable=True)

    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)

    farm = relationship("Farm", back_populates="crops")
    activities = relationship("Activity", back_populates="crop")
    schedules = relationship("Schedule", back_populates="crop")