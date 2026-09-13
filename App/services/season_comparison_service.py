from sqlalchemy.orm import Session

from App.database.models.crop import Crop
from App.database.models.farm import Farm
from App.database.models.cost import Cost
from App.database.models.harvest import Harvest
from App.database.models.sale import Sale


def get_crop_data(
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

    costs = (
        db.query(Cost)
        .filter(
            Cost.crop_id == crop_id
        )
        .all()
    )

    total_cost = sum(
        cost.gharama
        for cost in costs
    )

    harvests = (
        db.query(Harvest)
        .filter(
            Harvest.crop_id == crop_id
        )
        .all()
    )

    total_harvest = sum(
        harvest.kiasi
        for harvest in harvests
    )

    harvest_units = {
        harvest.unit
        for harvest in harvests
    }

    if len(harvest_units) == 1:
        harvest_unit = next(iter(harvest_units))
    elif len(harvest_units) == 0:
        harvest_unit = None
    else:
        harvest_unit = "mchanganyiko"

    harvest_ids = [
        harvest.id
        for harvest in harvests
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

    total_sales = sum(
        sale.kiasi
        for sale in sales
    )

    sale_units = {
        sale.unit
        for sale in sales
    }

    if len(sale_units) == 1:
        sale_unit = next(iter(sale_units))
    elif len(sale_units) == 0:
        sale_unit = None
    else:
        sale_unit = "mchanganyiko"

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
        "msimu": crop.msimu,
        "jumla_ya_gharama": total_cost,
        "jumla_ya_mavuno": total_harvest,
        "unit_ya_mavuno": harvest_unit,
        "jumla_ya_mauzo": total_sales,
        "unit_ya_mauzo": sale_unit,
        "jumla_ya_mapato": total_revenue,
        "faida_au_hasara": profit_loss,
        "hali": hali
    }


def compare_seasons(
    db: Session,
    crop_id_ya_kwanza: int,
    crop_id_ya_pili: int,
    current_farmer_id: int
):
    msimu_wa_kwanza = get_crop_data(
        db=db,
        crop_id=crop_id_ya_kwanza,
        current_farmer_id=current_farmer_id
    )

    msimu_wa_pili = get_crop_data(
        db=db,
        crop_id=crop_id_ya_pili,
        current_farmer_id=current_farmer_id
    )

    if msimu_wa_kwanza is None:
        return None

    if msimu_wa_pili is None:
        return None

    tofauti = {
        "gharama": (
            msimu_wa_pili["jumla_ya_gharama"]
            - msimu_wa_kwanza["jumla_ya_gharama"]
        ),
        "mavuno": (
            msimu_wa_pili["jumla_ya_mavuno"]
            - msimu_wa_kwanza["jumla_ya_mavuno"]
        ),
        "mauzo": (
            msimu_wa_pili["jumla_ya_mauzo"]
            - msimu_wa_kwanza["jumla_ya_mauzo"]
        ),
        "mapato": (
            msimu_wa_pili["jumla_ya_mapato"]
            - msimu_wa_kwanza["jumla_ya_mapato"]
        ),
        "faida_au_hasara": (
            msimu_wa_pili["faida_au_hasara"]
            - msimu_wa_kwanza["faida_au_hasara"]
        )
    }

    if (
        msimu_wa_kwanza["faida_au_hasara"]
        > msimu_wa_pili["faida_au_hasara"]
    ):
        msimu_bora = "msimu_wa_kwanza"

    elif (
        msimu_wa_pili["faida_au_hasara"]
        > msimu_wa_kwanza["faida_au_hasara"]
    ):
        msimu_bora = "msimu_wa_pili"

    else:
        msimu_bora = "sawa"

    return {
        "msimu_wa_kwanza": msimu_wa_kwanza,
        "msimu_wa_pili": msimu_wa_pili,
        "tofauti": tofauti,
        "msimu_bora": msimu_bora
    }