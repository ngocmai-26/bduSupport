from dataclasses import dataclass, field
from datetime import datetime
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
    date_of_birth: Optional[datetime] = field(default=None)
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
        date_fields = ["created_at", "date_of_birth", "updated_at"]
        for field_name in date_fields:
            value = getattr(self, field_name)
            if value and isinstance(value, str):
                try:
                    setattr(self, field_name, datetime.strptime(value, "%a, %d %b %Y %H:%M:%S %Z"))
                except ValueError:
                    setattr(self, field_name, None)
