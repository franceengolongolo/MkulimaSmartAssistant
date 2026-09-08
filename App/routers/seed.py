from fastapi import APIRouter, Depends
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


# =========================================================
# GET ALL SEEDS - FARMER WAKE TU
# =========================================================

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
        .all()
    )

    return seeds


# =========================================================
# CREATE SEED - FARMER HAWEZI KUTUMIA CROP YA MTU MWINGINE
# =========================================================

@router.post("/")
def create_seed(
    seed: SeedCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = (
        db.query(Crop)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Crop.id == seed.crop_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if crop is None:
        return {
            "ujumbe": "Huwezi kuongeza mbegu kwenye zao ambalo si lako"
        }

    new_seed = Seed(
        jina=seed.jina,
        aina=seed.aina,
        kampuni=seed.kampuni,
        kiasi=seed.kiasi,
        unit=seed.unit,
        gharama=seed.gharama,
        crop_id=seed.crop_id
    )

    db.add(new_seed)
    db.commit()
    db.refresh(new_seed)

    return new_seed


# =========================================================
# GET SEEDS ZA CROP FULANI
# =========================================================

@router.get("/crop/{crop_id}")
def get_crop_seeds(
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

    seeds = (
        db.query(Seed)
        .filter(
            Seed.crop_id == crop_id
        )
        .all()
    )

    return {
        "zao": crop.jina,
        "crop_id": crop.id,
        "seeds": seeds
    }


# =========================================================
# GET SINGLE SEED - FARMER WAKE TU
# =========================================================

@router.get("/{seed_id}")
def get_seed(
    seed_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    seed = (
        db.query(Seed)
        .join(Crop, Seed.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Seed.id == seed_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if seed is None:
        return {
            "ujumbe": "Mbegu haikupatikana"
        }

    return seed


# =========================================================
# UPDATE SEED
# =========================================================

@router.put("/{seed_id}")
def update_seed(
    seed_id: int,
    seed: SeedCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    existing_seed = (
        db.query(Seed)
        .join(Crop, Seed.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Seed.id == seed_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if existing_seed is None:
        return {
            "ujumbe": "Mbegu haikupatikana"
        }

    # Hakikisha crop mpya ni ya farmer huyu
    crop = (
        db.query(Crop)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Crop.id == seed.crop_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if crop is None:
        return {
            "ujumbe": "Huwezi kuhamisha mbegu kwenye zao ambalo si lako"
        }

    existing_seed.jina = seed.jina
    existing_seed.aina = seed.aina
    existing_seed.kampuni = seed.kampuni
    existing_seed.kiasi = seed.kiasi
    existing_seed.unit = seed.unit
    existing_seed.gharama = seed.gharama
    existing_seed.crop_id = seed.crop_id

    db.commit()
    db.refresh(existing_seed)

    return existing_seed


# =========================================================
# DELETE SEED
# =========================================================

@router.delete("/{seed_id}")
def delete_seed(
    seed_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    seed = (
        db.query(Seed)
        .join(Crop, Seed.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Seed.id == seed_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if seed is None:
        return {
            "ujumbe": "Mbegu haikupatikana"
        }

    db.delete(seed)
    db.commit()

    return {
        "ujumbe": "Mbegu imefutwa kikamilifu"
    }