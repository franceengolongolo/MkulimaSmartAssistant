from fastapi import FastAPI

from App.database.models.farmer import Farmer
from App.database.database import Base, engine
from App.routers.farmer import router as farmer_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(farmer_router)


@app.get("/")
def home():
    return {
        "ujumbe": "Karibu kwenye Mkulima Smart Assistant",
        "hali": "Backend inafanya kazi vizuri!"
    }