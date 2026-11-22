import pytest


def test_registrar_portatil_deja_equipo_disponible(service, models):
    equipo = service.register_equipment(
        "LAP-001", models.EquipmentKind.LAPTOP, "Portátil lab 1"
    )

    assert equipo.equipment_id == "LAP-001"
    assert equipo.kind is models.EquipmentKind.LAPTOP
    assert equipo.description == "Portátil lab 1"
    assert service.get_equipment_status("LAP-001") is models.EquipmentStatus.DISPONIBLE


def test_registrar_proyector_deja_equipo_disponible(service, models):
    equipo = service.register_equipment("PRO-001", models.EquipmentKind.PROJECTOR)

    assert equipo.kind is models.EquipmentKind.PROJECTOR
    assert service.get_equipment_status("PRO-001") is models.EquipmentStatus.DISPONIBLE


def test_registrar_tipo_no_soportado_se_rechaza(service, errors):
    with pytest.raises(errors.ValidationError):
        service.register_equipment("TAB-001", "tablet")

    assert service.list_equipment() == []


def test_registrar_identificador_duplicado_no_altera_original(service, models, errors):
    original = service.register_equipment(
        "LAP-001", models.EquipmentKind.LAPTOP, "Original"
    )

    with pytest.raises(errors.DuplicateRecordError):
        service.register_equipment(
            "LAP-001", models.EquipmentKind.PROJECTOR, "Reemplazo"
        )

    assert service.get_equipment("LAP-001") == original


def test_inventario_vacio_al_iniciar(service):
    assert service.list_equipment() == []


def test_listar_equipos_registrados(service, models):
    service.register_equipment("LAP-001", models.EquipmentKind.LAPTOP)
    service.register_equipment("PRO-001", models.EquipmentKind.PROJECTOR)

    equipos = service.list_equipment()

    assert [equipo.equipment_id for equipo in equipos] == ["LAP-001", "PRO-001"]
    assert [equipo.kind for equipo in equipos] == [
        models.EquipmentKind.LAPTOP,
        models.EquipmentKind.PROJECTOR,
    ]
    assert [
        service.get_equipment_status(equipo.equipment_id) for equipo in equipos
    ] == [models.EquipmentStatus.DISPONIBLE] * 2


def test_consultar_equipo_inexistente_lanza_error(service, errors):
    with pytest.raises(errors.NotFoundError):
        service.get_equipment("NO-EXISTE")
