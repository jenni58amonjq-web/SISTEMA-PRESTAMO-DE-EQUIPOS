def test_sesion_mantiene_estado_entre_comandos(shell_factory, capsys):
    shell = shell_factory()

    shell.onecmd("registrar-equipo LAP-001 laptop 'Portátil lab 1'")
    shell.onecmd("registrar-estudiante 202312345 'Ana Torres'")
    shell.onecmd("prestar LAP-001 202312345")
    shell.onecmd("estado LAP-001")

    salida = capsys.readouterr().out
    assert "prestado" in salida.lower()
    assert "202312345" in salida


def test_nueva_sesion_empieza_con_inventario_vacio(shell_factory, capsys):
    primera = shell_factory()
    primera.onecmd("registrar-equipo LAP-001 laptop")
    capsys.readouterr()

    segunda = shell_factory()
    segunda.onecmd("listar-equipos")

    assert "LAP-001" not in capsys.readouterr().out


def test_registrar_equipo_desde_cli_muestra_confirmacion(shell_factory, capsys):
    shell = shell_factory()

    shell.onecmd('registrar-equipo LAP-001 laptop "Portátil lab 1"')

    salida = capsys.readouterr().out
    assert "LAP-001" in salida
    shell.onecmd("estado LAP-001")
    assert "disponible" in capsys.readouterr().out.lower()


def test_registrar_estudiante_desde_cli_muestra_confirmacion(shell_factory, capsys):
    shell = shell_factory()

    shell.onecmd('registrar-estudiante 202312345 "Ana Torres"')

    salida = capsys.readouterr().out
    assert "202312345" in salida
    assert "Ana Torres" in salida


def test_prestar_desde_cli_muestra_identificador_del_prestamo(shell_factory, capsys):
    shell = shell_factory()
    shell.onecmd("registrar-equipo LAP-001 laptop")
    shell.onecmd("registrar-estudiante 202312345 Ana")
    capsys.readouterr()

    shell.onecmd("prestar LAP-001 202312345")

    salida = capsys.readouterr().out
    assert "LAP-001" in salida
    assert "202312345" in salida


def test_devolver_desde_cli_deja_equipo_disponible(shell_factory, capsys):
    shell = shell_factory()
    shell.onecmd("registrar-equipo LAP-001 laptop")
    shell.onecmd("registrar-estudiante 202312345 Ana")
    shell.onecmd("prestar LAP-001 202312345")
    capsys.readouterr()

    shell.onecmd("devolver LAP-001")

    assert "LAP-001" in capsys.readouterr().out
    shell.onecmd("estado LAP-001")
    assert "disponible" in capsys.readouterr().out.lower()


def test_salir_termina_la_sesion(shell_factory):
    shell = shell_factory()

    assert shell.onecmd("salir") is True


def test_listar_equipos_muestra_identificadores_tipo_y_estado(shell_factory, capsys):
    shell = shell_factory()
    shell.onecmd("registrar-equipo LAP-001 laptop")
    shell.onecmd("registrar-equipo PRO-001 projector")
    capsys.readouterr()

    shell.onecmd("listar-equipos")

    salida = capsys.readouterr().out
    assert "LAP-001" in salida
    assert "PRO-001" in salida
    assert "laptop" in salida.lower()
    assert "projector" in salida.lower()
    assert "disponible" in salida.lower()


def test_estado_de_equipo_prestado_muestra_estudiante_y_fecha(
    shell_factory, capsys, fixed_now
):
    shell = shell_factory()
    shell.onecmd("registrar-equipo LAP-001 laptop")
    shell.onecmd("registrar-estudiante 202312345 Ana")
    shell.onecmd("prestar LAP-001 202312345")
    capsys.readouterr()

    shell.onecmd("estado LAP-001")

    salida = capsys.readouterr().out
    assert "prestado" in salida.lower()
    assert "202312345" in salida
    assert str(fixed_now.date()) in salida


def test_prestamos_activos_muestra_equipo_estudiante_y_fecha(
    shell_factory, capsys, fixed_now
):
    shell = shell_factory()
    shell.onecmd("registrar-equipo LAP-001 laptop")
    shell.onecmd("registrar-estudiante 202312345 Ana")
    shell.onecmd("prestar LAP-001 202312345")
    capsys.readouterr()

    shell.onecmd("prestamos-activos")

    salida = capsys.readouterr().out
    assert "LAP-001" in salida
    assert "202312345" in salida
    assert str(fixed_now.date()) in salida


def test_historial_muestra_fechas_de_prestamo_y_devolucion(
    shell_factory, capsys, fixed_now
):
    shell = shell_factory()
    shell.onecmd("registrar-equipo LAP-001 laptop")
    shell.onecmd("registrar-estudiante 202312345 Ana")
    shell.onecmd("prestar LAP-001 202312345")
    shell.onecmd("devolver LAP-001")
    capsys.readouterr()

    shell.onecmd("historial LAP-001")

    salida = capsys.readouterr().out
    assert "LAP-001" in salida
    assert salida.count(str(fixed_now.date())) >= 2


def test_error_de_negocio_no_interrumpe_la_sesion(shell_factory, capsys):
    shell = shell_factory()
    shell.onecmd("registrar-equipo LAP-001 laptop")
    shell.onecmd("registrar-estudiante 202312345 Ana")
    shell.onecmd("prestar LAP-001 202312345")
    capsys.readouterr()

    shell.onecmd("prestar LAP-001 202312345")

    assert capsys.readouterr().err.strip() != ""
    shell.onecmd("estado LAP-001")
    assert "prestado" in capsys.readouterr().out.lower()


def test_comando_desconocido_muestra_ayuda(shell_factory, capsys):
    shell = shell_factory()

    shell.onecmd("inventar-comando")

    captura = capsys.readouterr()
    salida = (captura.out + captura.err).lower()
    assert "ayuda" in salida or "comandos" in salida


def test_argumentos_insuficientes_no_crean_prestamo(shell_factory, service_factory, capsys):
    service = service_factory()
    shell = shell_factory(service)

    shell.onecmd("prestar")

    captura = capsys.readouterr()
    assert captura.err.strip() != ""
    assert service.list_active_loans() == []


def test_ayuda_lista_los_comandos_disponibles(shell_factory, capsys):
    shell = shell_factory()

    shell.onecmd("ayuda")

    salida = capsys.readouterr().out.lower()
    assert "registrar-equipo" in salida
    assert "registrar-estudiante" in salida
    assert "prestar" in salida
    assert "devolver" in salida
