import pytest


def _prestar(service, models, equipment_id="LAP-001", student_id="202312345"):
    service.register_equipment(equipment_id, models.EquipmentKind.LAPTOP)
    service.register_student(student_id, "Ana Torres")
    return service.lend(equipment_id, student_id)


def test_prestar_equipo_disponible_crea_prestamo_activo(
    service, models, fixed_now
):
    prestamo = _prestar(service, models)

    assert prestamo.equipment_id == "LAP-001"
    assert prestamo.student_id == "202312345"
    assert prestamo.loaned_at == fixed_now
    assert prestamo.returned_at is None
    assert service.get_equipment_status("LAP-001") is models.EquipmentStatus.PRESTADO


def test_prestar_equipo_inexistente_no_crea_prestamo(service, errors):
    service.register_student("202312345", "Ana Torres")

    with pytest.raises(errors.NotFoundError):
        service.lend("NO-EXISTE", "202312345")

    assert service.list_active_loans() == []


def test_prestar_a_estudiante_inexistente_deja_equipo_disponible(
    service, models, errors
):
    service.register_equipment("LAP-001", models.EquipmentKind.LAPTOP)

    with pytest.raises(errors.NotFoundError):
        service.lend("LAP-001", "NO-EXISTE")

    assert service.list_active_loans() == []
    assert service.get_equipment_status("LAP-001") is models.EquipmentStatus.DISPONIBLE


def test_prestar_equipo_ya_prestado_conserva_prestamo_original(
    service, models, errors
):
    original = _prestar(service, models)

    with pytest.raises(errors.EquipmentUnavailableError):
        service.lend("LAP-001", "202312345")

    assert service.get_active_loan("LAP-001") == original


def test_devolver_equipo_prestado_lo_deja_disponible(service, models, fixed_now):
    prestamo = _prestar(service, models)

    devuelto = service.return_equipment("LAP-001")

    assert devuelto == prestamo
    assert devuelto.returned_at == fixed_now
    assert service.get_equipment_status("LAP-001") is models.EquipmentStatus.DISPONIBLE
    assert service.get_active_loan("LAP-001") is None


def test_devolver_equipo_sin_prestamo_activo_lanza_error(
    service, models, errors
):
    service.register_equipment("LAP-001", models.EquipmentKind.LAPTOP)

    with pytest.raises(errors.NoActiveLoanError):
        service.return_equipment("LAP-001")

    assert service.get_equipment_status("LAP-001") is models.EquipmentStatus.DISPONIBLE


def test_devolver_equipo_inexistente_lanza_error(service, errors):
    with pytest.raises(errors.NotFoundError):
        service.return_equipment("NO-EXISTE")


def test_consultar_prestamo_activo_de_equipo_prestado(service, models):
    prestamo = _prestar(service, models)

    assert service.get_active_loan("LAP-001") == prestamo


def test_consultar_equipo_sin_prestamo_activo_devuelve_none(service, models):
    service.register_equipment("LAP-001", models.EquipmentKind.LAPTOP)

    assert service.get_active_loan("LAP-001") is None


def test_consultar_prestamos_activos_de_un_estudiante(service, models):
    service.register_equipment("LAP-001", models.EquipmentKind.LAPTOP)
    service.register_equipment("PRO-001", models.EquipmentKind.PROJECTOR)
    service.register_student("202312345", "Ana Torres")
    service.lend("LAP-001", "202312345")
    service.lend("PRO-001", "202312345")

    activos = service.get_active_loans_for_student("202312345")

    assert {prestamo.equipment_id for prestamo in activos} == {"LAP-001", "PRO-001"}
    assert all(prestamo.returned_at is None for prestamo in activos)


def test_listar_solo_prestamos_activos(service, models):
    _prestar(service, models)
    service.register_equipment("PRO-001", models.EquipmentKind.PROJECTOR)
    prestamo_activo = service.lend("PRO-001", "202312345")
    service.return_equipment("LAP-001")

    assert service.list_active_loans() == [prestamo_activo]


def test_historial_del_equipo_incluye_prestamos_cerrados_y_activos(
    service, models, fixed_now
):
    service.register_equipment("LAP-001", models.EquipmentKind.LAPTOP)
    service.register_student("202312345", "Ana Torres")
    service.register_student("202312346", "Luis Pérez")
    primero = service.lend("LAP-001", "202312345")
    service.return_equipment("LAP-001")
    segundo = service.lend("LAP-001", "202312346")

    historial = service.get_equipment_history("LAP-001")

    assert historial == [primero, segundo]
    assert historial[0].returned_at == fixed_now
    assert historial[1].returned_at is None


def test_un_estudiante_puede_tener_dos_prestamos_activos(service, models):
    service.register_equipment("LAP-001", models.EquipmentKind.LAPTOP)
    service.register_equipment("PRO-001", models.EquipmentKind.PROJECTOR)
    service.register_student("202312345", "Ana Torres")

    service.lend("LAP-001", "202312345")
    service.lend("PRO-001", "202312345")

    assert len(service.get_active_loans_for_student("202312345")) == 2
    assert service.get_equipment_status("LAP-001") is models.EquipmentStatus.PRESTADO
    assert service.get_equipment_status("PRO-001") is models.EquipmentStatus.PRESTADO
