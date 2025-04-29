from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Optional

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
    subject_name: str = ""
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

@dataclass
class StudentScore:
    student_id: int = 0
    full_name: str = ""
    class_name: str = ""
    subject_name: str = ""
    department_code: str = ""
    academic_year: str = ""
    semester_code: int = 0
    semester: int = 0
    subject_group: str = ""
    passed: bool = False
    letter_grade: str = "F"
    final_score_10: float = 0.0
    final_score_4: float = 0.0
    midterm_score: Optional[float] = None
    midterm_weight: int = 0
    final_exam_score: Optional[float] = None
    final_exam_weight: int = 0
    library_score: Optional[float] = None
    library_weight: Optional[int] = None
    created_at: Optional[datetime] = field(default=None)
    updated_at: Optional[datetime] = field(default=None)

    def __post_init__(self):
        setattr(self, "created_at", datetime.strptime(self.created_at, "%a, %d %b %Y %H:%M:%S %Z"))
        setattr(self, "updated_at", datetime.strptime(self.updated_at, "%a, %d %b %Y %H:%M:%S %Z"))

@dataclass
class TimeTable:
    lesson_number: int = 0
    student_list: List[int] = field(default_factory=list)
    lecturer_code: str = ""
    class_code: str = ""
    subject_code: str = ""
    group_code: str = ""
    room_code: str = ""
    lesson_date: Optional[date] = field(default=None)
    group_number: str = ""
    semester_code: int = 0
    periods: int = 0
    lecturer_name: str = ""
    subject_name: str = ""
    weekday_number: int = 0
    start_period: int = 0
    start_week: int = 0

    def __post_init__(self):
        if isinstance(self.lesson_date, str):
            try:
                self.lesson_date = datetime.strptime(self.lesson_date, "%a, %d %b %Y %H:%M:%S %Z").date()
            except ValueError:
                pass
        
        if isinstance(self.student_list, str):
            self.student_list = []
            return
        
            try:
                self.student_list = eval(self.student_list)
                if not isinstance(self.student_list, list):
                    self.student_list = []
            except Exception:
                self.student_list = []

        if isinstance(self.start_week, str) and self.start_week.isdigit():
            self.start_week = int(self.start_week)

        if isinstance(self.lesson_number, str) and self.lesson_number.isdigit():
            self.lesson_number = int(self.lesson_number)
