from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from App.database.database import SessionLocal
from App.database.models.program_rule import ProgramRule
from App.database.models.program_task import ProgramTask
from App.database.models.program_stage import ProgramStage
from App.schemas.program_rule import (
    ProgramRuleCreate,
    ProgramRuleResponse
)


router = APIRouter(
    prefix="/program-rules",
    tags=["Program Rules"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================================
# CREATE PROGRAM RULE
# =========================================================

@router.post(
    "/",
    response_model=ProgramRuleResponse
)
def create_program_rule(
    rule: ProgramRuleCreate,
    db: Session = Depends(get_db)
):
    task = db.query(
        ProgramTask
    ).filter(
        ProgramTask.id == rule.task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Program Task haikupatikana"
        )

    if rule.stage_id is not None:
        stage = db.query(
            ProgramStage
        ).filter(
            ProgramStage.id == rule.stage_id
        ).first()

        if stage is None:
            raise HTTPException(
                status_code=404,
                detail="Program Stage haikupatikana"
            )

    new_rule = ProgramRule(
        task_id=rule.task_id,
        trigger_type=rule.trigger_type,
        offset_value=rule.offset_value,
        offset_unit=rule.offset_unit,
        stage_id=rule.stage_id,
        maelezo=rule.maelezo
    )

    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)

    return new_rule


# =========================================================
# GET ALL PROGRAM RULES
# =========================================================

@router.get(
    "/",
    response_model=list[ProgramRuleResponse]
)
def get_program_rules(
    db: Session = Depends(get_db)
):
    rules = db.query(
        ProgramRule
    ).order_by(
        ProgramRule.id.asc()
    ).all()

    return rules


# =========================================================
# GET SINGLE PROGRAM RULE
# =========================================================

@router.get(
    "/{rule_id}",
    response_model=ProgramRuleResponse
)
def get_program_rule(
    rule_id: int,
    db: Session = Depends(get_db)
):
    rule = db.query(
        ProgramRule
    ).filter(
        ProgramRule.id == rule_id
    ).first()

    if rule is None:
        raise HTTPException(
            status_code=404,
            detail="Program Rule haikupatikana"
        )

    return rule


# =========================================================
# UPDATE PROGRAM RULE
# =========================================================

@router.put(
    "/{rule_id}",
    response_model=ProgramRuleResponse
)
def update_program_rule(
    rule_id: int,
    rule: ProgramRuleCreate,
    db: Session = Depends(get_db)
):
    existing_rule = db.query(
        ProgramRule
    ).filter(
        ProgramRule.id == rule_id
    ).first()

    if existing_rule is None:
        raise HTTPException(
            status_code=404,
            detail="Program Rule haikupatikana"
        )

    task = db.query(
        ProgramTask
    ).filter(
        ProgramTask.id == rule.task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Program Task haikupatikana"
        )

    if rule.stage_id is not None:
        stage = db.query(
            ProgramStage
        ).filter(
            ProgramStage.id == rule.stage_id
        ).first()

        if stage is None:
            raise HTTPException(
                status_code=404,
                detail="Program Stage haikupatikana"
            )

    existing_rule.task_id = rule.task_id
    existing_rule.trigger_type = rule.trigger_type
    existing_rule.offset_value = rule.offset_value
    existing_rule.offset_unit = rule.offset_unit
    existing_rule.stage_id = rule.stage_id
    existing_rule.maelezo = rule.maelezo

    db.commit()
    db.refresh(existing_rule)

    return existing_rule


# =========================================================
# DELETE PROGRAM RULE
# =========================================================

@router.delete(
    "/{rule_id}"
)
def delete_program_rule(
    rule_id: int,
    db: Session = Depends(get_db)
):
    rule = db.query(
        ProgramRule
    ).filter(
        ProgramRule.id == rule_id
    ).first()

    if rule is None:
        raise HTTPException(
            status_code=404,
            detail="Program Rule haikupatikana"
        )

    db.delete(rule)
    db.commit()

    return {
        "ujumbe": "Program Rule imefutwa kikamilifu"
    }