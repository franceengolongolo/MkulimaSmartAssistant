from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.crop import Crop
from App.schemas.crop import CropCreate

router = APIRouter(
    prefix="/crops",
    tags=["Crops"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_crops(db: Session = Depends(get_db)):
    return db.query(Crop).all()


@router.post("/")
def create_crop(crop: CropCreate, db: Session = Depends(get_db)):
    new_crop = Crop(
        jina=crop.jina,
        aina=crop.aina,
        msimu=crop.msimu,
        farm_id=crop.farm_id
    )

    db.add(new_crop)
    db.commit()
    db.refresh(new_crop)

    return new_crop
@router.get("/{crop_id}")
def get_crop(crop_id: int, db: Session = Depends(get_db)):
    crop = db.query(Crop).filter(Crop.id == crop_id).first()

    if crop is None:
        return {
            "ujumbe": "Zao halikupatikana"
        }

    return crop
@router.put("/{crop_id}")
def update_crop(
    crop_id: int,
    crop: CropCreate,
    db: Session = Depends(get_db)
):
    existing_crop = db.query(Crop).filter(Crop.id == crop_id).first()

    if existing_crop is None:
        return {
            "ujumbe": "Zao halikupatikana"
        }

    existing_crop.jina = crop.jina
    existing_crop.aina = crop.aina
    existing_crop.msimu = crop.msimu
    existing_crop.farm_id = crop.farm_id

    db.commit()
    db.refresh(existing_crop)

    return existing_crop
@router.delete("/{crop_id}")
def delete_crop(crop_id: int, db: Session = Depends(get_db)):
    crop = db.query(Crop).filter(Crop.id == crop_id).first()

    if crop is None:
        return {
            "ujumbe": "Zao halikupatikana"
        }

    db.delete(crop)
    db.commit()

    return {
        "ujumbe": "Zao limefutwa kikamilifu"
    }