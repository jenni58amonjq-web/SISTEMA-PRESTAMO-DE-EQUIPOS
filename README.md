# Sistema de préstamo de equipos universitarios

Aplicación Python para registrar portátiles y proyectores, registrar estudiantes, prestar equipos disponibles, devolverlos y consultar su estado. El núcleo es una API Python (`src/prestamos`) con dos interfaces: una CLI de consola y una interfaz gráfica con tkinter.

## Requisitos

- Python 3.10 o superior.
- pytest para ejecutar las pruebas.
- tkinter para la interfaz gráfica (incluido en las instalaciones estándar de Python en Windows y macOS; en Linux puede requerir `python3-tk`).

Instalar pytest si no está disponible:

```bash
python -m pip install pytest
```

## Ejecutar las pruebas

```bash
python -m pytest -q
```

La suite cubre las 41 pruebas unitarias derivadas de las especificaciones OpenSpec.

## Ejecutar la interfaz gráfica

Desde la raíz del proyecto:

```bash
python gui.py
```

La ventana permite registrar equipos y estudiantes, prestar, devolver y ver tres listas actualizadas (equipos con su estado, estudiantes y préstamos activos). Comparte el mismo `LoanService` que la CLI; el estado se mantiene mientras la ventana esté abierta.

## Ejecutar la CLI

Desde la raíz del proyecto:

```bash
python main.py
```

También se puede ejecutar como módulo:

```bash
python -m prestamos
```

Si se usa el módulo directamente, hay que añadir `src` al path de Python:

```bash
# Windows (PowerShell)
$env:PYTHONPATH = "src"
python -m prestamos
```

```bash
# macOS / Linux
PYTHONPATH=src python -m prestamos
```

## Comandos de la CLI

| Comando | Uso |
| --- | --- |
| `registrar-equipo` | `registrar-equipo LAP-001 laptop "Portátil lab 1"` |
| `registrar-estudiante` | `registrar-estudiante 202312345 "Ana Torres"` |
| `prestar` | `prestar LAP-001 202312345` |
| `devolver` | `devolver LAP-001` |
| `listar-equipos` | Muestra inventario con tipo y estado |
| `estado` | `estado LAP-001` |
| `prestamos-activos` | Muestra todos los préstamos abiertos |
| `historial` | `historial LAP-001` |
| `ayuda` | Lista comandos y sintaxis |
| `salir` | Termina la sesión |

Ejemplo de sesión:

```text
registrar-equipo LAP-001 laptop "Portátil lab 1"
registrar-estudiante 202312345 "Ana Torres"
prestar LAP-001 202312345
estado LAP-001
devolver LAP-001
```

## Estado en memoria

Equipos, estudiantes y préstamos viven solo en memoria: se conservan durante una sesión de la CLI o mientras la ventana gráfica esté abierta, y se descartan al salir o reiniciar el proceso. No hay base de datos ni archivos de datos.

## Especificaciones

Las specs SDD están en `openspec/changes/sistema-prestamo-equipos/`: `proposal.md`, los deltas en `specs/`, `design.md` y `tasks.md`.
