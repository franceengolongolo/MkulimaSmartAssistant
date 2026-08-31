from fastapi import FastAPI

from App.database.models.farmer import Farmer
from App.database.models.farm import Farm
from App.database.models.farm import Farm
from App.database.models.crop import Crop
from App.database.models.activity import Activity

from App.database.database import Base, engine

from App.routers.farmer import router as farmer_router
from App.routers.farm import router as farm_router
from App.routers.crop import router as crop_router
from App.routers.activity import router as activity_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(farmer_router)
app.include_router(farm_router)
app.include_router(crop_router)
app.include_router(activity_router)


@app.get("/")
def home():
    return {
        "ujumbe": "Karibu kwenye Mkulima Smart Assistant",
        "hali": "Backend inafanya kazi vizuri!"
    }