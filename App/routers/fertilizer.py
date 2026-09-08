from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.fertilizer import Fertilizer
from App.database.models.crop import Crop
from App.database.models.farm import Farm
from App.schemas.fertilizer import FertilizerCreate
from App.services.auth_service import get_current_farmer


router = APIRouter(
    prefix="/fertilizers",
    tags=["Fertilizers"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================================
# GET ALL FERTILIZERS - FARMER WAKE TU
# =========================================================

@router.get("/")
def get_fertilizers(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    fertilizers = (
        db.query(Fertilizer)
        .join(Crop, Fertilizer.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Farm.farmer_id == current_farmer_id
        )
        .all()
    )

    return fertilizers


# =========================================================
# CREATE FERTILIZER
# =========================================================

@router.post("/")
def create_fertilizer(
    fertilizer: FertilizerCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = (
        db.query(Crop)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Crop.id == fertilizer.crop_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if crop is None:
        return {
            "ujumbe": "Huwezi kuongeza mbolea kwenye zao ambalo si lako"
        }

    new_fertilizer = Fertilizer(
        jina=fertilizer.jina,
        aina=fertilizer.aina,
        kampuni=fertilizer.kampuni,
        kiasi=fertilizer.kiasi,
        unit=fertilizer.unit,
        gharama=fertilizer.gharama,
        crop_id=fertilizer.crop_id
    )

    db.add(new_fertilizer)
    db.commit()
    db.refresh(new_fertilizer)

    return new_fertilizer


# =========================================================
# GET FERTILIZERS ZA CROP FULANI
# =========================================================

@router.get("/crop/{crop_id}")
def get_crop_fertilizers(
    crop_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = (
        db.query(Crop)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Crop.id == crop_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if crop is None:
        return {
            "ujumbe": "Zao halikupatikana"
        }

    fertilizers = (
        db.query(Fertilizer)
        .filter(
            Fertilizer.crop_id == crop_id
        )
        .all()
    )

    return {
        "zao": crop.jina,
        "crop_id": crop.id,
        "fertilizers": fertilizers
    }


# =========================================================
# GET SINGLE FERTILIZER
# =========================================================

@router.get("/{fertilizer_id}")
def get_fertilizer(
    fertilizer_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    fertilizer = (
        db.query(Fertilizer)
        .join(Crop, Fertilizer.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Fertilizer.id == fertilizer_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if fertilizer is None:
        return {
            "ujumbe": "Mbolea haikupatikana"
        }

    return fertilizer


# =========================================================
# UPDATE FERTILIZER
# =========================================================

@router.put("/{fertilizer_id}")
def update_fertilizer(
    fertilizer_id: int,
    fertilizer: FertilizerCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    existing_fertilizer = (
        db.query(Fertilizer)
        .join(Crop, Fertilizer.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Fertilizer.id == fertilizer_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if existing_fertilizer is None:
        return {
            "ujumbe": "Mbolea haikupatikana"
        }

    crop = (
        db.query(Crop)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Crop.id == fertilizer.crop_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if crop is None:
        return {
            "ujumbe": "Huwezi kuhamisha mbolea kwenye zao ambalo si lako"
        }

    existing_fertilizer.jina = fertilizer.jina
    existing_fertilizer.aina = fertilizer.aina
    existing_fertilizer.kampuni = fertilizer.kampuni
    existing_fertilizer.kiasi = fertilizer.kiasi
    existing_fertilizer.unit = fertilizer.unit
    existing_fertilizer.gharama = fertilizer.gharama
    existing_fertilizer.crop_id = fertilizer.crop_id

    db.commit()
    db.refresh(existing_fertilizer)

    return existing_fertilizer


# =========================================================
# DELETE FERTILIZER
# =========================================================

@router.delete("/{fertilizer_id}")
def delete_fertilizer(
    fertilizer_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    fertilizer = (
        db.query(Fertilizer)
        .join(Crop, Fertilizer.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Fertilizer.id == fertilizer_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if fertilizer is None:
        return {
            "ujumbe": "Mbolea haikupatikana"
        }

    db.delete(fertilizer)
    db.commit()

    return {
        "ujumbe": "Mbolea imefutwa kikamilifu"
    }