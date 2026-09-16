from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.program_source import ProgramSource
from App.database.models.crop_program import CropProgram
from App.schemas.program_source import (
    ProgramSourceCreate,
    ProgramSourceResponse
)


router = APIRouter(
    prefix="/program-sources",
    tags=["Program Sources"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================================
# CREATE PROGRAM SOURCE
# =========================================================

@router.post(
    "/",
    response_model=ProgramSourceResponse
)
def create_program_source(
    source: ProgramSourceCreate,
    db: Session = Depends(get_db)
):
    program = db.query(
        CropProgram
    ).filter(
        CropProgram.id == source.program_id
    ).first()

    if program is None:
        raise HTTPException(
            status_code=404,
            detail="Crop Program haikupatikana"
        )

    new_source = ProgramSource(
        program_id=source.program_id,
        jina_la_chanzo=source.jina_la_chanzo,
        taasisi=source.taasisi,
        url=source.url,
        tarehe_ya_chanzo=source.tarehe_ya_chanzo,
        maelezo=source.maelezo
    )

    db.add(new_source)
    db.commit()
    db.refresh(new_source)

    return new_source


# =========================================================
# GET ALL PROGRAM SOURCES
# =========================================================

@router.get(
    "/",
    response_model=list[ProgramSourceResponse]
)
def get_program_sources(
    db: Session = Depends(get_db)
):
    sources = db.query(
        ProgramSource
    ).order_by(
        ProgramSource.id.asc()
    ).all()

    return sources


# =========================================================
# GET SINGLE PROGRAM SOURCE
# =========================================================

@router.get(
    "/{source_id}",
    response_model=ProgramSourceResponse
)
def get_program_source(
    source_id: int,
    db: Session = Depends(get_db)
):
    source = db.query(
        ProgramSource
    ).filter(
        ProgramSource.id == source_id
    ).first()

    if source is None:
        raise HTTPException(
            status_code=404,
            detail="Program Source haikupatikana"
        )

    return source


# =========================================================
# UPDATE PROGRAM SOURCE
# =========================================================

@router.put(
    "/{source_id}",
    response_model=ProgramSourceResponse
)
def update_program_source(
    source_id: int,
    source: ProgramSourceCreate,
    db: Session = Depends(get_db)
):
    existing_source = db.query(
        ProgramSource
    ).filter(
        ProgramSource.id == source_id
    ).first()

    if existing_source is None:
        raise HTTPException(
            status_code=404,
            detail="Program Source haikupatikana"
        )

    program = db.query(
        CropProgram
    ).filter(
        CropProgram.id == source.program_id
    ).first()

    if program is None:
        raise HTTPException(
            status_code=404,
            detail="Crop Program haikupatikana"
        )

    existing_source.program_id = source.program_id
    existing_source.jina_la_chanzo = source.jina_la_chanzo
    existing_source.taasisi = source.taasisi
    existing_source.url = source.url
    existing_source.tarehe_ya_chanzo = source.tarehe_ya_chanzo
    existing_source.maelezo = source.maelezo

    db.commit()
    db.refresh(existing_source)

    return existing_source


# =========================================================
# DELETE PROGRAM SOURCE
# =========================================================

@router.delete(
    "/{source_id}"
)
def delete_program_source(
    source_id: int,
    db: Session = Depends(get_db)
):
    source = db.query(
        ProgramSource
    ).filter(
        ProgramSource.id == source_id
    ).first()

    if source is None:
        raise HTTPException(
            status_code=404,
            detail="Program Source haikupatikana"
        )

    db.delete(source)
    db.commit()

    return {
        "ujumbe": "Program Source imefutwa kikamilifu"
    }