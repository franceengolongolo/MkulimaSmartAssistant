from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta

from App.database.database import SessionLocal

from App.database.models.farm import Farm
from App.database.models.schedule import Schedule
from App.database.models.reminder import Reminder

from App.schemas.farm import FarmCreate
from App.schemas.dashboard import FarmDashboard

from App.services.auth_service import get_current_farmer


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


# =========================================================
# GET ALL FARMS - FARMER WAKE TU
# =========================================================

@router.get("/")
def get_farms(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    return db.query(Farm).filter(
        Farm.farmer_id == current_farmer_id
    ).all()


# =========================================================
# CREATE FARM
# =========================================================

@router.post("/")
def create_farm(
    farm: FarmCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    new_farm = Farm(
        jina=farm.jina,
        eneo=farm.eneo,
        ukubwa=farm.ukubwa,
        farmer_id=current_farmer_id
    )

    db.add(new_farm)
    db.commit()
    db.refresh(new_farm)

    return new_farm


# =========================================================
# GET SINGLE FARM
# =========================================================

@router.get("/{farm_id}")
def get_farm(
    farm_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    farm = db.query(Farm).filter(
        Farm.id == farm_id,
        Farm.farmer_id == current_farmer_id
    ).first()

    if farm is None:
        return {
            "ujumbe": "Shamba halikupatikana"
        }

    return farm


# =========================================================
# UPDATE FARM
# =========================================================

@router.put("/{farm_id}")
def update_farm(
    farm_id: int,
    farm: FarmCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    existing_farm = db.query(Farm).filter(
        Farm.id == farm_id,
        Farm.farmer_id == current_farmer_id
    ).first()

    if existing_farm is None:
        return {
            "ujumbe": "Shamba halikupatikana"
        }

    existing_farm.jina = farm.jina
    existing_farm.eneo = farm.eneo
    existing_farm.ukubwa = farm.ukubwa

    db.commit()
    db.refresh(existing_farm)

    return existing_farm


# =========================================================
# DELETE FARM
# =========================================================

@router.delete("/{farm_id}")
def delete_farm(
    farm_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    farm = db.query(Farm).filter(
        Farm.id == farm_id,
        Farm.farmer_id == current_farmer_id
    ).first()

    if farm is None:
        return {
            "ujumbe": "Shamba halikupatikana"
        }

    db.delete(farm)
    db.commit()

    return {
        "ujumbe": "Shamba limefutwa kikamilifu"
    }


# =========================================================
# FARM DASHBOARD
# =========================================================

@router.get("/{farm_id}/dashboard", response_model=FarmDashboard)
def get_farm_dashboard(
    farm_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    # -----------------------------------------------------
    # HAKIKI SHAMBA NI LA FARMER HUYU
    # -----------------------------------------------------

    farm = db.query(Farm).filter(
        Farm.id == farm_id,
        Farm.farmer_id == current_farmer_id
    ).first()

    if farm is None:
        return {
            "ujumbe": "Shamba halikupatikana"
        }

    # -----------------------------------------------------
    # MAZAO
    # -----------------------------------------------------

    crops = farm.crops

    jumla_ya_crops = len(crops)

    crop_list = []

    for crop in crops:
        crop_list.append({
            "jina": crop.jina,
            "aina": crop.aina,
            "msimu": crop.msimu
        })

    # -----------------------------------------------------
    # ACTIVITIES
    # -----------------------------------------------------

    jumla_ya_activities = 0
    zilizokamilika = 0
    ambazo_hazijakamilika = 0

    for crop in crops:
        jumla_ya_activities += len(crop.activities)

        for activity in crop.activities:
            if activity.hali == "imekamilika":
                zilizokamilika += 1

            elif activity.hali == "haijakamilika":
                ambazo_hazijakamilika += 1

    # -----------------------------------------------------
    # RATIBA
    # -----------------------------------------------------

    leo = date.today()

    ratiba_zijazo = []
    ratiba_ya_leo = []

    for crop in crops:

        if crop.tarehe_ya_kupanda is None:
            continue

        schedules = db.query(Schedule).filter(
            Schedule.crop_id == crop.id
        ).all()

        for schedule in schedules:

            tarehe = crop.tarehe_ya_kupanda + timedelta(
                days=schedule.siku
            )

            # -----------------------------
            # RATIBA YA LEO
            # -----------------------------

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

            # -----------------------------
            # RATIBA ZIJAZO
            # -----------------------------

            if (
                tarehe >= leo
                and schedule.status != "imekamilika"
            ):

                siku_zimebaki = (
                    tarehe - leo
                ).days

                ratiba_zijazo.append({
                    "zao": crop.jina,
                    "jina": schedule.jina,
                    "siku": schedule.siku,
                    "tarehe": tarehe,
                    "siku_zimebaki": siku_zimebaki,
                    "status": schedule.status,
                    "maelezo": schedule.maelezo
                })

    # Panga ratiba kuanzia tarehe ya karibu
    ratiba_zijazo.sort(
        key=lambda x: x["tarehe"]
    )

    ratiba_ya_leo.sort(
        key=lambda x: x["jina"]
    )

    # -----------------------------------------------------
    # REMINDERS
    # -----------------------------------------------------

    reminders = []

    for crop in crops:

        crop_reminders = db.query(Reminder).filter(
            Reminder.crop_id == crop.id
        ).all()

        reminders.extend(crop_reminders)

    # -----------------------------------------------------
    # PANGA REMINDERS KWA TAREHE
    # -----------------------------------------------------

    reminders.sort(
        key=lambda x: x.tarehe
    )

    # -----------------------------------------------------
    # FARM DASHBOARD RESPONSE
    # -----------------------------------------------------

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
            "inayofuata": (
                ratiba_zijazo[0]
                if ratiba_zijazo
                else None
            ),
            "zijazo": ratiba_zijazo
        },

        "ratiba_ya_leo": ratiba_ya_leo,

        "reminders": reminders
    }