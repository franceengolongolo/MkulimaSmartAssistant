from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.farmer import Farmer
from App.schemas.farmer import FarmerCreate, FarmerUpdate

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
@router.put("/{farmer_id}")
def update_farmer(
    farmer_id: int,
    farmer: FarmerUpdate,
    db: Session = Depends(get_db)
):
    existing_farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()

    if existing_farmer is None:
        return {
            "ujumbe": "Mkulima hakupatikana"
        }

    existing_farmer.jina = farmer.jina
    existing_farmer.simu = farmer.simu
    existing_farmer.eneo = farmer.eneo

    db.commit()
    db.refresh(existing_farmer)

    return existing_farmer
@router.delete("/{farmer_id}")
def delete_farmer(farmer_id: int, db: Session = Depends(get_db)):
    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()

    if farmer is None:
        return {
            "ujumbe": "Mkulima hakupatikana"
        }

    db.delete(farmer)
    db.commit()

    return {
        "ujumbe": "Mkulima amefutwa kikamilifu"
    }