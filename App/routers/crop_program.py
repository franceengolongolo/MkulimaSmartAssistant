from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.crop_program import CropProgram
from App.schemas.crop_program import (
    CropProgramCreate,
    CropProgramResponse
)


router = APIRouter(
    prefix="/crop-programs",
    tags=["Crop Programs"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================================
# CREATE CROP PROGRAM
# =========================================================

@router.post(
    "/",
    response_model=CropProgramResponse
)
def create_crop_program(
    program: CropProgramCreate,
    db: Session = Depends(get_db)
):
    new_program = CropProgram(
        jina=program.jina,
        aina_ya_zao=program.aina_ya_zao,
        aina_ya_program=program.aina_ya_program,
        msimu=program.msimu,
        maelezo=program.maelezo,
        version=program.version,
        hali=program.hali
    )

    db.add(new_program)
    db.commit()
    db.refresh(new_program)

    return new_program


# =========================================================
# GET ALL CROP PROGRAMS
# =========================================================

@router.get(
    "/",
    response_model=list[CropProgramResponse]
)
def get_crop_programs(
    db: Session = Depends(get_db)
):
    programs = db.query(
        CropProgram
    ).order_by(
        CropProgram.id.asc()
    ).all()

    return programs


# =========================================================
# GET SINGLE CROP PROGRAM
# =========================================================

@router.get(
    "/{program_id}",
    response_model=CropProgramResponse
)
def get_crop_program(
    program_id: int,
    db: Session = Depends(get_db)
):
    program = db.query(
        CropProgram
    ).filter(
        CropProgram.id == program_id
    ).first()

    if program is None:
        raise HTTPException(
            status_code=404,
            detail="Crop Program haikupatikana"
        )

    return program


# =========================================================
# UPDATE CROP PROGRAM
# =========================================================

@router.put(
    "/{program_id}",
    response_model=CropProgramResponse
)
def update_crop_program(
    program_id: int,
    program: CropProgramCreate,
    db: Session = Depends(get_db)
):
    existing_program = db.query(
        CropProgram
    ).filter(
        CropProgram.id == program_id
    ).first()

    if existing_program is None:
        raise HTTPException(
            status_code=404,
            detail="Crop Program haikupatikana"
        )

    existing_program.jina = program.jina
    existing_program.aina_ya_zao = program.aina_ya_zao
    existing_program.aina_ya_program = program.aina_ya_program
    existing_program.msimu = program.msimu
    existing_program.maelezo = program.maelezo
    existing_program.version = program.version
    existing_program.hali = program.hali

    db.commit()
    db.refresh(existing_program)

    return existing_program


# =========================================================
# DELETE CROP PROGRAM
# =========================================================

@router.delete(
    "/{program_id}"
)
def delete_crop_program(
    program_id: int,
    db: Session = Depends(get_db)
):
    program = db.query(
        CropProgram
    ).filter(
        CropProgram.id == program_id
    ).first()

    if program is None:
        raise HTTPException(
            status_code=404,
            detail="Crop Program haikupatikana"
        )

    db.delete(program)
    db.commit()

    return {
        "ujumbe": "Crop Program imefutwa kikamilifu"
    }