from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EquipmentKind(Enum):
    LAPTOP = "laptop"
    PROJECTOR = "projector"


class EquipmentStatus(Enum):
    DISPONIBLE = "disponible"
    PRESTADO = "prestado"


@dataclass
class Equipment:
    equipment_id: str
    kind: EquipmentKind
    description: str = ""


@dataclass
class Student:
    student_id: str
    name: str


@dataclass
class Loan:
    loan_id: str
    equipment_id: str
    student_id: str
    loaned_at: datetime
    returned_at: datetime | None = None

    @property
    def is_active(self):
        return self.returned_at is None
