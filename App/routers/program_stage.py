from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.program_stage import ProgramStage
from App.database.models.crop_program import CropProgram
from App.schemas.program_stage import (
    ProgramStageCreate,
    ProgramStageResponse
)


router = APIRouter(
    prefix="/program-stages",
    tags=["Program Stages"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================================
# CREATE PROGRAM STAGE
# =========================================================

@router.post(
    "/",
    response_model=ProgramStageResponse
)
def create_program_stage(
    stage: ProgramStageCreate,
    db: Session = Depends(get_db)
):
    program = db.query(
        CropProgram
    ).filter(
        CropProgram.id == stage.program_id
    ).first()

    if program is None:
        raise HTTPException(
            status_code=404,
            detail="Crop Program haikupatikana"
        )

    new_stage = ProgramStage(
        program_id=stage.program_id,
        jina=stage.jina,
        namba_ya_hatua=stage.namba_ya_hatua,
        maelezo=stage.maelezo
    )

    db.add(new_stage)
    db.commit()
    db.refresh(new_stage)

    return new_stage


# =========================================================
# GET ALL PROGRAM STAGES
# =========================================================

@router.get(
    "/",
    response_model=list[ProgramStageResponse]
)
def get_program_stages(
    db: Session = Depends(get_db)
):
    stages = db.query(
        ProgramStage
    ).order_by(
        ProgramStage.id.asc()
    ).all()

    return stages


# =========================================================
# GET SINGLE PROGRAM STAGE
# =========================================================

@router.get(
    "/{stage_id}",
    response_model=ProgramStageResponse
)
def get_program_stage(
    stage_id: int,
    db: Session = Depends(get_db)
):
    stage = db.query(
        ProgramStage
    ).filter(
        ProgramStage.id == stage_id
    ).first()

    if stage is None:
        raise HTTPException(
            status_code=404,
            detail="Program Stage haikupatikana"
        )

    return stage


# =========================================================
# UPDATE PROGRAM STAGE
# =========================================================

@router.put(
    "/{stage_id}",
    response_model=ProgramStageResponse
)
def update_program_stage(
    stage_id: int,
    stage: ProgramStageCreate,
    db: Session = Depends(get_db)
):
    existing_stage = db.query(
        ProgramStage
    ).filter(
        ProgramStage.id == stage_id
    ).first()

    if existing_stage is None:
        raise HTTPException(
            status_code=404,
            detail="Program Stage haikupatikana"
        )

    program = db.query(
        CropProgram
    ).filter(
        CropProgram.id == stage.program_id
    ).first()

    if program is None:
        raise HTTPException(
            status_code=404,
            detail="Crop Program haikupatikana"
        )

    existing_stage.program_id = stage.program_id
    existing_stage.jina = stage.jina
    existing_stage.namba_ya_hatua = stage.namba_ya_hatua
    existing_stage.maelezo = stage.maelezo

    db.commit()
    db.refresh(existing_stage)

    return existing_stage


# =========================================================
# DELETE PROGRAM STAGE
# =========================================================

@router.delete(
    "/{stage_id}"
)
def delete_program_stage(
    stage_id: int,
    db: Session = Depends(get_db)
):
    stage = db.query(
        ProgramStage
    ).filter(
        ProgramStage.id == stage_id
    ).first()

    if stage is None:
        raise HTTPException(
            status_code=404,
            detail="Program Stage haikupatikana"
        )

    db.delete(stage)
    db.commit()

    return {
        "ujumbe": "Program Stage imefutwa kikamilifu"
    }