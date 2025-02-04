import datetime
import logging
from collections import defaultdict
from celery import shared_task
from bduSuport.models.student_supervision_registration import StudentSupervisionRegistration
from bduSuport.tasks.biz.send_student_attendance_notification import create_student_attendance_notification

@shared_task
def send_student_attendance_notification():
    try:
        _start_time = datetime.datetime.now()
        queryset = StudentSupervisionRegistration.objects.filter(deleted_at=None)
        grouped_users = defaultdict(list)
        student_infos = {}
        num_errors = 0

        for obj in queryset:
            grouped_users[obj.student_dw_code].append(obj.miniapp_user)
            student_infos[obj.student_dw_code] = obj.student_full_name

        today = datetime.datetime.now().date()
        
        for student_code, users in grouped_users.items():
            try:
                create_student_attendance_notification(student_code, student_infos[student_code], users, today)
            except:
                num_errors = num_errors + 1
                continue

        _end_time = datetime.datetime.now()

        return {
            "task": "send_student_attendance_notification",
            "start_time": _start_time,
            "end_time": _end_time,
            "num_errors": num_errors
        }
    except Exception as e:
        logging.getLogger().exception("send_student_attendance_notification exc=%s", str(e))
        raise e

