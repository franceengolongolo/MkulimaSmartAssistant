from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.farm import Farm
from App.schemas.farm import FarmCreate
from App.schemas.dashboard import FarmDashboard
from datetime import date, timedelta
from App.database.models.schedule import Schedule

router = APIRouter(
    prefix="/farms",
    tags=["Farms"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_farms(db: Session = Depends(get_db)):
    return db.query(Farm).all()


@router.post("/")
def create_farm(farm: FarmCreate, db: Session = Depends(get_db)):
    new_farm = Farm(
        jina=farm.jina,
        eneo=farm.eneo,
        ukubwa=farm.ukubwa,
        farmer_id=farm.farmer_id
    )

    db.add(new_farm)
    db.commit()
    db.refresh(new_farm)

    return new_farm
@router.get("/{farm_id}")
def get_farm(farm_id: int, db: Session = Depends(get_db)):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()

    if farm is None:
        return {
            "ujumbe": "Shamba halikupatikana"
        }

    return farm
@router.put("/{farm_id}")
def update_farm(
    farm_id: int,
    farm: FarmCreate,
    db: Session = Depends(get_db)
):
    existing_farm = db.query(Farm).filter(Farm.id == farm_id).first()

    if existing_farm is None:
        return {
            "ujumbe": "Shamba halikupatikana"
        }

    existing_farm.jina = farm.jina
    existing_farm.eneo = farm.eneo
    existing_farm.ukubwa = farm.ukubwa
    existing_farm.farmer_id = farm.farmer_id

    db.commit()
    db.refresh(existing_farm)

    return existing_farm
@router.delete("/{farm_id}")
def delete_farm(farm_id: int, db: Session = Depends(get_db)):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()

    if farm is None:
        return {
            "ujumbe": "Shamba halikupatikana"
        }

    db.delete(farm)
    db.commit()

    return {
        "ujumbe": "Shamba limefutwa kikamilifu"
    }
@router.get("/{farm_id}/dashboard", response_model=FarmDashboard)
def get_farm_dashboard(farm_id: int, db: Session = Depends(get_db)):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()

    if farm is None:
        return {
            "ujumbe": "Shamba halikupatikana"
        }

    crops = farm.crops

    jumla_ya_crops = len(crops)

    crop_list = [
        {
            "jina": crop.jina,
            "aina": crop.aina,
            "msimu": crop.msimu
        }
        for crop in crops
    ]

    jumla_ya_activities = sum(
        len(crop.activities)
        for crop in crops
    )

    zilizokamilika = sum(
        len([
            activity
            for activity in crop.activities
            if activity.hali == "imekamilika"
        ])
        for crop in crops
    )

    ambazo_hazijakamilika = sum(
        len([
            activity
            for activity in crop.activities
            if activity.hali == "haijakamilika"
        ])
        for crop in crops
    )
    leo = date.today()
    ratiba_zijazo = []
    ratiba_ya_leo = []

    for crop in crops:
        if crop.tarehe_ya_kupanda:
            schedules = db.query(Schedule).filter(
                Schedule.crop_id == crop.id
            ).all()

            for schedule in schedules:
                tarehe = crop.tarehe_ya_kupanda + timedelta(
                    days=schedule.siku
                )

                if tarehe == leo:
                    ratiba_ya_leo.append({
                        "zao": crop.jina,
                        "jina": schedule.jina,
                        "siku": schedule.siku,
                        "tarehe": tarehe,
                        "siku_zimebaki": 0,
                        "status": schedule.status,
                        "maelezo": schedule.maelezo
                    })

                if tarehe >= leo and schedule.status != "imekamilika":
                    siku_zimebaki = (tarehe - leo).days

                    ratiba_zijazo.append({
                        "zao": crop.jina,
                        "jina": schedule.jina,
                        "siku": schedule.siku,
                        "tarehe": tarehe,
                        "siku_zimebaki": siku_zimebaki,
                        "status": schedule.status,
                        "maelezo": schedule.maelezo
                    })
    ratiba_zijazo.sort(key=lambda x: x["tarehe"])
    return {
        "shamba": {
            "jina": farm.jina,
            "eneo": farm.eneo,
            "ukubwa": farm.ukubwa
        },
        "mazao": {
            "jumla": jumla_ya_crops,
            "orodha": crop_list
        },
        "activities": {
            "jumla": jumla_ya_activities,
            "zilizokamilika": zilizokamilika,
            "ambazo_hazijakamilika": ambazo_hazijakamilika
        },
                "ratiba": {
            "inayofuata": ratiba_zijazo[0] if ratiba_zijazo else None,
            "zijazo": ratiba_zijazo
        },
        "ratiba_ya_leo": ratiba_ya_leo
    }