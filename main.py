from fastapi import FastAPI

# =========================================================
# DATABASE MODELS
# =========================================================

from App.database.models.farmer import Farmer
from App.database.models.farm import Farm
from App.database.models.crop import Crop
from App.database.models.activity import Activity
from App.database.models.schedule import Schedule
from App.database.models.reminder import Reminder
from App.database.models.otp import OTPVerification
from App.database.models.seed import Seed
from App.database.models.fertilizer import Fertilizer
from App.database.models.pesticide import Pesticide
from App.database.models.cost import Cost
from App.database.models.harvest import Harvest
from App.database.models.sale import Sale

from App.database.models.crop_program import CropProgram
from App.database.models.program_source import ProgramSource
from App.database.models.program_stage import ProgramStage
from App.database.models.program_task import ProgramTask
from App.database.models.program_rule import ProgramRule
from App.database.models.program_input import ProgramInput


# =========================================================
# DATABASE
# =========================================================

from App.database.database import Base, engine


# =========================================================
# ROUTERS
# =========================================================

from App.routers.farmer import router as farmer_router
from App.routers.farm import router as farm_router
from App.routers.crop import router as crop_router
from App.routers.activity import router as activity_router
from App.routers.schedule import router as schedule_router
from App.routers.reminder import router as reminder_router
from App.routers.auth import router as auth_router
from App.routers.seed import router as seed_router
from App.routers.fertilizer import router as fertilizer_router
from App.routers.pesticide import router as pesticide_router
from App.routers.cost import router as cost_router
from App.routers.harvest import router as harvest_router
from App.routers.sale import router as sale_router
from App.routers.profit_loss import router as profit_loss_router
from App.routers.pdf import router as pdf_router
from App.routers.season_comparison import router as season_comparison_router

from App.routers.crop_program import router as crop_program_router
from App.routers.program_stage import router as program_stage_router
from App.routers.program_source import router as program_source_router
from App.routers.program_task import router as program_task_router
from App.routers.program_rule import router as program_rule_router
from App.routers.program_input import router as program_input_router


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Mkulima Smart Assistant",
    description="Backend ya Mkulima Smart Assistant",
    version="1.0.0"
)


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# INCLUDE ROUTERS
# =========================================================

app.include_router(farmer_router)
app.include_router(farm_router)
app.include_router(crop_router)
app.include_router(activity_router)
app.include_router(schedule_router)
app.include_router(reminder_router)
app.include_router(auth_router)
app.include_router(seed_router)
app.include_router(fertilizer_router)
app.include_router(pesticide_router)
app.include_router(cost_router)
app.include_router(harvest_router)
app.include_router(sale_router)
app.include_router(profit_loss_router)
app.include_router(pdf_router)
app.include_router(season_comparison_router)

app.include_router(crop_program_router)
app.include_router(program_stage_router)
app.include_router(program_source_router)
app.include_router(program_task_router)
app.include_router(program_rule_router)
app.include_router(program_input_router)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "ujumbe": "Karibu kwenye Mkulima Smart Assistant",
        "hali": "Backend inafanya kazi vizuri!"
    }