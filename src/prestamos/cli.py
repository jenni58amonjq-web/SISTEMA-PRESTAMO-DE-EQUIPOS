import shlex
import sys
from cmd import Cmd

from .errors import LoanError
from .service import LoanService

HELP_LINES = [
    "Comandos disponibles:",
    "  registrar-equipo <id> <laptop|projector> [descripción]",
    "  registrar-estudiante <id> <nombre>",
    "  prestar <id_equipo> <id_estudiante>",
    "  devolver <id_equipo>",
    "  listar-equipos",
    "  estado <id_equipo>",
    "  prestamos-activos",
    "  historial <id_equipo>",
    "  ayuda",
    "  salir",
]


class LoanShell(Cmd):
    def __init__(self, service=None, stdout=None, stderr=None):
        super().__init__(stdin=None, stdout=stdout)
        self.stderr = stderr if stderr is not None else sys.stderr
        self._service = service or LoanService()

    def onecmd(self, line):
        parts = line.strip().split(maxsplit=1)
        if parts:
            command = parts[0].replace("-", "_")
            line = command + (" " + parts[1] if len(parts) > 1 else "")
        return super().onecmd(line)

    def emptyline(self):
        return False

    def _error(self, message):
        self.stderr.write(f"{message}\n")

    def _parse(self, arg, minimum, maximum, usage):
        try:
            parts = shlex.split(arg)
        except ValueError:
            self._error(f"Uso: {usage}")
            return None
        if not minimum <= len(parts) <= maximum:
            self._error(f"Uso: {usage}")
            return None
        return parts

    def _guard(self, action):
        try:
            action()
        except LoanError as exc:
            self._error(str(exc))
        return False

    def do_registrar_equipo(self, arg):
        parts = self._parse(
            arg, 2, 3, "registrar-equipo <id> <laptop|projector> [descripción]"
        )
        if parts is None:
            return False

        def action():
            equipo = self._service.register_equipment(
                parts[0], parts[1], " ".join(parts[2:])
            )
            self.stdout.write(
                f"Equipo registrado: {equipo.equipment_id} ({equipo.kind.value})\n"
            )

        return self._guard(action)

    def do_registrar_estudiante(self, arg):
        parts = self._parse(
            arg, 2, 2, "registrar-estudiante <id> <nombre>"
        )
        if parts is None:
            return False

        def action():
            estudiante = self._service.register_student(parts[0], " ".join(parts[1:]))
            self.stdout.write(
                f"Estudiante registrado: {estudiante.student_id} - {estudiante.name}\n"
            )

        return self._guard(action)

    def do_prestar(self, arg):
        parts = self._parse(arg, 2, 2, "prestar <id_equipo> <id_estudiante>")
        if parts is None:
            return False

        def action():
            prestamo = self._service.lend(parts[0], parts[1])
            self.stdout.write(
                f"Préstamo {prestamo.loan_id}: {prestamo.equipment_id} "
                f"prestado a {prestamo.student_id}\n"
            )

        return self._guard(action)

    def do_devolver(self, arg):
        parts = self._parse(arg, 1, 1, "devolver <id_equipo>")
        if parts is None:
            return False

        def action():
            prestamo = self._service.return_equipment(parts[0])
            self.stdout.write(f"Devolución registrada: {prestamo.equipment_id}\n")

        return self._guard(action)

    def do_listar_equipos(self, arg):
        def action():
            equipos = self._service.list_equipment()
            if not equipos:
                self.stdout.write("No hay equipos registrados.\n")
                return
            for equipo in equipos:
                estado = self._service.get_equipment_status(equipo.equipment_id).value
                self.stdout.write(
                    f"{equipo.equipment_id} | {equipo.kind.value} | {estado} | "
                    f"{equipo.description}\n"
                )

        return self._guard(action)

    def do_estado(self, arg):
        parts = self._parse(arg, 1, 1, "estado <id_equipo>")
        if parts is None:
            return False

        def action():
            estado = self._service.get_equipment_status(parts[0]).value
            self.stdout.write(f"Equipo {parts[0]}: {estado}\n")
            prestamo = self._service.get_active_loan(parts[0])
            if prestamo is not None:
                self.stdout.write(
                    f"Préstamo {prestamo.loan_id} | estudiante {prestamo.student_id} | "
                    f"fecha {prestamo.loaned_at.date().isoformat()}\n"
                )

        return self._guard(action)

    def do_prestamos_activos(self, arg):
        def action():
            prestamos = self._service.list_active_loans()
            if not prestamos:
                self.stdout.write("No hay préstamos activos.\n")
                return
            for prestamo in prestamos:
                self.stdout.write(
                    f"{prestamo.loan_id} | {prestamo.equipment_id} | "
                    f"{prestamo.student_id} | {prestamo.loaned_at.date().isoformat()}\n"
                )

        return self._guard(action)

    def do_historial(self, arg):
        parts = self._parse(arg, 1, 1, "historial <id_equipo>")
        if parts is None:
            return False

        def action():
            historial = self._service.get_equipment_history(parts[0])
            if not historial:
                self.stdout.write(f"Sin historial para {parts[0]}.\n")
                return
            for prestamo in historial:
                devolucion = (
                    prestamo.returned_at.date().isoformat()
                    if prestamo.returned_at is not None
                    else "-"
                )
                self.stdout.write(
                    f"{prestamo.loan_id} | {prestamo.equipment_id} | "
                    f"{prestamo.student_id} | {prestamo.loaned_at.date().isoformat()} "
                    f"| {devolucion}\n"
                )

        return self._guard(action)

    def do_ayuda(self, arg):
        for line in HELP_LINES:
            self.stdout.write(line + "\n")
        return False

    def do_salir(self, arg):
        self.stdout.write("Hasta luego.\n")
        return True

    def default(self, line):
        self.stdout.write(
            "Comando desconocido. Escribe 'ayuda' para ver los comandos disponibles.\n"
        )
        return False
