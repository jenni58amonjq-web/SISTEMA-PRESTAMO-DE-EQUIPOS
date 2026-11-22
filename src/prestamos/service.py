from datetime import datetime, timezone

from .errors import DuplicateRecordError, EquipmentUnavailableError, NoActiveLoanError, ValidationError
from .models import Equipment, EquipmentKind, EquipmentStatus, Student
from .repositories import (
    InMemoryEquipmentRepository,
    InMemoryLoanRepository,
    InMemoryStudentRepository,
)


def _coerce_kind(kind):
    if isinstance(kind, EquipmentKind):
        return kind
    if isinstance(kind, str):
        for member in EquipmentKind:
            if kind.lower() == member.value:
                return member
    raise ValidationError(f"Tipo de equipo no soportado: {kind!r}")


def _require_text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field} no puede estar vacío")
    return value


class LoanService:
    def __init__(self, clock=None, equipment_repo=None, student_repo=None, loan_repo=None):
        self._clock = clock or (lambda: datetime.now(timezone.utc))
        self._equipment = equipment_repo or InMemoryEquipmentRepository()
        self._students = student_repo or InMemoryStudentRepository()
        self._loans = loan_repo or InMemoryLoanRepository()

    def register_equipment(self, equipment_id, kind, description=""):
        equipment_id = _require_text(equipment_id, "Identificador de equipo")
        kind = _coerce_kind(kind)
        if equipment_id in [item.equipment_id for item in self._equipment.list()]:
            raise DuplicateRecordError(f"Equipo ya registrado: {equipment_id}")
        return self._equipment.add(
            Equipment(
                equipment_id=equipment_id,
                kind=kind,
                description=description or "",
            )
        )

    def register_student(self, student_id, name):
        student_id = _require_text(student_id, "Identificador de estudiante")
        name = _require_text(name, "Nombre del estudiante")
        if student_id in [item.student_id for item in self._students.list()]:
            raise DuplicateRecordError(f"Estudiante ya registrado: {student_id}")
        return self._students.add(Student(student_id=student_id, name=name))

    def lend(self, equipment_id, student_id):
        self._equipment.get(equipment_id)
        self._students.get(student_id)
        if self._loans.active_for_equipment(equipment_id) is not None:
            raise EquipmentUnavailableError(f"Equipo no disponible: {equipment_id}")
        return self._loans.add(equipment_id, student_id, self._clock())

    def return_equipment(self, equipment_id):
        self._equipment.get(equipment_id)
        loan = self._loans.active_for_equipment(equipment_id)
        if loan is None:
            raise NoActiveLoanError(f"Equipo sin préstamo activo: {equipment_id}")
        loan.returned_at = self._clock()
        return loan

    def get_equipment(self, equipment_id):
        return self._equipment.get(equipment_id)

    def list_equipment(self):
        return self._equipment.list()

    def get_student(self, student_id):
        return self._students.get(student_id)

    def list_students(self):
        return self._students.list()

    def get_equipment_status(self, equipment_id):
        self._equipment.get(equipment_id)
        if self._loans.active_for_equipment(equipment_id) is None:
            return EquipmentStatus.DISPONIBLE
        return EquipmentStatus.PRESTADO

    def get_active_loan(self, equipment_id):
        self._equipment.get(equipment_id)
        return self._loans.active_for_equipment(equipment_id)

    def get_active_loans_for_student(self, student_id):
        self._students.get(student_id)
        return self._loans.active_for_student(student_id)

    def list_active_loans(self):
        return self._loans.active_all()

    def get_equipment_history(self, equipment_id):
        self._equipment.get(equipment_id)
        return self._loans.history_for_equipment(equipment_id)
