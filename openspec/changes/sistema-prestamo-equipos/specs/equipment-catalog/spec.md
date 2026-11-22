# Spec Delta

## Purpose

Define el inventario de equipos universitarios y su estado de disponibilidad para que el servicio de préstamos pueda decidir qué equipos pueden prestarse y para informar la situación de cada uno.

## ADDED Requirements

### Requirement: Registro de equipos con tipo válido
El sistema DEBERÁ (SHALL) permitir registrar equipos de los tipos `laptop` o `projector` con un identificador, datos descriptivos opcionales y estado inicial `disponible`.

#### Scenario: Registrar un portátil
- **WHEN** se registra un equipo con identificador `LAP-001`, tipo `laptop` y una descripción
- **THEN** el equipo queda almacenado con estado `disponible` y conserva su tipo y descripción

#### Scenario: Registrar un proyector
- **WHEN** se registra un equipo con identificador `PRO-001` y tipo `projector`
- **THEN** el equipo queda almacenado con estado `disponible`

#### Scenario: Rechazar un tipo de equipo no soportado
- **WHEN** se intenta registrar un equipo con un tipo distinto de `laptop` o `projector`
- **THEN** el registro se rechaza con un error de validación y el equipo no queda almacenado

### Requirement: Identificador de equipo único
El sistema DEBERÁ (SHALL) rechazar el registro de un equipo cuyo identificador ya esté en uso, sin alterar el equipo existente.

#### Scenario: Registrar un identificador duplicado
- **GIVEN** un equipo registrado con identificador `LAP-001`
- **WHEN** se intenta registrar otro equipo con el mismo identificador
- **THEN** se devuelve un error de registro duplicado y el equipo original conserva sus datos

### Requirement: Consulta del inventario y del estado de un equipo
El sistema DEBERÁ (SHALL) permitir listar todo el inventario y consultar, para un identificador dado, si el equipo está `disponible` o `prestado`.

#### Scenario: Listar el inventario vacío
- **WHEN** se consulta el inventario antes de registrar equipos
- **THEN** se obtiene una lista vacía

#### Scenario: Listar equipos registrados
- **GIVEN** dos equipos registrados
- **WHEN** se consulta el inventario
- **THEN** se obtienen ambos equipos con sus identificadores, tipos y estados

#### Scenario: Consultar un equipo inexistente
- **WHEN** se consulta el estado de un identificador no registrado
- **THEN** se devuelve un error de equipo no encontrado
