from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.program_task import ProgramTask
from App.database.models.program_stage import ProgramStage
from App.schemas.program_task import (
    ProgramTaskCreate,
    ProgramTaskResponse
)


router = APIRouter(
    prefix="/program-tasks",
    tags=["Program Tasks"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================================
# CREATE PROGRAM TASK
# =========================================================

@router.post(
    "/",
    response_model=ProgramTaskResponse
)
def create_program_task(
    task: ProgramTaskCreate,
    db: Session = Depends(get_db)
):
    stage = db.query(
        ProgramStage
    ).filter(
        ProgramStage.id == task.stage_id
    ).first()

    if stage is None:
        raise HTTPException(
            status_code=404,
            detail="Program Stage haikupatikana"
        )

    new_task = ProgramTask(
        stage_id=task.stage_id,
        jina=task.jina,
        aina=task.aina,
        maelezo=task.maelezo,
        muhimu=task.muhimu
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# =========================================================
# GET ALL PROGRAM TASKS
# =========================================================

@router.get(
    "/",
    response_model=list[ProgramTaskResponse]
)
def get_program_tasks(
    db: Session = Depends(get_db)
):
    tasks = db.query(
        ProgramTask
    ).order_by(
        ProgramTask.id.asc()
    ).all()

    return tasks


# =========================================================
# GET SINGLE PROGRAM TASK
# =========================================================

@router.get(
    "/{task_id}",
    response_model=ProgramTaskResponse
)
def get_program_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(
        ProgramTask
    ).filter(
        ProgramTask.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Program Task haikupatikana"
        )

    return task


# =========================================================
# UPDATE PROGRAM TASK
# =========================================================

@router.put(
    "/{task_id}",
    response_model=ProgramTaskResponse
)
def update_program_task(
    task_id: int,
    task: ProgramTaskCreate,
    db: Session = Depends(get_db)
):
    existing_task = db.query(
        ProgramTask
    ).filter(
        ProgramTask.id == task_id
    ).first()

    if existing_task is None:
        raise HTTPException(
            status_code=404,
            detail="Program Task haikupatikana"
        )

    stage = db.query(
        ProgramStage
    ).filter(
        ProgramStage.id == task.stage_id
    ).first()

    if stage is None:
        raise HTTPException(
            status_code=404,
            detail="Program Stage haikupatikana"
        )

    existing_task.stage_id = task.stage_id
    existing_task.jina = task.jina
    existing_task.aina = task.aina
    existing_task.maelezo = task.maelezo
    existing_task.muhimu = task.muhimu

    db.commit()
    db.refresh(existing_task)

    return existing_task


# =========================================================
# DELETE PROGRAM TASK
# =========================================================

@router.delete(
    "/{task_id}"
)
def delete_program_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(
        ProgramTask
    ).filter(
        ProgramTask.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Program Task haikupatikana"
        )

    db.delete(task)
    db.commit()

    return {
        "ujumbe": "Program Task imefutwa kikamilifu"
    }