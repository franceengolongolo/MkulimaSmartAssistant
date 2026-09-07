from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from App.database.database import Base


class OTPVerification(Base):
    __tablename__ = "otp_verifications"

    id = Column(Integer, primary_key=True, index=True)

    simu = Column(String, nullable=False)

    code = Column(String, nullable=False)

    expires_at = Column(DateTime, nullable=False)

    farmer_id = Column(
        Integer,
        ForeignKey("farmers.id"),
        nullable=False
    )

    farmer = relationship("Farmer")