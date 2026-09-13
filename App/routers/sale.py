from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException

from App.database.database import SessionLocal
from App.database.models.sale import Sale
from App.database.models.harvest import Harvest
from App.database.models.crop import Crop
from App.database.models.farm import Farm
from App.schemas.sale import SaleCreate
from App.services.auth_service import get_current_farmer


router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_sales(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    sales = (
        db.query(Sale)
        .join(Harvest, Sale.harvest_id == Harvest.id)
        .join(Crop, Harvest.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Farm.farmer_id == current_farmer_id
        )
        .all()
    )

    return sales


@router.post("/")
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    harvest = (
        db.query(Harvest)
        .join(Crop, Harvest.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Harvest.id == sale.harvest_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if harvest is None:
        raise HTTPException(
            status_code=404,
            detail="Mavuno hayakupatikana"
        )

    if sale.unit != harvest.unit:
        raise HTTPException(
            status_code=400,
            detail="Unit ya mauzo lazima ifanane na unit ya mavuno"
        )

    sold_quantity = (
        db.query(Sale)
        .filter(
            Sale.harvest_id == sale.harvest_id
        )
        .all()
    )

    total_sold = sum(
        existing_sale.kiasi
        for existing_sale in sold_quantity
    )

    remaining_quantity = harvest.kiasi - total_sold

    if sale.kiasi > remaining_quantity:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Huwezi kuuza kiasi hiki. "
                f"Mavuno yaliyobaki ni {remaining_quantity} {harvest.unit}"
            )
        )

    jumla = sale.kiasi * sale.bei_kwa_unit

    new_sale = Sale(
        kiasi=sale.kiasi,
        unit=sale.unit,
        bei_kwa_unit=sale.bei_kwa_unit,
        jumla=jumla,
        tarehe=sale.tarehe,
        maelezo=sale.maelezo,
        harvest_id=sale.harvest_id
    )

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return new_sale


@router.get("/harvest/{harvest_id}")
def get_harvest_sales(
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
        raise HTTPException(
            status_code=404,
            detail="Mavuno hayakupatikana"
        )

    sales = (
        db.query(Sale)
        .filter(
            Sale.harvest_id == harvest_id
        )
        .all()
    )

    total_sold = sum(
        sale.kiasi
        for sale in sales
    )

    remaining_quantity = harvest.kiasi - total_sold

    total_revenue = sum(
        sale.jumla
        for sale in sales
    )

    return {
        "harvest_id": harvest.id,
        "mavuno": harvest.kiasi,
        "unit": harvest.unit,
        "yaliyouzwa": total_sold,
        "yaliyobaki": remaining_quantity,
        "mapato": total_revenue,
        "mauzo": sales
    }


@router.get("/{sale_id}")
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    sale = (
        db.query(Sale)
        .join(Harvest, Sale.harvest_id == Harvest.id)
        .join(Crop, Harvest.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Sale.id == sale_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if sale is None:
        raise HTTPException(
            status_code=404,
            detail="Mauzo hayakupatikana"
        )

    return sale


@router.put("/{sale_id}")
def update_sale(
    sale_id: int,
    sale: SaleCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    existing_sale = (
        db.query(Sale)
        .join(Harvest, Sale.harvest_id == Harvest.id)
        .join(Crop, Harvest.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Sale.id == sale_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if existing_sale is None:
        raise HTTPException(
            status_code=404,
            detail="Mauzo hayakupatikana"
        )

    harvest = (
        db.query(Harvest)
        .join(Crop, Harvest.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Harvest.id == sale.harvest_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if harvest is None:
        raise HTTPException(
            status_code=404,
            detail="Mavuno hayakupatikana"
        )

    if sale.unit != harvest.unit:
        raise HTTPException(
            status_code=400,
            detail="Unit ya mauzo lazima ifanane na unit ya mavuno"
        )

    other_sales = (
        db.query(Sale)
        .filter(
            Sale.harvest_id == sale.harvest_id,
            Sale.id != sale_id
        )
        .all()
    )

    total_other_sold = sum(
        existing.kiasi
        for existing in other_sales
    )

    remaining_for_update = harvest.kiasi - total_other_sold

    if sale.kiasi > remaining_for_update:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Huwezi kuweka kiasi hiki. "
                f"Kiasi kinachoweza kuuzwa ni "
                f"{remaining_for_update} {harvest.unit}"
            )
        )

    existing_sale.kiasi = sale.kiasi
    existing_sale.unit = sale.unit
    existing_sale.bei_kwa_unit = sale.bei_kwa_unit
    existing_sale.jumla = sale.kiasi * sale.bei_kwa_unit
    existing_sale.tarehe = sale.tarehe
    existing_sale.maelezo = sale.maelezo
    existing_sale.harvest_id = sale.harvest_id

    db.commit()
    db.refresh(existing_sale)

    return existing_sale


@router.delete("/{sale_id}")
def delete_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    sale = (
        db.query(Sale)
        .join(Harvest, Sale.harvest_id == Harvest.id)
        .join(Crop, Harvest.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Sale.id == sale_id,
            Farm.farmer_id == current_farmer_id
        )
        .first()
    )

    if sale is None:
        raise HTTPException(
            status_code=404,
            detail="Mauzo hayakupatikana"
        )

    db.delete(sale)
    db.commit()

    return {
        "ujumbe": "Mauzo yamefutwa kikamilifu"
    }