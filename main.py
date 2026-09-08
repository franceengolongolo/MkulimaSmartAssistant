from fastapi import FastAPI

from App.database.models.farmer import Farmer
from App.database.models.farm import Farm
from App.database.models.crop import Crop
from App.database.models.activity import Activity
from App.database.models.schedule import Schedule
from App.database.models.reminder import Reminder
from App.database.models.otp import OTPVerification
from App.database.models.seed import Seed
from App.database.models.fertilizer import Fertilizer

from App.database.database import Base, engine

from App.routers.farmer import router as farmer_router
from App.routers.farm import router as farm_router
from App.routers.crop import router as crop_router
from App.routers.activity import router as activity_router
from App.routers.schedule import router as schedule_router
from App.routers.reminder import router as reminder_router
from App.routers.auth import router as auth_router
from App.routers.seed import router as seed_router
from App.routers.fertilizer import router as fertilizer_router


app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(farmer_router)

app.include_router(farm_router)

app.include_router(crop_router)

app.include_router(activity_router)

app.include_router(schedule_router)

app.include_router(reminder_router)

app.include_router(auth_router)

app.include_router(seed_router)

app.include_router(fertilizer_router)


@app.get("/")
def home():

    return {
        "ujumbe": "Karibu kwenye Mkulima Smart Assistant",
        "hali": "Backend inafanya kazi vizuri!"
    }