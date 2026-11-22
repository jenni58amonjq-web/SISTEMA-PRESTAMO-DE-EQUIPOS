from .errors import NotFoundError
from .models import Loan


class InMemoryEquipmentRepository:
    def __init__(self):
        self._items = {}

    def add(self, equipment):
        self._items[equipment.equipment_id] = equipment
        return equipment

    def get(self, equipment_id):
        try:
            return self._items[equipment_id]
        except KeyError:
            raise NotFoundError(f"Equipo no encontrado: {equipment_id}") from None

    def list(self):
        return list(self._items.values())


class InMemoryStudentRepository:
    def __init__(self):
        self._items = {}

    def add(self, student):
        self._items[student.student_id] = student
        return student

    def get(self, student_id):
        try:
            return self._items[student_id]
        except KeyError:
            raise NotFoundError(f"Estudiante no encontrado: {student_id}") from None

    def list(self):
        return list(self._items.values())


class InMemoryLoanRepository:
    def __init__(self):
        self._items = []
        self._next_number = 1

    def add(self, equipment_id, student_id, loaned_at):
        loan = Loan(
            loan_id=f"P-{self._next_number:04d}",
            equipment_id=equipment_id,
            student_id=student_id,
            loaned_at=loaned_at,
        )
        self._next_number += 1
        self._items.append(loan)
        return loan

    def active_for_equipment(self, equipment_id):
        for loan in self._items:
            if loan.equipment_id == equipment_id and loan.is_active:
                return loan
        return None

    def active_for_student(self, student_id):
        return [
            loan
            for loan in self._items
            if loan.student_id == student_id and loan.is_active
        ]

    def active_all(self):
        return [loan for loan in self._items if loan.is_active]

    def history_for_equipment(self, equipment_id):
        return [loan for loan in self._items if loan.equipment_id == equipment_id]
