import sys
from pathlib import Path

import tkinter as tk
from tkinter import ttk

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from prestamos.errors import LoanError
from prestamos.models import EquipmentKind
from prestamos.service import LoanService


class LoanApp:
    def __init__(self, root, service=None):
        self.root = root
        self.service = service or LoanService()
        self.root.title("Sistema de préstamo de equipos")
        self.root.geometry("900x650")
        self.status = tk.StringVar(value="Listo.")

        main = ttk.Frame(self.root, padding=10)
        main.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(2, weight=1)

        self._build_equipment_frame(main)
        self._build_student_frame(main)
        self._build_loan_frame(main)
        self._build_lists(main)

        ttk.Label(main, textvariable=self.status, anchor="w").grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=(8, 0)
        )
        self.refresh()

    def _build_equipment_frame(self, parent):
        frame = ttk.LabelFrame(parent, text="Registrar equipo", padding=8)
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        ttk.Label(frame, text="Identificador:").grid(row=0, column=0, sticky="w")
        self.equip_id = ttk.Entry(frame)
        self.equip_id.grid(row=0, column=1, sticky="ew")

        ttk.Label(frame, text="Tipo:").grid(row=1, column=0, sticky="w")
        self.equip_kind = ttk.Combobox(
            frame, values=[kind.value for kind in EquipmentKind], state="readonly"
        )
        self.equip_kind.current(0)
        self.equip_kind.grid(row=1, column=1, sticky="ew")

        ttk.Label(frame, text="Descripción:").grid(row=2, column=0, sticky="w")
        self.equip_desc = ttk.Entry(frame)
        self.equip_desc.grid(row=2, column=1, sticky="ew")

        ttk.Button(
            frame, text="Registrar equipo", command=self.register_equipment
        ).grid(row=3, column=0, columnspan=2, pady=(8, 0))
        frame.columnconfigure(1, weight=1)

    def _build_student_frame(self, parent):
        frame = ttk.LabelFrame(parent, text="Registrar estudiante", padding=8)
        frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        ttk.Label(frame, text="Identificador:").grid(row=0, column=0, sticky="w")
        self.student_id = ttk.Entry(frame)
        self.student_id.grid(row=0, column=1, sticky="ew")

        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky="w")
        self.student_name = ttk.Entry(frame)
        self.student_name.grid(row=1, column=1, sticky="ew")

        ttk.Button(
            frame, text="Registrar estudiante", command=self.register_student
        ).grid(row=2, column=0, columnspan=2, pady=(8, 0))
        frame.columnconfigure(1, weight=1)

    def _build_loan_frame(self, parent):
        frame = ttk.LabelFrame(parent, text="Préstamos y devoluciones", padding=8)
        frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        ttk.Label(frame, text="ID equipo:").grid(row=0, column=0, sticky="w")
        self.loan_equipment = ttk.Entry(frame)
        self.loan_equipment.grid(row=0, column=1, sticky="ew")

        ttk.Label(frame, text="ID estudiante:").grid(row=0, column=2, sticky="w")
        self.loan_student = ttk.Entry(frame)
        self.loan_student.grid(row=0, column=3, sticky="ew")

        ttk.Button(frame, text="Prestar", command=self.lend).grid(
            row=0, column=4, padx=(8, 0)
        )

        ttk.Label(frame, text="Devolver equipo:").grid(row=1, column=0, sticky="w")
        self.return_equipment_id = ttk.Entry(frame)
        self.return_equipment_id.grid(row=1, column=1, sticky="ew")
        ttk.Button(frame, text="Devolver", command=self.return_equipment).grid(
            row=1, column=2, columnspan=3, sticky="w", padx=(8, 0)
        )
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(3, weight=1)

    def _build_lists(self, parent):
        notebook = ttk.Notebook(parent)
        notebook.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(10, 0))

        equipment_tab = ttk.Frame(notebook, padding=5)
        student_tab = ttk.Frame(notebook, padding=5)
        loan_tab = ttk.Frame(notebook, padding=5)
        notebook.add(equipment_tab, text="Equipos")
        notebook.add(student_tab, text="Estudiantes")
        notebook.add(loan_tab, text="Préstamos activos")

        self.equip_tree = self._make_tree(
            equipment_tab,
            ("id", "tipo", "estado", "descripcion"),
            ("ID", "Tipo", "Estado", "Descripción"),
            (110, 90, 90, 250),
        )
        self.student_tree = self._make_tree(
            student_tab, ("id", "nombre"), ("ID", "Nombre"), (140, 250)
        )
        self.loan_tree = self._make_tree(
            loan_tab,
            ("id", "equipo", "estudiante", "fecha"),
            ("Préstamo", "Equipo", "Estudiante", "Fecha"),
            (100, 120, 140, 120),
        )

        ttk.Button(parent, text="Actualizar listas", command=self.refresh).grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(8, 0)
        )

    def _make_tree(self, parent, columns, headings, widths):
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=12)
        for column, heading, width in zip(columns, headings, widths):
            tree.heading(column, text=heading)
            tree.column(column, width=width)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        return tree

    def _run(self, action, message):
        try:
            result = action()
        except LoanError as exc:
            self.status.set(f"Error: {exc}")
            return False
        self.status.set(message(result) if callable(message) else message)
        self.refresh()
        return True

    def register_equipment(self):
        def action():
            return self.service.register_equipment(
                self.equip_id.get().strip(),
                self.equip_kind.get(),
                self.equip_desc.get().strip(),
            )

        if self._run(action, lambda equipo: f"Equipo {equipo.equipment_id} registrado."):
            self.equip_id.delete(0, "end")
            self.equip_desc.delete(0, "end")

    def register_student(self):
        def action():
            return self.service.register_student(
                self.student_id.get().strip(), self.student_name.get().strip()
            )

        if self._run(
            action, lambda estudiante: f"Estudiante {estudiante.student_id} registrado."
        ):
            self.student_id.delete(0, "end")
            self.student_name.delete(0, "end")

    def lend(self):
        def action():
            return self.service.lend(
                self.loan_equipment.get().strip(), self.loan_student.get().strip()
            )

        if self._run(action, lambda prestamo: f"Préstamo {prestamo.loan_id} creado."):
            self.loan_equipment.delete(0, "end")
            self.loan_student.delete(0, "end")

    def return_equipment(self):
        def action():
            return self.service.return_equipment(self.return_equipment_id.get().strip())

        if self._run(
            action, lambda prestamo: f"Devolución de {prestamo.equipment_id} registrada."
        ):
            self.return_equipment_id.delete(0, "end")

    def refresh(self):
        for tree in (self.equip_tree, self.student_tree, self.loan_tree):
            for item in tree.get_children():
                tree.delete(item)

        for equipo in self.service.list_equipment():
            estado = self.service.get_equipment_status(equipo.equipment_id).value
            self.equip_tree.insert(
                "",
                "end",
                values=(
                    equipo.equipment_id,
                    equipo.kind.value,
                    estado,
                    equipo.description,
                ),
            )

        for estudiante in self.service.list_students():
            self.student_tree.insert(
                "", "end", values=(estudiante.student_id, estudiante.name)
            )

        for prestamo in self.service.list_active_loans():
            self.loan_tree.insert(
                "",
                "end",
                values=(
                    prestamo.loan_id,
                    prestamo.equipment_id,
                    prestamo.student_id,
                    prestamo.loaned_at.date().isoformat(),
                ),
            )


def main():
    root = tk.Tk()
    LoanApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
