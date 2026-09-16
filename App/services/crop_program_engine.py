from datetime import timedelta

from sqlalchemy.orm import Session

from App.database.models.crop import Crop
from App.database.models.schedule import Schedule
from App.database.models.reminder import Reminder
from App.database.models.program_stage import ProgramStage
from App.database.models.program_task import ProgramTask
from App.database.models.program_rule import ProgramRule
from App.services.reminder_service import create_reminder_from_schedule


def generate_schedules_from_crop_program(
    db: Session,
    crop_id: int
):
    """
    Generate schedules and reminders for a crop
    using its assigned Crop Program.

    Flow:
        Crop
            -> Crop Program
            -> Program Stages
            -> Program Tasks
            -> Program Rules
            -> Schedule
            -> Reminder
    """

    # =====================================================
    # 1. TAFUTA CROP
    # =====================================================

    crop = (
        db.query(Crop)
        .filter(
            Crop.id == crop_id
        )
        .first()
    )

    if crop is None:
        raise ValueError(
            "Zao halikupatikana"
        )

    # =====================================================
    # 2. HAKIKISHA CROP INA PROGRAM
    # =====================================================

    if crop.program_id is None:
        raise ValueError(
            "Zao hili halijaunganishwa na Crop Program"
        )

    # =====================================================
    # 3. HAKIKISHA TAREHE YA KUPANDA IPO
    # =====================================================

    if crop.tarehe_ya_kupanda is None:
        raise ValueError(
            "Tarehe ya kupanda haijawekwa kwenye zao"
        )

    # =====================================================
    # 4. TAFUTA STAGES ZA PROGRAM
    # =====================================================

    stages = (
        db.query(ProgramStage)
        .filter(
            ProgramStage.program_id == crop.program_id
        )
        .order_by(
            ProgramStage.namba_ya_hatua.asc()
        )
        .all()
    )

    generated_schedules = []

    # =====================================================
    # 5. PITIA STAGES
    # =====================================================

    for stage in stages:

        # =================================================
        # 6. TAFUTA TASKS ZA STAGE
        # =================================================

        tasks = (
            db.query(ProgramTask)
            .filter(
                ProgramTask.stage_id == stage.id
            )
            .order_by(
                ProgramTask.id.asc()
            )
            .all()
        )

        # =================================================
        # 7. PITIA TASKS
        # =================================================

        for task in tasks:

            # =============================================
            # 8. TAFUTA RULES ZA TASK
            # =============================================

            rules = (
                db.query(ProgramRule)
                .filter(
                    ProgramRule.task_id == task.id
                )
                .order_by(
                    ProgramRule.id.asc()
                )
                .all()
            )

            # =============================================
            # 9. PITIA RULES
            # =============================================

            for rule in rules:

                # Kwa sasa Engine hii inashughulikia
                # rule zinazotegemea tarehe ya kupanda.
                if rule.trigger_type != "planting":
                    continue

                if rule.offset_value is None:
                    continue

                if rule.offset_unit is None:
                    continue

                # =========================================
                # 10. HESABU SIKU
                # =========================================

                if rule.offset_unit == "days":
                    siku = rule.offset_value

                elif rule.offset_unit == "weeks":
                    siku = rule.offset_value * 7

                else:
                    continue

                # =========================================
                # 11. TAFUTA SCHEDULE ILIYOPO
                # =========================================

                existing_schedule = (
                    db.query(Schedule)
                    .filter(
                        Schedule.crop_id == crop.id,
                        Schedule.program_task_id == task.id
                    )
                    .first()
                )

                # =========================================
                # 12. KAMA SCHEDULE IPO
                #     HAKIKISHA REMINDER IPO
                # =========================================

                if existing_schedule is not None:

                    existing_reminder = (
                        db.query(Reminder)
                        .filter(
                            Reminder.schedule_id == existing_schedule.id
                        )
                        .first()
                    )

                    if existing_reminder is None:

                        tarehe_reminder = (
                            crop.tarehe_ya_kupanda
                            + timedelta(days=siku)
                        )

                        create_reminder_from_schedule(
                            db=db,
                            ujumbe=existing_schedule.jina,
                            tarehe=tarehe_reminder,
                            crop_id=crop.id,
                            schedule_id=existing_schedule.id
                        )

                    continue

                # =========================================
                # 13. TENGENEZA SCHEDULE MPYA
                # =========================================

                new_schedule = Schedule(
                    jina=task.jina,
                    maelezo=task.maelezo,
                    siku=siku,
                    status="inayofuata",
                    crop_id=crop.id,
                    program_task_id=task.id
                )

                db.add(new_schedule)

                # Schedule ipate ID kwanza
                db.flush()

                # =========================================
                # 14. TENGENEZA REMINDER
                # =========================================

                tarehe_reminder = (
                    crop.tarehe_ya_kupanda
                    + timedelta(days=siku)
                )

                create_reminder_from_schedule(
                    db=db,
                    ujumbe=new_schedule.jina,
                    tarehe=tarehe_reminder,
                    crop_id=crop.id,
                    schedule_id=new_schedule.id
                )

                generated_schedules.append(
                    new_schedule
                )

    # =====================================================
    # 15. COMMIT
    # =====================================================

    db.commit()

    # =====================================================
    # 16. REFRESH RECORDS
    # =====================================================

    for schedule in generated_schedules:
        db.refresh(schedule)

    return generated_schedules