from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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


def get_farmer_sale(
    db: Session,
    sale_id: int,
    current_farmer_id: int
):
    return (
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


def get_total_sold(
    db: Session,
    harvest_id: int,
    exclude_sale_id: int | None = None
):
    query = (
        db.query(Sale)
        .filter(
            Sale.harvest_id == harvest_id
        )
    )

    if exclude_sale_id is not None:
        query = query.filter(
            Sale.id != exclude_sale_id
        )

    sales = query.all()

    return sum(
        sale.kiasi
        for sale in sales
    )


@router.get("/")
def get_sales(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    return (
        db.query(Sale)
        .join(Harvest, Sale.harvest_id == Harvest.id)
        .join(Crop, Harvest.crop_id == Crop.id)
        .join(Farm, Crop.farm_id == Farm.id)
        .filter(
            Farm.farmer_id == current_farmer_id
        )
        .order_by(
            Sale.tarehe.asc(),
            Sale.id.asc()
        )
        .all()
    )


@router.post("/")
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    harvest = get_farmer_harvest(
        db=db,
        harvest_id=sale.harvest_id,
        current_farmer_id=current_farmer_id
    )

    if harvest is None:
        raise HTTPException(
            status_code=404,
            detail="Mavuno hayakupatikana au si yako"
        )

    if sale.unit != harvest.unit:
        raise HTTPException(
            status_code=400,
            detail="Unit ya mauzo lazima ifanane na unit ya mavuno"
        )

    total_sold = get_total_sold(
        db=db,
        harvest_id=sale.harvest_id
    )

    remaining_quantity = harvest.kiasi - total_sold

    if sale.kiasi > remaining_quantity:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Huwezi kuuza kiasi hiki. "
                f"Mavuno yaliyobaki ni "
                f"{remaining_quantity} {harvest.unit}"
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

    try:
        db.add(new_sale)
        db.commit()
        db.refresh(new_sale)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Imeshindikana kuhifadhi mauzo"
        )

    return new_sale


@router.get("/harvest/{harvest_id}")
def get_harvest_sales(
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
            detail="Mavuno hayakupatikana au si yako"
        )

    sales = (
        db.query(Sale)
        .filter(
            Sale.harvest_id == harvest_id
        )
        .order_by(
            Sale.tarehe.asc(),
            Sale.id.asc()
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
    sale = get_farmer_sale(
        db=db,
        sale_id=sale_id,
        current_farmer_id=current_farmer_id
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
    existing_sale = get_farmer_sale(
        db=db,
        sale_id=sale_id,
        current_farmer_id=current_farmer_id
    )

    if existing_sale is None:
        raise HTTPException(
            status_code=404,
            detail="Mauzo hayakupatikana"
        )

    harvest = get_farmer_harvest(
        db=db,
        harvest_id=sale.harvest_id,
        current_farmer_id=current_farmer_id
    )

    if harvest is None:
        raise HTTPException(
            status_code=404,
            detail="Mavuno hayakupatikana au si yako"
        )

    if sale.unit != harvest.unit:
        raise HTTPException(
            status_code=400,
            detail="Unit ya mauzo lazima ifanane na unit ya mavuno"
        )

    total_other_sold = get_total_sold(
        db=db,
        harvest_id=sale.harvest_id,
        exclude_sale_id=sale_id
    )

    remaining_quantity = harvest.kiasi - total_other_sold

    if sale.kiasi > remaining_quantity:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Huwezi kuweka kiasi hiki. "
                f"Kiasi kinachoweza kuuzwa ni "
                f"{remaining_quantity} {harvest.unit}"
            )
        )

    existing_sale.kiasi = sale.kiasi
    existing_sale.unit = sale.unit
    existing_sale.bei_kwa_unit = sale.bei_kwa_unit
    existing_sale.jumla = sale.kiasi * sale.bei_kwa_unit
    existing_sale.tarehe = sale.tarehe
    existing_sale.maelezo = sale.maelezo
    existing_sale.harvest_id = sale.harvest_id

    try:
        db.commit()
        db.refresh(existing_sale)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Imeshindikana kusasisha mauzo"
        )

    return existing_sale


@router.delete("/{sale_id}")
def delete_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    sale = get_farmer_sale(
        db=db,
        sale_id=sale_id,
        current_farmer_id=current_farmer_id
    )

    if sale is None:
        raise HTTPException(
            status_code=404,
            detail="Mauzo hayakupatikana"
        )

    try:
        db.delete(sale)
        db.commit()

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Imeshindikana kufuta mauzo"
        )

    return {
        "ujumbe": "Mauzo yamefutwa kikamilifu"
    }