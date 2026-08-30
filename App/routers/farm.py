from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.farm import Farm
from App.schemas.farm import FarmCreate

router = APIRouter(
    prefix="/farms",
    tags=["Farms"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_farms(db: Session = Depends(get_db)):
    return db.query(Farm).all()


@router.post("/")
def create_farm(farm: FarmCreate, db: Session = Depends(get_db)):
    new_farm = Farm(
        jina=farm.jina,
        eneo=farm.eneo,
        ukubwa=farm.ukubwa,
        farmer_id=farm.farmer_id
    )

    db.add(new_farm)
    db.commit()
    db.refresh(new_farm)

    return new_farm
@router.get("/{farm_id}")
def get_farm(farm_id: int, db: Session = Depends(get_db)):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()

    if farm is None:
        return {
            "ujumbe": "Shamba halikupatikana"
        }

    return farm
@router.put("/{farm_id}")
def update_farm(
    farm_id: int,
    farm: FarmCreate,
    db: Session = Depends(get_db)
):
    existing_farm = db.query(Farm).filter(Farm.id == farm_id).first()

    if existing_farm is None:
        return {
            "ujumbe": "Shamba halikupatikana"
        }

    existing_farm.jina = farm.jina
    existing_farm.eneo = farm.eneo
    existing_farm.ukubwa = farm.ukubwa
    existing_farm.farmer_id = farm.farmer_id

    db.commit()
    db.refresh(existing_farm)

    return existing_farm
@router.delete("/{farm_id}")
def delete_farm(farm_id: int, db: Session = Depends(get_db)):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()

    if farm is None:
        return {
            "ujumbe": "Shamba halikupatikana"
        }

    db.delete(farm)
    db.commit()

    return {
        "ujumbe": "Shamba limefutwa kikamilifu"
    }