# Tasks

## 1. Preparación del entorno

- [ ] 1.1 Crear `pyproject.toml` con pytest como dependencia de desarrollo y verificar `python -m pytest --version` sin errores.
- [ ] 1.2 Crear `prestamos/__init__.py` y `tests/` con la estructura inicial y verificar `python -c "import prestamos"` sin errores.

## 2. Catálogo de equipos (`equipment-catalog`)

- [ ] 2.1 Escribir en `tests/test_equipment_catalog.py` las pruebas de registro de portátil, proyector y tipo inválido, y verificar que fallan en rojo con `python -m pytest tests/test_equipment_catalog.py -q`.
- [ ] 2.2 Implementar los modelos de equipo y tipo, la validación de tipo y el registro en el servicio, y verificar que las pruebas de 2.1 pasan en verde.
- [ ] 2.3 Escribir la prueba de identificador duplicado y conservación del equipo original, verificar que falla en rojo, implementar el rechazo de duplicados y verificar que pasa en verde.
- [ ] 2.4 Escribir las pruebas de inventario vacío, listado de equipos y consulta de identificador inexistente, verificar que fallan en rojo, implementar listado, consulta y error de no encontrado, y verificar que pasan en verde.
- [ ] 2.5 Refactorizar los modelos y el repositorio de equipos eliminando duplicación, y verificar que `python -m pytest tests/test_equipment_catalog.py -q` sigue en verde.

## 3. Registro de estudiantes (`student-registry`)

- [ ] 3.1 Escribir en `tests/test_student_registry.py` las pruebas de registro válido, datos vacíos e identificador duplicado, y verificar que fallan en rojo con `python -m pytest tests/test_student_registry.py -q`.
- [ ] 3.2 Implementar el modelo de estudiante, los errores de validación y duplicado, y el registro en el servicio, y verificar que las pruebas de 3.1 pasan en verde.
- [ ] 3.3 Escribir las pruebas de consulta por identificador, listado y estudiante inexistente, verificar que fallan en rojo, implementar las consultas y verificar que pasan en verde.

## 4. Préstamos y devoluciones (`equipment-loans`)

- [ ] 4.1 Escribir en `tests/test_loans.py` la prueba de préstamo exitoso con fecha fija y estado derivado del equipo, verificar que falla en rojo, implementar el modelo de préstamo, el repositorio, el reloj inyectable y la operación de préstamo, y verificar que pasa en verde.
- [ ] 4.2 Escribir las pruebas de equipo inexistente, estudiante inexistente y equipo ya prestado, verificar que fallan en rojo, implementar las validaciones y sus errores, y verificar que pasan en verde sin que se cree ningún préstamo ni cambie el estado del equipo.
- [ ] 4.3 Escribir las pruebas de devolución exitosa, devolución sin préstamo activo y equipo inexistente, verificar que fallan en rojo, implementar la devolución con cierre de fecha y recuperación de disponibilidad, y verificar que pasan en verde.
- [ ] 4.4 Escribir las pruebas de consulta de préstamo activo de un equipo, equipo disponible, préstamos por estudiante, todos los préstamos activos e historial del equipo, verificar que fallan en rojo, implementar las consultas y verificar que pasan en verde.
- [ ] 4.5 Escribir la prueba de dos equipos prestados al mismo estudiante y verificar que pasa sin añadir ningún límite de préstamos por estudiante.
- [ ] 4.6 Refactorizar el servicio y los repositorios para eliminar lógica repetida, y verificar que `python -m pytest tests/test_loans.py tests/test_equipment_catalog.py tests/test_student_registry.py -q` sigue en verde.

## 5. CLI interactiva (`loan-cli`)

- [ ] 5.1 Crear `tests/test_cli.py` con una fixture que construya la shell con un servicio nuevo y `cmdqueue`, escribir la prueba de una sesión que registra equipo y estudiante, presta y consulta el estado, y verificar que falla en rojo con `python -m pytest tests/test_cli.py -q`.
- [ ] 5.2 Implementar la shell con `cmd.Cmd`, análisis de argumentos con `shlex.split`, comandos `registrar-equipo`, `registrar-estudiante`, `prestar`, `devolver` y `salir`, y mensajes de confirmación, y verificar que la prueba de 5.1 pasa en verde.
- [ ] 5.3 Escribir las pruebas de `listar-equipos`, `estado`, `prestamos-activos`, `historial` y estado vacío en una nueva sesión, verificar que fallan en rojo, implementar los comandos de consulta y verificar que pasan en verde.
- [ ] 5.4 Escribir las pruebas de error de negocio en salida de error sin cortar la sesión, comando desconocido, argumentos insuficientes y `ayuda`, verificar que fallan en rojo, implementar el manejo de errores y la ayuda, y verificar que pasan en verde.
- [ ] 5.5 Implementar `prestamos/__main__.py` para iniciar la sesión y verificar que `python -m prestamos` muestra el mensaje de bienvenida, responde a `ayuda` y termina con `salir`.

## 6. Verificación de integración y cierre

- [ ] 6.1 Ejecutar `python -m pytest -q` y verificar que toda la suite termina en verde.
- [ ] 6.2 Ejecutar `openspec validate sistema-prestamo-equipos --strict` y verificar que no hay errores ni advertencias.
- [ ] 6.3 Revisar los cuatro deltas de `specs/` frente a los archivos de prueba y verificar que cada escenario tiene al menos una prueba asociada.
- [ ] 6.4 Realizar una prueba manual de la CLI con registrar, prestar, consultar, devolver y salir, y verificar que los mensajes y estados coinciden con las specs.
