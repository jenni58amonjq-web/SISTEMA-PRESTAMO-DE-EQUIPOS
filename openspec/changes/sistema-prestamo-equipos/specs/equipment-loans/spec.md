# Spec Delta

## Purpose

Gestiona el ciclo de vida de los préstamos de portátiles y proyectores, garantizando que un equipo solo se preste cuando está disponible, que su devolución lo devuelve al inventario y que el estado de cada préstamo pueda consultarse.

## ADDED Requirements

### Requirement: Préstamo de un equipo disponible
El sistema DEBERÁ (SHALL) crear un préstamo activo con fecha al prestar un equipo disponible a un estudiante registrado, cambiando el estado del equipo a `prestado`.

#### Scenario: Prestar un equipo disponible
- **GIVEN** un equipo disponible y un estudiante registrado
- **WHEN** se presta el equipo al estudiante
- **THEN** se crea un préstamo activo con fecha de préstamo y el equipo pasa a estado `prestado`

#### Scenario: Prestar un equipo inexistente
- **WHEN** se intenta prestar un identificador de equipo no registrado
- **THEN** se devuelve un error de equipo no encontrado y no se crea ningún préstamo

#### Scenario: Prestar a un estudiante inexistente
- **GIVEN** un equipo disponible
- **WHEN** se intenta prestarlo a un identificador de estudiante no registrado
- **THEN** se devuelve un error de estudiante no encontrado, no se crea el préstamo y el equipo sigue disponible

#### Scenario: Prestar un equipo ya prestado
- **GIVEN** un equipo con un préstamo activo
- **WHEN** se intenta prestarlo de nuevo
- **THEN** se devuelve un error de equipo no disponible y el préstamo existente permanece activo

### Requirement: Devolución de un préstamo activo
El sistema DEBERÁ (SHALL) cerrar el préstamo activo de un equipo con fecha de devolución y dejar el equipo en estado `disponible`.

#### Scenario: Devolver un equipo prestado
- **GIVEN** un equipo prestado con un préstamo activo
- **WHEN** se devuelve el equipo
- **THEN** el préstamo queda cerrado con fecha de devolución, deja de estar activo y el equipo pasa a estado `disponible`

#### Scenario: Devolver un equipo sin préstamo activo
- **GIVEN** un equipo disponible
- **WHEN** se intenta devolverlo
- **THEN** se devuelve un error de equipo sin préstamo activo y su estado no cambia

#### Scenario: Devolver un equipo inexistente
- **WHEN** se intenta devolver un identificador de equipo no registrado
- **THEN** se devuelve un error de equipo no encontrado

### Requirement: Consulta del estado de los préstamos
El sistema DEBERÁ (SHALL) permitir consultar el préstamo activo de un equipo, los préstamos activos de un estudiante, todos los préstamos activos y el historial de préstamos de un equipo.

#### Scenario: Consultar el estado de un equipo prestado
- **GIVEN** un equipo prestado a un estudiante
- **WHEN** se consulta su estado de préstamo
- **THEN** se obtiene el préstamo activo con el identificador del estudiante y la fecha de préstamo

#### Scenario: Consultar el estado de un equipo disponible
- **GIVEN** un equipo sin préstamo activo
- **WHEN** se consulta su estado de préstamo
- **THEN** se indica que no tiene préstamo activo

#### Scenario: Consultar los préstamos activos de un estudiante
- **GIVEN** un estudiante con dos equipos prestados
- **WHEN** se consultan sus préstamos activos
- **THEN** se obtienen ambos préstamos con sus equipos y fechas

#### Scenario: Consultar todos los préstamos activos
- **GIVEN** un préstamo activo y un equipo disponible
- **WHEN** se consultan todos los préstamos activos
- **THEN** se obtiene únicamente el préstamo activo existente

#### Scenario: Consultar el historial de un equipo
- **GIVEN** un equipo con un préstamo devuelto y otro activo
- **WHEN** se consulta su historial de préstamos
- **THEN** se obtienen ambos préstamos con sus fechas de préstamo y, cuando corresponda, de devolución

### Requirement: Límite de préstamos por estudiante
El sistema NO DEBERÁ (SHALL NOT) limitar la cantidad de préstamos activos por estudiante; la única restricción para prestar es que cada equipo esté disponible.

#### Scenario: Prestar dos equipos al mismo estudiante
- **GIVEN** dos equipos disponibles y un estudiante registrado
- **WHEN** se prestan ambos equipos al mismo estudiante
- **THEN** se crean dos préstamos activos y ambos equipos pasan a estado `prestado`
