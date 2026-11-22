# Proposal

## Why

La universidad necesita llevar el control de sus portátiles y proyectores: hoy no existe un registro único que indique qué equipo está prestado, a qué estudiante y cuándo se devolvió. Un núcleo pequeño y verificable con TDD permite confiar en esas reglas antes de conectar cualquier interfaz o almacenamiento.

## What Changes

- Registrar equipos de los tipos `laptop` y `projector` con identificador único y estado inicial `disponible`.
- Registrar estudiantes con identificador único y datos básicos.
- Prestar solo equipos existentes y disponibles, asociando el préstamo a un estudiante existente y registrando la fecha.
- Devolver solo equipos que estén prestados, cerrando el préstamo activo y dejando el equipo disponible.
- Consultar el estado de un equipo, los préstamos activos de un estudiante y el listado de préstamos activos.
- Exponer las operaciones anteriores como API Python y como CLI interactiva sobre el mismo servicio en memoria.
- Definir la estrategia TDD con pytest: pruebas de dominio primero, luego pruebas de la CLI.
- Fuera de alcance: persistencia en disco o base de datos, autenticación, concurrencia entre procesos, reservas, fechas límite, multas y notificaciones.

## Capabilities

### New Capabilities

- `equipment-catalog`: registro, validación y consulta del inventario de portátiles y proyectores, incluido su estado de disponibilidad.
- `student-registry`: registro y consulta de estudiantes con identificador único.
- `equipment-loans`: préstamo de equipos disponibles, devolución y consulta del estado e historial de préstamos.
- `loan-cli`: interfaz interactiva de terminal que expone las operaciones del dominio con mensajes y errores verificables.

### Modified Capabilities

Ninguna. El proyecto no tiene specs existentes.

## Impact

- Proyecto greenfield: se crean el paquete Python, las pruebas pytest y la configuración mínima del entorno de desarrollo.
- Sin dependencias de producción externas: la API y la CLI usan solo la biblioteca estándar (`dataclasses`, `datetime`, `cmd`); pytest se usa únicamente en desarrollo.
- El estado es volátil por decisión explícita: se reinicia al arrancar el proceso y se conserva durante una sesión interactiva de la CLI.
- La API es la fuente de verdad de las reglas de negocio; la CLI es una capa delgada que no duplica validaciones.
