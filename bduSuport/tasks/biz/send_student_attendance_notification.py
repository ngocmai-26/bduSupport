from datetime import date
import logging
from typing import List
from bduSuport.models.mini_app_user import MiniAppUser
from bduSuport.services.bdu_dw.bdu_dw import BduDwService
from bduSuport.models.miniapp_notification import MiniappNotification

def create_student_attendance_notification(student_dw_code: int, student_name: str, mini_app_users: List[MiniAppUser], attendance_date: date):
    try:
        attendances = BduDwService().get_attendances_by_student_code_and_date_range(student_dw_code, attendance_date, attendance_date)

        for attendance in attendances:
            _attendance_date = attendance.attendance_date.strftime("%d-%m-%Y")

            for mini_app_user in mini_app_users:
                try:
                    MiniappNotification.objects.create(
                        user=mini_app_user,
                        content=f"Sinh viên {attendance.student_code} - {student_name} tham gia môn học {attendance.subject_code} vào ngày {_attendance_date} (buổi: {attendance.lesson}) với trạng thái điểm danh: {attendance.status}"
                    )
                except Exception as e:
                    logging.getLogger().exception(
                        "create_student_attendance_notification create notification failed exc=%s, student_code=%s, student_name=%s, subject_code=%s, _attendance_date=%s, lesson=%s, status=%s",
                        str(e),
                        attendance.student_code,
                        student_name,
                        attendance.subject_code,
                        _attendance_date,
                        attendance.lesson,
                        attendance.status
                    )
                    continue
    except Exception as e:
        logging.getLogger().exception(
            "create_student_attendance_notification exc=%s, student_dw_code=%s, mini_app_user_ids=%s", 
            str(e), student_dw_code, [user.id for user in mini_app_users]
        )
