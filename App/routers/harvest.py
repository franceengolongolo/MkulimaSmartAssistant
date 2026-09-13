from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.harvest import Harvest
from App.database.models.crop import Crop
from App.database.models.farm import Farm
from App.schemas.harvest import HarvestCreate
from App.services.auth_service import get_current_farmer


router = APIRouter(
    prefix="/harvests",
    tags=["Harvests"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_harvests(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    harvests = (
        db.query(Harvest)
        .join(Crop, Harvest.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Farm.farmer_id == current_farmer_id
        )
        .all()
    )

    return harvests


@router.post("/")
def create_harvest(
    harvest: HarvestCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = (
        db.query(Crop)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Crop.id == harvest.crop_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if crop is None:
        return {
            "ujumbe": "Huwezi kuongeza mavuno kwenye zao ambalo si lako"
        }

    new_harvest = Harvest(
        kiasi=harvest.kiasi,
        unit=harvest.unit,
        tarehe=harvest.tarehe,
        maelezo=harvest.maelezo,
        crop_id=harvest.crop_id
    )

    db.add(new_harvest)
    db.commit()
    db.refresh(new_harvest)

    return new_harvest


@router.get("/crop/{crop_id}")
def get_crop_harvests(
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

    harvests = (
        db.query(Harvest)
        .filter(
            Harvest.crop_id == crop_id
        )
        .all()
    )

    return {
        "zao": crop.jina,
        "crop_id": crop.id,
        "mavuno": harvests
    }


@router.get("/{harvest_id}")
def get_harvest(
    harvest_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    harvest = (
        db.query(Harvest)
        .join(Crop, Harvest.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Harvest.id == harvest_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if harvest is None:
        return {
            "ujumbe": "Mavuno hayakupatikana"
        }

    return harvest


@router.put("/{harvest_id}")
def update_harvest(
    harvest_id: int,
    harvest: HarvestCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    existing_harvest = (
        db.query(Harvest)
        .join(Crop, Harvest.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Harvest.id == harvest_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if existing_harvest is None:
        return {
            "ujumbe": "Mavuno hayakupatikana"
        }

    crop = (
        db.query(Crop)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Crop.id == harvest.crop_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if crop is None:
        return {
            "ujumbe": "Huwezi kuhamisha mavuno kwenye zao ambalo si lako"
        }

    existing_harvest.kiasi = harvest.kiasi
    existing_harvest.unit = harvest.unit
    existing_harvest.tarehe = harvest.tarehe
    existing_harvest.maelezo = harvest.maelezo
    existing_harvest.crop_id = harvest.crop_id

    db.commit()
    db.refresh(existing_harvest)

    return existing_harvest


@router.delete("/{harvest_id}")
def delete_harvest(
    harvest_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    harvest = (
        db.query(Harvest)
        .join(Crop, Harvest.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Harvest.id == harvest_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if harvest is None:
        return {
            "ujumbe": "Mavuno hayakupatikana"
        }

    db.delete(harvest)
    db.commit()

    return {
        "ujumbe": "Mavuno yamefutwa kikamilifu"
    }