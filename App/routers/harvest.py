from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.harvest import Harvest
from App.database.models.sale import Sale
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


def get_farmer_harvest(
    db: Session,
    harvest_id: int,
    current_farmer_id: int
):
    return (
        db.query(Harvest)
        .join(Crop, Harvest.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Harvest.id == harvest_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )


@router.get("/")
def get_harvests(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    return (
        db.query(Harvest)
        .join(Crop, Harvest.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Farm.farmer_id == current_farmer_id
        )
        .order_by(
            Harvest.tarehe.asc(),
            Harvest.id.asc()
        )
        .all()
    )


@router.post("/")
def create_harvest(
    harvest: HarvestCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = get_farmer_crop(
        db=db,
        crop_id=harvest.crop_id,
        current_farmer_id=current_farmer_id
    )

    if crop is None:
        raise HTTPException(
            status_code=404,
            detail="Huwezi kuongeza mavuno kwenye zao ambalo si lako"
        )

    new_harvest = Harvest(
        kiasi=harvest.kiasi,
        unit=harvest.unit,
        tarehe=harvest.tarehe,
        maelezo=harvest.maelezo,
        crop_id=harvest.crop_id
    )

    try:
        db.add(new_harvest)
        db.commit()
        db.refresh(new_harvest)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Imeshindikana kuhifadhi mavuno"
        )

    return new_harvest


@router.get("/crop/{crop_id}")
def get_crop_harvests(
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

    harvests = (
        db.query(Harvest)
        .filter(
            Harvest.crop_id == crop_id
        )
        .order_by(
            Harvest.tarehe.asc(),
            Harvest.id.asc()
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
    harvest = get_farmer_harvest(
        db=db,
        harvest_id=harvest_id,
        current_farmer_id=current_farmer_id
    )

    if harvest is None:
        raise HTTPException(
            status_code=404,
            detail="Mavuno hayakupatikana"
        )

    return harvest


@router.put("/{harvest_id}")
def update_harvest(
    harvest_id: int,
    harvest: HarvestCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    existing_harvest = get_farmer_harvest(
        db=db,
        harvest_id=harvest_id,
        current_farmer_id=current_farmer_id
    )

    if existing_harvest is None:
        raise HTTPException(
            status_code=404,
            detail="Mavuno hayakupatikana"
        )

    crop = get_farmer_crop(
        db=db,
        crop_id=harvest.crop_id,
        current_farmer_id=current_farmer_id
    )

    if crop is None:
        raise HTTPException(
            status_code=404,
            detail="Huwezi kuhamisha mavuno kwenye zao ambalo si lako"
        )

    existing_harvest.kiasi = harvest.kiasi
    existing_harvest.unit = harvest.unit
    existing_harvest.tarehe = harvest.tarehe
    existing_harvest.maelezo = harvest.maelezo
    existing_harvest.crop_id = harvest.crop_id

    try:
        db.commit()
        db.refresh(existing_harvest)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Imeshindikana kusasisha mavuno"
        )

    return existing_harvest


@router.delete("/{harvest_id}")
def delete_harvest(
    harvest_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    harvest = get_farmer_harvest(
        db=db,
        harvest_id=harvest_id,
        current_farmer_id=current_farmer_id
    )

    if harvest is None:
        raise HTTPException(
            status_code=404,
            detail="Mavuno hayakupatikana"
        )

    sales_count = (
        db.query(Sale)
        .filter(
            Sale.harvest_id == harvest.id
        )
        .count()
    )

    if sales_count > 0:
        raise HTTPException(
            status_code=409,
            detail=(
                "Mavuno hayawezi kufutwa kwa sababu yana "
                f"mauzo {sales_count} yanayohusiana nayo"
            )
        )

    try:
        db.delete(harvest)
        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Imeshindikana kufuta mavuno"
        )

    return {
        "ujumbe": "Mavuno yamefutwa kikamilifu"
    }