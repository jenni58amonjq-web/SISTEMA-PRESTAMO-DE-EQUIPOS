import pytest


def test_registrar_estudiante(service):
    estudiante = service.register_student("202312345", "Ana Torres")

    assert estudiante.student_id == "202312345"
    assert estudiante.name == "Ana Torres"
    assert service.get_student("202312345") == estudiante


@pytest.mark.parametrize(
    ("student_id", "name"), [("", "Ana Torres"), ("202312345", "")]
)
def test_registrar_estudiante_con_datos_vacios_se_rechaza(service, errors, student_id, name):
    with pytest.raises(errors.ValidationError):
        service.register_student(student_id, name)

    assert service.list_students() == []


def test_registrar_estudiante_duplicado_no_altera_original(service, errors):
    original = service.register_student("202312345", "Ana Torres")

    with pytest.raises(errors.DuplicateRecordError):
        service.register_student("202312345", "Otro Nombre")

    assert service.get_student("202312345") == original


def test_consultar_estudiante_inexistente_lanza_error(service, errors):
    with pytest.raises(errors.NotFoundError):
        service.get_student("NO-EXISTE")


def test_listar_estudiantes_registrados(service):
    service.register_student("202312345", "Ana Torres")
    service.register_student("202312346", "Luis Pérez")

    estudiantes = service.list_students()

    assert [(e.student_id, e.name) for e in estudiantes] == [
        ("202312345", "Ana Torres"),
        ("202312346", "Luis Pérez"),
    ]
