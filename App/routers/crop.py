from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta

from App.database.database import SessionLocal
from App.database.models.crop import Crop
from App.database.models.farm import Farm
from App.database.models.schedule import Schedule
from App.database.models.activity import Activity
from App.database.models.reminder import Reminder
from App.schemas.crop import CropCreate
from App.schemas.dashboard import CropDashboard
from App.services.auth_service import get_current_farmer


router = APIRouter(
    prefix="/crops",
    tags=["Crops"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================================
# GET ALL CROPS - FARMER WAKE TU
# =========================================================

@router.get("/")
def get_crops(
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crops = db.query(Crop).join(
        Farm, Crop.farm_id == Farm.id
    ).filter(
        Farm.farmer_id == current_farmer_id
    ).all()

    return crops


# =========================================================
# CREATE CROP - FARMER HAWEZI KUTUMIA FARM YA MTU MWINGINE
# =========================================================

@router.post("/")
def create_crop(
    crop: CropCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    farm = db.query(Farm).filter(
        Farm.id == crop.farm_id,
        Farm.farmer_id == current_farmer_id
    ).first()

    if farm is None:
        return {
            "ujumbe": "Huwezi kuongeza zao kwenye shamba ambalo si lako"
        }

    new_crop = Crop(
        jina=crop.jina,
        aina=crop.aina,
        msimu=crop.msimu,
        farm_id=crop.farm_id,
        tarehe_ya_kupanda=crop.tarehe_ya_kupanda
    )

    db.add(new_crop)
    db.commit()
    db.refresh(new_crop)

    return new_crop


# =========================================================
# GET SINGLE CROP - FARMER WAKE TU
# =========================================================

@router.get("/{crop_id}")
def get_crop(
    crop_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = db.query(Crop).join(
        Farm, Crop.farm_id == Farm.id
    ).filter(
        Crop.id == crop_id,
        Farm.farmer_id == current_farmer_id
    ).first()

    if crop is None:
        return {
            "ujumbe": "Zao halikupatikana"
        }

    return crop


# =========================================================
# GET CROP ACTIVITIES
# =========================================================

@router.get("/{crop_id}/activities")
def get_crop_activities(
    crop_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = db.query(Crop).join(
        Farm, Crop.farm_id == Farm.id
    ).filter(
        Crop.id == crop_id,
        Farm.farmer_id == current_farmer_id
    ).first()

    if crop is None:
        return {
            "ujumbe": "Zao halikupatikana"
        }

    activities = db.query(Activity).filter(
        Activity.crop_id == crop_id
    ).all()

    return {
        "zao": crop.jina,
        "activities": activities
    }


# =========================================================
# GET CROP SCHEDULE
# =========================================================

@router.get("/{crop_id}/schedule")
def get_crop_schedule(
    crop_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = db.query(Crop).join(
        Farm, Crop.farm_id == Farm.id
    ).filter(
        Crop.id == crop_id,
        Farm.farmer_id == current_farmer_id
    ).first()

    if crop is None:
        return {
            "ujumbe": "Zao halikupatikana"
        }

    schedules = db.query(Schedule).filter(
        Schedule.crop_id == crop_id
    ).all()

    ratiba = []

    for schedule in schedules:
        tarehe = None

        if crop.tarehe_ya_kupanda:
            tarehe = crop.tarehe_ya_kupanda + timedelta(
                days=schedule.siku
            )

        if tarehe == date.today():
            status = "leo"
        elif tarehe and tarehe > date.today():
            status = "inayofuata"
        else:
            status = "imepita"

        ratiba.append({
            "jina": schedule.jina,
            "siku": schedule.siku,
            "tarehe": tarehe,
            "status": status,
            "maelezo": schedule.maelezo
        })

    return {
        "zao": crop.jina,
        "tarehe_ya_kupanda": crop.tarehe_ya_kupanda,
        "ratiba": ratiba
    }


# =========================================================
# GET TODAY SCHEDULE
# =========================================================

@router.get("/{crop_id}/schedule/today")
def get_today_schedule(
    crop_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = db.query(Crop).join(
        Farm, Crop.farm_id == Farm.id
    ).filter(
        Crop.id == crop_id,
        Farm.farmer_id == current_farmer_id
    ).first()

    if crop is None:
        return {
            "ujumbe": "Zao halikupatikana"
        }

    if crop.tarehe_ya_kupanda is None:
        return {
            "ujumbe": "Tarehe ya kupanda haijawekwa"
        }

    schedules = db.query(Schedule).filter(
        Schedule.crop_id == crop_id
    ).all()

    leo = date.today()
    ratiba_ya_leo = []

    for schedule in schedules:
        tarehe = crop.tarehe_ya_kupanda + timedelta(
            days=schedule.siku
        )

        if tarehe == leo:
            ratiba_ya_leo.append({
                "jina": schedule.jina,
                "siku": schedule.siku,
                "tarehe": tarehe,
                "status": "leo",
                "maelezo": schedule.maelezo
            })

    return {
        "zao": crop.jina,
        "tarehe_ya_kupanda": crop.tarehe_ya_kupanda,
        "tarehe_ya_leo": leo,
        "ratiba": ratiba_ya_leo
    }


# =========================================================
# GET NEXT SCHEDULE
# =========================================================

@router.get("/{crop_id}/schedule/next")
def get_next_schedule(
    crop_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = db.query(Crop).join(
        Farm, Crop.farm_id == Farm.id
    ).filter(
        Crop.id == crop_id,
        Farm.farmer_id == current_farmer_id
    ).first()

    if crop is None:
        return {
            "ujumbe": "Zao halikupatikana"
        }

    if crop.tarehe_ya_kupanda is None:
        return {
            "ujumbe": "Tarehe ya kupanda haijawekwa"
        }

    schedules = db.query(Schedule).filter(
        Schedule.crop_id == crop_id
    ).all()

    leo = date.today()
    ratiba_zijazo = []

    for schedule in schedules:
        tarehe = crop.tarehe_ya_kupanda + timedelta(
            days=schedule.siku
        )

        if tarehe >= leo and schedule.status != "imekamilika":
            siku_zimebaki = (tarehe - leo).days

            if tarehe == leo:
                status = "leo"
            else:
                status = "inayofuata"

            ratiba_zijazo.append({
                "jina": schedule.jina,
                "siku": schedule.siku,
                "tarehe": tarehe,
                "siku_zimebaki": siku_zimebaki,
                "status": status,
                "maelezo": schedule.maelezo
            })

    if not ratiba_zijazo:
        return {
            "ujumbe": "Hakuna ratiba inayofuata"
        }

    ratiba_zijazo.sort(
        key=lambda x: x["tarehe"]
    )

    return {
        "zao": crop.jina,
        "tarehe_ya_leo": leo,
        "ratiba_inayofuata": ratiba_zijazo[0]
    }


# =========================================================
# GET UPCOMING SCHEDULES
# =========================================================

@router.get("/{crop_id}/upcoming-schedules")
def get_upcoming_schedules(
    crop_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = db.query(Crop).join(
        Farm, Crop.farm_id == Farm.id
    ).filter(
        Crop.id == crop_id,
        Farm.farmer_id == current_farmer_id
    ).first()

    if crop is None:
        return {
            "ujumbe": "Zao halikupatikana"
        }

    if crop.tarehe_ya_kupanda is None:
        return {
            "ujumbe": "Tarehe ya kupanda haijawekwa"
        }

    schedules = db.query(Schedule).filter(
        Schedule.crop_id == crop_id
    ).all()

    leo = date.today()
    ratiba_zijazo = []

    for schedule in schedules:
        tarehe = crop.tarehe_ya_kupanda + timedelta(
            days=schedule.siku
        )

        if tarehe >= leo and schedule.status != "imekamilika":
            siku_zimebaki = (tarehe - leo).days

            if tarehe == leo:
                status = "leo"
            else:
                status = "inayofuata"

            ratiba_zijazo.append({
                "jina": schedule.jina,
                "siku": schedule.siku,
                "tarehe": tarehe,
                "siku_zimebaki": siku_zimebaki,
                "status": status,
                "maelezo": schedule.maelezo
            })

    ratiba_zijazo.sort(
        key=lambda x: x["tarehe"]
    )

    return {
        "zao": crop.jina,
        "tarehe_ya_leo": leo,
        "ratiba": ratiba_zijazo
    }


# =========================================================
# CROP SUMMARY
# =========================================================

@router.get("/{crop_id}/summary")
def get_crop_summary(
    crop_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = db.query(Crop).join(
        Farm, Crop.farm_id == Farm.id
    ).filter(
        Crop.id == crop_id,
        Farm.farmer_id == current_farmer_id
    ).first()

    if crop is None:
        return {
            "ujumbe": "Zao halikupatikana"
        }

    activities = db.query(Activity).filter(
        Activity.crop_id == crop_id
    ).all()

    jumla_ya_activities = len(activities)

    zilizokamilika = len([
        activity for activity in activities
        if activity.hali == "imekamilika"
    ])

    ambazo_hazijakamilika = len([
        activity for activity in activities
        if activity.hali == "haijakamilika"
    ])

    return {
        "zao": crop.jina,
        "aina": crop.aina,
        "msimu": crop.msimu,
        "tarehe_ya_kupanda": crop.tarehe_ya_kupanda,
        "activities": {
            "jumla": jumla_ya_activities,
            "zilizokamilika": zilizokamilika,
            "ambazo_hazijakamilika": ambazo_hazijakamilika
        }
    }


# =========================================================
# CROP DASHBOARD
# =========================================================

@router.get("/{crop_id}/dashboard", response_model=CropDashboard)
def get_crop_dashboard(
    crop_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = db.query(Crop).join(
        Farm, Crop.farm_id == Farm.id
    ).filter(
        Crop.id == crop_id,
        Farm.farmer_id == current_farmer_id
    ).first()

    if crop is None:
        return {
            "ujumbe": "Zao halikupatikana"
        }

    activities = db.query(Activity).filter(
        Activity.crop_id == crop_id
    ).all()

    jumla_ya_activities = len(activities)

    zilizokamilika = len([
        activity for activity in activities
        if activity.hali == "imekamilika"
    ])

    ambazo_hazijakamilika = len([
        activity for activity in activities
        if activity.hali == "haijakamilika"
    ])

    ratiba = db.query(Schedule).filter(
        Schedule.crop_id == crop_id
    ).all()

    reminders = db.query(Reminder).filter(
        Reminder.crop_id == crop_id
    ).all()

    leo = date.today()

    ratiba_zijazo = []

    if crop.tarehe_ya_kupanda:
        for schedule in ratiba:
            tarehe = crop.tarehe_ya_kupanda + timedelta(
                days=schedule.siku
            )

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

    ratiba_zijazo.sort(
        key=lambda x: x["tarehe"]
    )

    return {
        "zao": {
            "jina": crop.jina,
            "aina": crop.aina,
            "msimu": crop.msimu,
            "tarehe_ya_kupanda": crop.tarehe_ya_kupanda
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
        "reminders": reminders
    }


# =========================================================
# UPDATE CROP
# =========================================================

@router.put("/{crop_id}")
def update_crop(
    crop_id: int,
    crop: CropCreate,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    existing_crop = db.query(Crop).join(
        Farm, Crop.farm_id == Farm.id
    ).filter(
        Crop.id == crop_id,
        Farm.farmer_id == current_farmer_id
    ).first()

    if existing_crop is None:
        return {
            "ujumbe": "Zao halikupatikana"
        }

    # Hakikisha Farm mpya ni ya farmer huyu
    farm = db.query(Farm).filter(
        Farm.id == crop.farm_id,
        Farm.farmer_id == current_farmer_id
    ).first()

    if farm is None:
        return {
            "ujumbe": "Huwezi kuhamisha zao kwenye shamba ambalo si lako"
        }

    existing_crop.jina = crop.jina
    existing_crop.aina = crop.aina
    existing_crop.msimu = crop.msimu
    existing_crop.farm_id = crop.farm_id
    existing_crop.tarehe_ya_kupanda = crop.tarehe_ya_kupanda

    db.commit()
    db.refresh(existing_crop)

    return existing_crop


# =========================================================
# DELETE CROP
# =========================================================

@router.delete("/{crop_id}")
def delete_crop(
    crop_id: int,
    db: Session = Depends(get_db),
    current_farmer_id: int = Depends(get_current_farmer)
):
    crop = db.query(Crop).join(
        Farm, Crop.farm_id == Farm.id
    ).filter(
        Crop.id == crop_id,
        Farm.farmer_id == current_farmer_id
    ).first()

    if crop is None:
        return {
            "ujumbe": "Zao halikupatikana"
        }

    db.delete(crop)
    db.commit()

    return {
        "ujumbe": "Zao limefutwa kikamilifu"
    }