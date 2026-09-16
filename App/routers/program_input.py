from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.program_input import ProgramInput
from App.database.models.program_task import ProgramTask
from App.schemas.program_input import (
    ProgramInputCreate,
    ProgramInputResponse
)


router = APIRouter(
    prefix="/program-inputs",
    tags=["Program Inputs"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================================
# CREATE PROGRAM INPUT
# =========================================================

@router.post(
    "/",
    response_model=ProgramInputResponse
)
def create_program_input(
    input_data: ProgramInputCreate,
    db: Session = Depends(get_db)
):
    task = db.query(
        ProgramTask
    ).filter(
        ProgramTask.id == input_data.task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Program Task haikupatikana"
        )

    new_input = ProgramInput(
        task_id=input_data.task_id,
        jina=input_data.jina,
        aina=input_data.aina,
        kiasi=input_data.kiasi,
        unit=input_data.unit,
        njia_ya_matumizi=input_data.njia_ya_matumizi,
        maelezo=input_data.maelezo
    )

    db.add(new_input)
    db.commit()
    db.refresh(new_input)

    return new_input


# =========================================================
# GET ALL PROGRAM INPUTS
# =========================================================

@router.get(
    "/",
    response_model=list[ProgramInputResponse]
)
def get_program_inputs(
    db: Session = Depends(get_db)
):
    inputs = db.query(
        ProgramInput
    ).order_by(
        ProgramInput.id.asc()
    ).all()

    return inputs


# =========================================================
# GET SINGLE PROGRAM INPUT
# =========================================================

@router.get(
    "/{input_id}",
    response_model=ProgramInputResponse
)
def get_program_input(
    input_id: int,
    db: Session = Depends(get_db)
):
    input_data = db.query(
        ProgramInput
    ).filter(
        ProgramInput.id == input_id
    ).first()

    if input_data is None:
        raise HTTPException(
            status_code=404,
            detail="Program Input haikupatikana"
        )

    return input_data


# =========================================================
# UPDATE PROGRAM INPUT
# =========================================================

@router.put(
    "/{input_id}",
    response_model=ProgramInputResponse
)
def update_program_input(
    input_id: int,
    input_data: ProgramInputCreate,
    db: Session = Depends(get_db)
):
    existing_input = db.query(
        ProgramInput
    ).filter(
        ProgramInput.id == input_id
    ).first()

    if existing_input is None:
        raise HTTPException(
            status_code=404,
            detail="Program Input haikupatikana"
        )

    task = db.query(
        ProgramTask
    ).filter(
        ProgramTask.id == input_data.task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Program Task haikupatikana"
        )

    existing_input.task_id = input_data.task_id
    existing_input.jina = input_data.jina
    existing_input.aina = input_data.aina
    existing_input.kiasi = input_data.kiasi
    existing_input.unit = input_data.unit
    existing_input.njia_ya_matumizi = input_data.njia_ya_matumizi
    existing_input.maelezo = input_data.maelezo

    db.commit()
    db.refresh(existing_input)

    return existing_input


# =========================================================
# DELETE PROGRAM INPUT
# =========================================================

@router.delete(
    "/{input_id}"
)
def delete_program_input(
    input_id: int,
    db: Session = Depends(get_db)
):
    input_data = db.query(
        ProgramInput
    ).filter(
        ProgramInput.id == input_id
    ).first()

    if input_data is None:
        raise HTTPException(
            status_code=404,
            detail="Program Input haikupatikana"
        )

    db.delete(input_data)
    db.commit()

    return {
        "ujumbe": "Program Input imefutwa kikamilifu"
    }