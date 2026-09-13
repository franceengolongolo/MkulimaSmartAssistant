from sqlalchemy.orm import Session

from App.database.models.cost import Cost
from App.database.models.sale import Sale
from App.database.models.harvest import Harvest
from App.database.models.crop import Crop
from App.database.models.farm import Farm


def get_crop_profit_loss(
    db: Session,
    crop_id: int,
    current_farmer_id: int
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
        return None

    total_costs = (
        db.query(Cost)
        .filter(
            Cost.crop_id == crop_id
        )
        .all()
    )

    total_cost = sum(
        cost.gharama
        for cost in total_costs
    )

    total_harvests = (
        db.query(Harvest)
        .filter(
            Harvest.crop_id == crop_id
        )
        .all()
    )

    harvest_ids = [
        harvest.id
        for harvest in total_harvests
    ]

    if harvest_ids:
        sales = (
            db.query(Sale)
            .filter(
                Sale.harvest_id.in_(harvest_ids)
            )
            .all()
        )
    else:
        sales = []

    total_revenue = sum(
        sale.jumla
        for sale in sales
    )

    profit_loss = total_revenue - total_cost

    if profit_loss > 0:
        hali = "faida"

    elif profit_loss < 0:
        hali = "hasara"

    else:
        hali = "sawa"

    return {
        "crop_id": crop.id,
        "zao": crop.jina,
        "jumla_ya_gharama": total_cost,
        "jumla_ya_mapato": total_revenue,
        "faida_au_hasara": profit_loss,
        "hali": hali
    }