import sys
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from prestamos.errors import LoanError
from prestamos.service import LoanService

app = Flask(__name__)
app.config["SECRET_KEY"] = "sistema-prestamos-desarrollo"
TEMPLATES_DIR = ROOT / "templates"
service = LoanService()


@app.route("/style.css")
def style():
    return send_from_directory(TEMPLATES_DIR, "style.css", mimetype="text/css")


def _view_data():
    equipos = []
    for equipo in service.list_equipment():
        equipos.append(
            {
                "id": equipo.equipment_id,
                "tipo": equipo.kind.value,
                "estado": service.get_equipment_status(equipo.equipment_id).value,
                "descripcion": equipo.description,
            }
        )

    estudiantes = [
        {"id": estudiante.student_id, "nombre": estudiante.name}
        for estudiante in service.list_students()
    ]

    prestamos = [
        {
            "id": prestamo.loan_id,
            "equipo": prestamo.equipment_id,
            "estudiante": prestamo.student_id,
            "fecha": prestamo.loaned_at.date().isoformat(),
        }
        for prestamo in service.list_active_loans()
    ]

    return equipos, estudiantes, prestamos


@app.route("/")
def index():
    equipos, estudiantes, prestamos = _view_data()
    return render_template(
        "index.html",
        equipos=equipos,
        estudiantes=estudiantes,
        prestamos=prestamos,
        total_equipos=len(equipos),
        total_estudiantes=len(estudiantes),
        total_prestamos=len(prestamos),
    )


@app.post("/equipos")
def create_equipment():
    try:
        equipo = service.register_equipment(
            request.form.get("equipment_id", "").strip(),
            request.form.get("kind", "").strip(),
            request.form.get("description", "").strip(),
        )
        flash(f"Equipo {equipo.equipment_id} registrado correctamente.", "success")
    except LoanError as exc:
        flash(str(exc), "error")
    return redirect(url_for("index"))


@app.post("/estudiantes")
def create_student():
    try:
        estudiante = service.register_student(
            request.form.get("student_id", "").strip(),
            request.form.get("name", "").strip(),
        )
        flash(f"Estudiante {estudiante.student_id} registrado correctamente.", "success")
    except LoanError as exc:
        flash(str(exc), "error")
    return redirect(url_for("index"))


@app.post("/prestamos")
def create_loan():
    try:
        prestamo = service.lend(
            request.form.get("equipment_id", "").strip(),
            request.form.get("student_id", "").strip(),
        )
        flash(f"Préstamo {prestamo.loan_id} creado correctamente.", "success")
    except LoanError as exc:
        flash(str(exc), "error")
    return redirect(url_for("index"))


@app.post("/devoluciones")
def return_equipment():
    try:
        prestamo = service.return_equipment(
            request.form.get("equipment_id", "").strip()
        )
        flash(f"Devolución de {prestamo.equipment_id} registrada.", "success")
    except LoanError as exc:
        flash(str(exc), "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
