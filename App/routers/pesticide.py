from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.pesticide import Pesticide
from App.database.models.crop import Crop
from App.database.models.farm import Farm
from App.schemas.pesticide import PesticideCreate
from App.services.auth_service import get_current_farmer


router = APIRouter(
    prefix="/pesticides",
    tags=["Pesticides"]
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


def get_farmer_pesticide(
    db: Session,
    pesticide_id: int,
    current_farmer_id: int
):
    return (
        db.query(Pesticide)
        .join(Crop, Pesticide.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Pesticide.id == pesticide_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )


@router.get("/")
def get_pesticides(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    pesticides = (
        db.query(Pesticide)
        .join(Crop, Pesticide.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Farm.farmer_id == current_farmer_id
        )
        .order_by(Pesticide.id.asc())
        .all()
    )

    return pesticides


@router.post("/")
def create_pesticide(
    pesticide: PesticideCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = get_farmer_crop(
        db=db,
        crop_id=pesticide.crop_id,
        current_farmer_id=current_farmer_id
    )

    if crop is None:
        raise HTTPException(
            status_code=404,
            detail="Zao halikupatikana au si lako"
        )

    new_pesticide = Pesticide(
        jina=pesticide.jina,
        aina=pesticide.aina,
        kampuni=pesticide.kampuni,
        kiasi=pesticide.kiasi,
        unit=pesticide.unit,
        gharama=pesticide.gharama,
        crop_id=pesticide.crop_id
    )

    try:
        db.add(new_pesticide)
        db.commit()
        db.refresh(new_pesticide)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Imeshindikana kuhifadhi dawa"
        )

    return new_pesticide


@router.get("/crop/{crop_id}")
def get_crop_pesticides(
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

    pesticides = (
        db.query(Pesticide)
        .filter(
            Pesticide.crop_id == crop_id
        )
        .order_by(Pesticide.id.asc())
        .all()
    )

    return {
        "zao": crop.jina,
        "crop_id": crop.id,
        "pesticides": pesticides
    }


@router.get("/{pesticide_id}")
def get_pesticide(
    pesticide_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    pesticide = get_farmer_pesticide(
        db=db,
        pesticide_id=pesticide_id,
        current_farmer_id=current_farmer_id
    )

    if pesticide is None:
        raise HTTPException(
            status_code=404,
            detail="Dawa haikupatikana"
        )

    return pesticide


@router.put("/{pesticide_id}")
def update_pesticide(
    pesticide_id: int,
    pesticide: PesticideCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    existing_pesticide = get_farmer_pesticide(
        db=db,
        pesticide_id=pesticide_id,
        current_farmer_id=current_farmer_id
    )

    if existing_pesticide is None:
        raise HTTPException(
            status_code=404,
            detail="Dawa haikupatikana"
        )

    crop = get_farmer_crop(
        db=db,
        crop_id=pesticide.crop_id,
        current_farmer_id=current_farmer_id
    )

    if crop is None:
        raise HTTPException(
            status_code=404,
            detail="Zao jipya halikupatikana au si lako"
        )

    existing_pesticide.jina = pesticide.jina
    existing_pesticide.aina = pesticide.aina
    existing_pesticide.kampuni = pesticide.kampuni
    existing_pesticide.kiasi = pesticide.kiasi
    existing_pesticide.unit = pesticide.unit
    existing_pesticide.gharama = pesticide.gharama
    existing_pesticide.crop_id = pesticide.crop_id

    try:
        db.commit()
        db.refresh(existing_pesticide)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Imeshindikana kusasisha dawa"
        )

    return existing_pesticide


@router.delete("/{pesticide_id}")
def delete_pesticide(
    pesticide_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    pesticide = get_farmer_pesticide(
        db=db,
        pesticide_id=pesticide_id,
        current_farmer_id=current_farmer_id
    )

    if pesticide is None:
        raise HTTPException(
            status_code=404,
            detail="Dawa haikupatikana"
        )

    try:
        db.delete(pesticide)
        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Imeshindikana kufuta dawa"
        )

    return {
        "ujumbe": "Dawa imefutwa kikamilifu"
    }