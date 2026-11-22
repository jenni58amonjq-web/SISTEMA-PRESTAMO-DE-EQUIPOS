# Design

## Context

El proyecto está vacío salvo el andamiaje de OpenSpec; no hay código, dependencias ni specs previas. La motivación y el alcance están en `proposal.md`; el comportamiento observable está en los cuatro deltas de `specs/`. Las decisiones tomadas con el usuario son: API Python como núcleo, CLI interactiva encima y estado solo en memoria.

## Goals / Non-Goals

**Goals:**

- Mantener las reglas de préstamo en un único núcleo independiente de cualquier interfaz.
- Hacer que cada escenario de las specs pueda comprobarse con una prueba pytest pequeña y determinista.
- Permitir sustituir el almacenamiento en memoria por otro sin cambiar las reglas de negocio.
- Mantener la CLI como una capa delgada de parseo y presentación.

**Non-Goals:**

- Persistir datos entre procesos ni compartir estado entre sesiones.
- Introducir frameworks web, ORM, bases de datos o dependencias de producción externas.
- Resolver concurrencia, reservas, fechas límite, multas ni autenticación.

## Decisions

### Arquitectura en capas con repositorios en memoria

El núcleo expone un servicio de préstamos que coordina tres repositorios en memoria: equipos, estudiantes y préstamos. La API Python son las operaciones públicas de ese servicio; la CLI las invoca y solo se encarga de leer argumentos y mostrar resultados.

- **Rationale:** separar reglas de interfaz permite probar el dominio sin terminal y hace sustituible el almacenamiento.
- **Alternativas consideradas:** poner la lógica dentro de la CLI (rechazado: acopla reglas a E/S y complica las pruebas); un único diccionario global (rechazado: mezcla responsabilidades y dificulta consultas).

### Estado del equipo derivado del préstamo activo

No se guarda un campo independiente `disponible`/`prestado`. El estado observable de un equipo se calcula a partir de si existe un préstamo sin fecha de devolución; el servicio garantiza que el préstamo se cierre antes de que el equipo vuelva a aparecer como disponible.

- **Rationale:** evita que un indicador duplicado quede desincronizado tras un préstamo o una devolución fallida.
- **Alternativas consideradas:** bandera de estado en el equipo actualizada manualmente (rechazado: dos fuentes de verdad).

### Modelo de datos mínimo

- Equipo: identificador único, tipo `laptop` o `projector`, descripción opcional.
- Estudiante: identificador único y nombre obligatorio.
- Préstamo: identificador único, equipo, estudiante, fecha de préstamo y fecha de devolución opcional; está activo si la fecha de devolución es nula.
- Se usan `dataclasses` y enums de la biblioteca estándar; fechas con `datetime` en UTC.

### Reloj inyectable para pruebas deterministas

El servicio recibe una función reloj con valor por defecto `datetime.now(timezone.utc)`. Las pruebas pueden fijar una fecha concreta sin parchear la biblioteca estándar.

- **Rationale:** las aserciones sobre fechas de préstamo y devolución son estables y no dependen del momento de ejecución.
- **Alternativas consideradas:** usar la hora real y comparar rangos (rechazado: pruebas frágiles); parchear `datetime` globalmente (rechazado: efecto colateral).

### Errores de dominio tipados

Una jerarquía base de error de préstamo cubre validación, duplicados, no encontrado, equipo no disponible y devolución sin préstamo activo. La CLI captura solo esa jerarquía, escribe el mensaje en la salida de error y continúa la sesión; los errores de uso se distinguen de los errores de negocio.

- **Rationale:** hace verificables los escenarios de error y evita ocultar fallos de programación.
- **Alternativas consideradas:** devolver `None` o tuples de error (rechazado: obliga a cada llamador a interpretar el resultado).

### CLI interactiva con `cmd`

Se usa `cmd.Cmd` de la biblioteca estándar para una sesión REPL con comandos en español: `registrar-equipo`, `registrar-estudiante`, `prestar`, `devolver`, `listar-equipos`, `estado`, `prestamos-activos`, `historial`, `ayuda` y `salir`. Los argumentos se analizan con `shlex.split` para respetar comillas. Cada sesión crea su propio servicio, por lo que el estado se conserva solo mientras la sesión está abierta.

- **Rationale:** cumple la decisión de estado en memoria sin engañar al usuario con datos que desaparecen entre comandos de una misma sesión.
- **Alternativas consideradas:** un comando por proceso (rechazado: perdería todo el estado entre invocaciones); `argparse` clásico (rechazado: no mantiene sesión interactiva).

### Estructura de proyecto y estrategia TDD

```
prestamos/
  __init__.py
  models.py
  errors.py
  repositories.py
  service.py
  cli.py
  __main__.py
tests/
  conftest.py
  test_equipment_catalog.py
  test_student_registry.py
  test_loans.py
  test_cli.py
pyproject.toml
```

Ciclo rojo-verde-refactor: una prueba nueva por escenario, ejecutar `pytest -q` y verla fallar, implementar lo mínimo, verla pasar y refactorizar. Una fixture entrega un servicio nuevo y un reloj fijo a cada prueba; las pruebas de CLI usan `cmdqueue` y captura de salida. El orden de implementación sigue dependencias: modelos y errores, catálogo, estudiantes, préstamos, consultas y finalmente la CLI.

- **Rationale:** cada prueba aísla un comportamiento de la spec y el orden evita construir la CLI sobre reglas no verificadas.
- **Alternativas consideradas:** escribir todas las pruebas antes de cualquier código (rechazado: retrasa la retroalimentación); usar mocks en repositorios (innecesario: las implementaciones en memoria son simples y rápidas).

## Risks / Trade-offs

- **[Riesgo] El estado desaparece al cerrar el proceso** → Mitigación: documentarlo en la ayuda de la CLI y mantener repositorios detrás de una interfaz simple para poder añadir persistencia más adelante.
- **[Riesgo] Inconsistencia entre préstamo y disponibilidad** → Mitigación: estado derivado del préstamo activo y mutaciones coordinadas en el servicio.
- **[Riesgo] Pruebas dependientes de la hora real** → Mitigación: reloj inyectable con fecha fija en las fixtures.
- **[Riesgo] La CLI duplique validaciones y diverga de la API** → Mitigación: la CLI solo valida aridad y da formato; las reglas de negocio se prueban en el servicio y la CLI prueba los mensajes de error.
- **[Riesgo] Ampliación de alcance durante la implementación** → Mitigación: reservas, multas y persistencia quedan explícitamente fuera del proposal.

## Migration Plan

No aplica: es un proyecto greenfield sin datos ni versiones previas. La reversión consiste en eliminar el paquete `prestamos/`, las pruebas y la configuración creada; no hay datos de usuario que preservar.
