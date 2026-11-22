# Spec Delta

## Purpose

Registra a los estudiantes que pueden recibir equipos en préstamo y permite consultarlos, garantizando que cada identificador represente a una única persona dentro del sistema.

## ADDED Requirements

### Requirement: Registro de estudiantes
El sistema DEBERÁ (SHALL) permitir registrar estudiantes con un identificador único y un nombre, rechazando datos vacíos.

#### Scenario: Registrar un estudiante
- **WHEN** se registra un estudiante con identificador `202312345` y nombre `Ana Torres`
- **THEN** el estudiante queda almacenado con esos datos

#### Scenario: Rechazar identificador o nombre vacío
- **WHEN** se intenta registrar un estudiante con identificador o nombre vacío
- **THEN** el registro se rechaza con un error de validación y no se almacena el estudiante

#### Scenario: Rechazar identificador duplicado
- **GIVEN** un estudiante registrado con identificador `202312345`
- **WHEN** se intenta registrar otro estudiante con el mismo identificador
- **THEN** se devuelve un error de registro duplicado y el estudiante original conserva sus datos

### Requirement: Consulta de estudiantes
El sistema DEBERÁ (SHALL) permitir obtener los datos de un estudiante a partir de su identificador y listar los estudiantes registrados.

#### Scenario: Consultar un estudiante existente
- **GIVEN** un estudiante registrado con identificador `202312345`
- **WHEN** se consulta ese identificador
- **THEN** se obtienen su nombre y su identificador

#### Scenario: Consultar un estudiante inexistente
- **WHEN** se consulta un identificador de estudiante no registrado
- **THEN** se devuelve un error de estudiante no encontrado

#### Scenario: Listar estudiantes registrados
- **GIVEN** dos estudiantes registrados
- **WHEN** se consulta el listado de estudiantes
- **THEN** se obtienen ambos con sus identificadores y nombres
