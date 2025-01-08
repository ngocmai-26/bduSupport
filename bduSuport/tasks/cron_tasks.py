import logging
from dataclasses import asdict
from celery import shared_task
from bduSuport.models.bdu_student import BduStudent
from bduSuport.services.bdu_dw.bdu_dw import BduDwService

@shared_task
def sync_bdu_students():
    try:
        students = BduDwService().get_students()

        for student in students:
            try:
                _data = asdict(student)
                _data.pop("student_id", None)
                BduStudent.objects.update_or_create(
                    student_id=student.student_id,
                    defaults=_data
                )
                logging.getLogger().info("sync_bdu_students update_or_create sync student %s success", student.student_id)
            except Exception as e:
                logging.getLogger().exception("sync_bdu_students update_or_create exc=%s, dto=%s", e, student)
    except Exception as e:
        raise e