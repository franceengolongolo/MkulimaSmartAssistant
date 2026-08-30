from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from App.database.database import Base


class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)
    jina = Column(String, nullable=False)
    simu = Column(String, unique=True, nullable=False)
    eneo = Column(String, nullable=True)

    farms = relationship("Farm", back_populates="farmer")