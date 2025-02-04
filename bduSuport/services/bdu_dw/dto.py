from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional

@dataclass
class BduStudentDto:
    id_card: str = ""
    created_at: Optional[datetime] = field(default=None)
    ethnicity: Optional[str] = None
    email: str = ""
    gender: str = ""
    attendance: Optional[str] = None
    residence: str = ""
    last_name: str = ""
    major_code: Optional[str] = None
    advisor_code: Optional[str] = None
    education_system_code: Optional[str] = None
    faculty_code: str = ""
    class_code: str = ""
    field_code: str = ""
    student_id: int = 0
    date_of_birth: Optional[date] = field(default=None)
    source: str = ""
    academic_year: str = ""
    place_of_birth: str = ""
    phone_number: str = ""
    degree_name: str = ""
    major_name: Optional[str] = None
    advisor_name: Optional[str] = None
    full_name: str = ""
    faculty_name: str = ""
    class_name: Optional[str] = None
    field_name: str = ""
    first_name: str = ""
    religion: str = ""
    updated_at: Optional[datetime] = field(default=None)

    def __post_init__(self):
        setattr(self, "created_at", datetime.strptime(self.created_at, "%a, %d %b %Y %H:%M:%S %Z"))
        setattr(self, "updated_at", datetime.strptime(self.updated_at, "%a, %d %b %Y %H:%M:%S %Z"))
        setattr(self, "date_of_birth", datetime.strptime(self.date_of_birth, "%a, %d %b %Y %H:%M:%S %Z").date())

@dataclass
class Attendance:
    lesson: str = ""
    status: Optional[str] = None
    attendance_id: str = ""
    subject_code: str = ""
    group_code: str = ""
    student_code: str = ""
    attendance_date: Optional[date] = field(default=None)
    attendance_datetime: Optional[datetime] = field(default=None)
    created_at: Optional[datetime] = field(default=None)
    updated_at: Optional[datetime] = field(default=None)

    def __post_init__(self):
        setattr(self, "created_at", datetime.strptime(self.created_at, "%a, %d %b %Y %H:%M:%S %Z"))
        setattr(self, "updated_at", datetime.strptime(self.updated_at, "%a, %d %b %Y %H:%M:%S %Z"))
        setattr(self, "attendance_datetime", datetime.strptime(self.attendance_datetime, "%a, %d %b %Y %H:%M:%S %Z"))
        setattr(self, "attendance_date", datetime.strptime(self.attendance_date, "%Y-%m-%d").date())
