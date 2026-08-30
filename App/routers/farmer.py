from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.farmer import Farmer
from App.schemas.farmer import FarmerCreate

router = APIRouter(
    prefix="/farmers",
    tags=["Farmers"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_farmers(db: Session = Depends(get_db)):
    return db.query(Farmer).all()


@router.post("/")
def create_farmer(farmer: FarmerCreate, db: Session = Depends(get_db)):
    new_farmer = Farmer(
        jina=farmer.jina,
        simu=farmer.simu,
        eneo=farmer.eneo
    )

    db.add(new_farmer)
    db.commit()
    db.refresh(new_farmer)

    return new_farmer
@router.get("/{farmer_id}")
def get_farmer(farmer_id: int, db: Session = Depends(get_db)):
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()

    if farmer is None:
        return {
            "ujumbe": "Mkulima hakupatikana"
        }

    return farmer