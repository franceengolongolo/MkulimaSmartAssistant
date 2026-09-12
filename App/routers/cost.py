from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.cost import Cost
from App.database.models.crop import Crop
from App.database.models.farm import Farm
from App.schemas.cost import CostCreate
from App.services.auth_service import get_current_farmer


router = APIRouter(
    prefix="/costs",
    tags=["Costs"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_costs(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    costs = (
        db.query(Cost)
        .join(Crop, Cost.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Farm.farmer_id == current_farmer_id
        )
        .all()
    )

    return costs


@router.post("/")
def create_cost(
    cost: CostCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = (
        db.query(Crop)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Crop.id == cost.crop_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if crop is None:
        return {
            "ujumbe": "Huwezi kuongeza gharama kwenye zao ambalo si lako"
        }

    new_cost = Cost(
        jina=cost.jina,
        aina=cost.aina,
        kiasi=cost.kiasi,
        unit=cost.unit,
        gharama=cost.gharama,
        tarehe=cost.tarehe,
        maelezo=cost.maelezo,
        crop_id=cost.crop_id
    )

    db.add(new_cost)
    db.commit()
    db.refresh(new_cost)

    return new_cost


@router.get("/crop/{crop_id}")
def get_crop_costs(
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

    costs = (
        db.query(Cost)
        .filter(
            Cost.crop_id == crop_id
        )
        .all()
    )

    return {
        "zao": crop.jina,
        "crop_id": crop.id,
        "gharama": costs
    }


@router.get("/{cost_id}")
def get_cost(
    cost_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    cost = (
        db.query(Cost)
        .join(Crop, Cost.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Cost.id == cost_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if cost is None:
        return {
            "ujumbe": "Gharama haikupatikana"
        }

    return cost


@router.put("/{cost_id}")
def update_cost(
    cost_id: int,
    cost: CostCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    existing_cost = (
        db.query(Cost)
        .join(Crop, Cost.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Cost.id == cost_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if existing_cost is None:
        return {
            "ujumbe": "Gharama haikupatikana"
        }

    crop = (
        db.query(Crop)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Crop.id == cost.crop_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if crop is None:
        return {
            "ujumbe": "Huwezi kuhamisha gharama kwenye zao ambalo si lako"
        }

    existing_cost.jina = cost.jina
    existing_cost.aina = cost.aina
    existing_cost.kiasi = cost.kiasi
    existing_cost.unit = cost.unit
    existing_cost.gharama = cost.gharama
    existing_cost.tarehe = cost.tarehe
    existing_cost.maelezo = cost.maelezo
    existing_cost.crop_id = cost.crop_id

    db.commit()
    db.refresh(existing_cost)

    return existing_cost


@router.delete("/{cost_id}")
def delete_cost(
    cost_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    cost = (
        db.query(Cost)
        .join(Crop, Cost.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Cost.id == cost_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if cost is None:
        return {
            "ujumbe": "Gharama haikupatikana"
        }

    db.delete(cost)
    db.commit()

    return {
        "ujumbe": "Gharama imefutwa kikamilifu"
    }