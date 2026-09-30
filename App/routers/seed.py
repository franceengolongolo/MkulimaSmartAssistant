from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.seed import Seed
from App.database.models.crop import Crop
from App.database.models.farm import Farm
from App.schemas.seed import SeedCreate
from App.services.auth_service import get_current_farmer


router = APIRouter(
    prefix="/seeds",
    tags=["Seeds"]
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


def get_farmer_seed(
    db: Session,
    seed_id: int,
    current_farmer_id: int
):
    return (
        db.query(Seed)
        .join(Crop, Seed.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Seed.id == seed_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )


@router.get("/")
def get_seeds(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    seeds = (
        db.query(Seed)
        .join(Crop, Seed.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Farm.farmer_id == current_farmer_id
        )
        .order_by(Seed.id.asc())
        .all()
    )

    return seeds


@router.post("/")
def create_seed(
    seed: SeedCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = get_farmer_crop(
        db=db,
        crop_id=seed.crop_id,
        current_farmer_id=current_farmer_id
    )

    if crop is None:
        raise HTTPException(
            status_code=404,
            detail="Zao halikupatikana au si lako"
        )

    new_seed = Seed(
        jina=seed.jina,
        aina=seed.aina,
        kampuni=seed.kampuni,
        kiasi=seed.kiasi,
        unit=seed.unit,
        gharama=seed.gharama,
        crop_id=seed.crop_id
    )

    try:
        db.add(new_seed)
        db.commit()
        db.refresh(new_seed)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Imeshindikana kuhifadhi mbegu"
        )

    return new_seed


@router.get("/crop/{crop_id}")
def get_crop_seeds(
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

    seeds = (
        db.query(Seed)
        .filter(
            Seed.crop_id == crop_id
        )
        .order_by(Seed.id.asc())
        .all()
    )

    return {
        "zao": crop.jina,
        "crop_id": crop.id,
        "seeds": seeds
    }


@router.get("/{seed_id}")
def get_seed(
    seed_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    seed = get_farmer_seed(
        db=db,
        seed_id=seed_id,
        current_farmer_id=current_farmer_id
    )

    if seed is None:
        raise HTTPException(
            status_code=404,
            detail="Mbegu haikupatikana"
        )

    return seed


@router.put("/{seed_id}")
def update_seed(
    seed_id: int,
    seed: SeedCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    existing_seed = get_farmer_seed(
        db=db,
        seed_id=seed_id,
        current_farmer_id=current_farmer_id
    )

    if existing_seed is None:
        raise HTTPException(
            status_code=404,
            detail="Mbegu haikupatikana"
        )

    crop = get_farmer_crop(
        db=db,
        crop_id=seed.crop_id,
        current_farmer_id=current_farmer_id
    )

    if crop is None:
        raise HTTPException(
            status_code=404,
            detail="Zao jipya halikupatikana au si lako"
        )

    existing_seed.jina = seed.jina
    existing_seed.aina = seed.aina
    existing_seed.kampuni = seed.kampuni
    existing_seed.kiasi = seed.kiasi
    existing_seed.unit = seed.unit
    existing_seed.gharama = seed.gharama
    existing_seed.crop_id = seed.crop_id

    try:
        db.commit()
        db.refresh(existing_seed)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Imeshindikana kusasisha mbegu"
        )

    return existing_seed


@router.delete("/{seed_id}")
def delete_seed(
    seed_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    seed = get_farmer_seed(
        db=db,
        seed_id=seed_id,
        current_farmer_id=current_farmer_id
    )

    if seed is None:
        raise HTTPException(
            status_code=404,
            detail="Mbegu haikupatikana"
        )

    try:
        db.delete(seed)
        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Imeshindikana kufuta mbegu"
        )

    return {
        "ujumbe": "Mbegu imefutwa kikamilifu"
    }