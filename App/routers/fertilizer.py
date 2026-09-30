from fastapi import APIRouter, Depends, HTTPException
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


def get_farmer_crop(
    db: Session,
    crop_id: int,
    current_farmer_id: int
):
    return (
        db.query(Crop)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Crop.id == crop_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )


def get_farmer_fertilizer(
    db: Session,
    fertilizer_id: int,
    current_farmer_id: int
):
    return (
        db.query(Fertilizer)
        .join(Crop, Fertilizer.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Fertilizer.id == fertilizer_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )


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
        .order_by(Fertilizer.id.asc())
        .all()
    )

    return fertilizers


@router.post("/")
def create_fertilizer(
    fertilizer: FertilizerCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = get_farmer_crop(
        db=db,
        crop_id=fertilizer.crop_id,
        current_farmer_id=current_farmer_id
    )

    if crop is None:
        raise HTTPException(
            status_code=404,
            detail="Zao halikupatikana au si lako"
        )

    new_fertilizer = Fertilizer(
        jina=fertilizer.jina,
        aina=fertilizer.aina,
        kampuni=fertilizer.kampuni,
        kiasi=fertilizer.kiasi,
        unit=fertilizer.unit,
        gharama=fertilizer.gharama,
        crop_id=fertilizer.crop_id
    )

    try:
        db.add(new_fertilizer)
        db.commit()
        db.refresh(new_fertilizer)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Imeshindikana kuhifadhi mbolea"
        )

    return new_fertilizer


@router.get("/crop/{crop_id}")
def get_crop_fertilizers(
    crop_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = get_farmer_crop(
        db=db,
        crop_id=crop_id,
        current_farmer_id=current_farmer_id
    )

    if crop is None:
        raise HTTPException(
            status_code=404,
            detail="Zao halikupatikana au si lako"
        )

    fertilizers = (
        db.query(Fertilizer)
        .filter(
            Fertilizer.crop_id == crop_id
        )
        .order_by(Fertilizer.id.asc())
        .all()
    )

    return {
        "zao": crop.jina,
        "crop_id": crop.id,
        "fertilizers": fertilizers
    }


@router.get("/{fertilizer_id}")
def get_fertilizer(
    fertilizer_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    fertilizer = get_farmer_fertilizer(
        db=db,
        fertilizer_id=fertilizer_id,
        current_farmer_id=current_farmer_id
    )

    if fertilizer is None:
        raise HTTPException(
            status_code=404,
            detail="Mbolea haikupatikana"
        )

    return fertilizer


@router.put("/{fertilizer_id}")
def update_fertilizer(
    fertilizer_id: int,
    fertilizer: FertilizerCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    existing_fertilizer = get_farmer_fertilizer(
        db=db,
        fertilizer_id=fertilizer_id,
        current_farmer_id=current_farmer_id
    )

    if existing_fertilizer is None:
        raise HTTPException(
            status_code=404,
            detail="Mbolea haikupatikana"
        )

    crop = get_farmer_crop(
        db=db,
        crop_id=fertilizer.crop_id,
        current_farmer_id=current_farmer_id
    )

    if crop is None:
        raise HTTPException(
            status_code=404,
            detail="Zao jipya halikupatikana au si lako"
        )

    existing_fertilizer.jina = fertilizer.jina
    existing_fertilizer.aina = fertilizer.aina
    existing_fertilizer.kampuni = fertilizer.kampuni
    existing_fertilizer.kiasi = fertilizer.kiasi
    existing_fertilizer.unit = fertilizer.unit
    existing_fertilizer.gharama = fertilizer.gharama
    existing_fertilizer.crop_id = fertilizer.crop_id

    try:
        db.commit()
        db.refresh(existing_fertilizer)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Imeshindikana kusasisha mbolea"
        )

    return existing_fertilizer


@router.delete("/{fertilizer_id}")
def delete_fertilizer(
    fertilizer_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    fertilizer = get_farmer_fertilizer(
        db=db,
        fertilizer_id=fertilizer_id,
        current_farmer_id=current_farmer_id
    )

    if fertilizer is None:
        raise HTTPException(
            status_code=404,
            detail="Mbolea haikupatikana"
        )

    try:
        db.delete(fertilizer)
        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Imeshindikana kufuta mbolea"
        )

    return {
        "ujumbe": "Mbolea imefutwa kikamilifu"
    }