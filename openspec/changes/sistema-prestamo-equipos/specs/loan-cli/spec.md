# Spec Delta

## Purpose

Ofrece una sesión interactiva de terminal para registrar equipos y estudiantes, prestar y devolver equipos y consultar estados sin duplicar las reglas de negocio, manteniendo el estado en memoria durante la sesión.

## ADDED Requirements

### Requirement: Sesión interactiva con estado en memoria
La CLI DEBERÁ (SHALL) aceptar comandos hasta que se ingrese `salir`, conservando el estado de equipos, estudiantes y préstamos durante esa sesión y descartándolo al iniciar una nueva.

#### Scenario: Mantener el estado entre comandos de una sesión
- **GIVEN** una sesión de CLI iniciada
- **WHEN** se registra un equipo, se registra un estudiante y se presta el equipo en comandos sucesivos
- **THEN** una consulta posterior de estado muestra el equipo prestado al estudiante

#### Scenario: Estado vacío al iniciar una nueva sesión
- **GIVEN** una sesión anterior que registró equipos
- **WHEN** se inicia una nueva sesión y se consulta el inventario
- **THEN** el inventario aparece vacío

### Requirement: Comandos de gestión disponibles
La CLI DEBERÁ (SHALL) ofrecer comandos para registrar equipos y estudiantes, prestar equipos, devolverlos y finalizar la sesión, con mensajes de confirmación en caso de éxito.

#### Scenario: Registrar un equipo desde la CLI
- **WHEN** se ejecuta `registrar-equipo LAP-001 laptop "Portátil lab 1"`
- **THEN** se muestra una confirmación y el equipo queda disponible en la sesión

#### Scenario: Registrar un estudiante desde la CLI
- **WHEN** se ejecuta `registrar-estudiante 202312345 "Ana Torres"`
- **THEN** se muestra una confirmación y el estudiante queda registrado en la sesión

#### Scenario: Prestar un equipo desde la CLI
- **GIVEN** un equipo disponible y un estudiante registrado en la sesión
- **WHEN** se ejecuta `prestar LAP-001 202312345`
- **THEN** se muestra una confirmación con el identificador del préstamo y el equipo pasa a prestado

#### Scenario: Devolver un equipo desde la CLI
- **GIVEN** un equipo prestado en la sesión
- **WHEN** se ejecuta `devolver LAP-001`
- **THEN** se muestra una confirmación y el equipo pasa a disponible

#### Scenario: Finalizar la sesión
- **WHEN** se ejecuta `salir`
- **THEN** la CLI deja de aceptar comandos y termina sin error

### Requirement: Consultas de estado desde la CLI
La CLI DEBERÁ (SHALL) permitir consultar el inventario, el estado de un equipo, los préstamos activos y el historial de un equipo, mostrando la información de forma legible.

#### Scenario: Consultar el inventario
- **GIVEN** dos equipos registrados en la sesión
- **WHEN** se ejecuta `listar-equipos`
- **THEN** se muestran ambos equipos con su identificador, tipo y estado

#### Scenario: Consultar un equipo prestado
- **GIVEN** un equipo prestado en la sesión
- **WHEN** se ejecuta `estado LAP-001`
- **THEN** se muestra el estado `prestado`, el estudiante y la fecha de préstamo

#### Scenario: Consultar préstamos activos
- **GIVEN** un préstamo activo en la sesión
- **WHEN** se ejecuta `prestamos-activos`
- **THEN** se muestra el préstamo con equipo, estudiante y fecha

#### Scenario: Consultar el historial de un equipo
- **GIVEN** un equipo con un préstamo devuelto en la sesión
- **WHEN** se ejecuta `historial LAP-001`
- **THEN** se muestra el préstamo con sus fechas de préstamo y devolución

### Requirement: Errores y ayuda de la CLI
La CLI DEBERÁ (SHALL) mostrar errores de validación o de reglas de negocio en la salida de error sin interrumpir la sesión, y ofrecer ayuda para comandos desconocidos o mal formados.

#### Scenario: Error de negocio no interrumpe la sesión
- **GIVEN** un equipo ya prestado en la sesión
- **WHEN** se ejecuta `prestar LAP-001 202312345`
- **THEN** se muestra el error en la salida de error, el equipo sigue prestado y la CLI acepta nuevos comandos

#### Scenario: Comando desconocido
- **WHEN** se ejecuta un comando no reconocido
- **THEN** se muestra un mensaje de ayuda con los comandos disponibles y la sesión continúa

#### Scenario: Argumentos insuficientes
- **WHEN** se ejecuta `prestar` sin identificadores
- **THEN** se muestra el uso correcto del comando en la salida de error y no se crea ningún préstamo

#### Scenario: Ayuda explícita
- **WHEN** se ejecuta `ayuda`
- **THEN** se listan los comandos disponibles y su sintaxis
