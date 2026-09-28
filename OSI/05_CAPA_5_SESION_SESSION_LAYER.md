# 05. CAPA 5: CAPA DE SESION (SESSION LAYER) - DIALOGOS, SINCRONIZACION Y CONTROL

> **MODELO OSI (OPEN SYSTEMS INTERCONNECTION) - GUIA MAESTRA PARA CERTIFICACIONES**  
> *Guía de referencia técnica y preparación para certificaciones Cisco CCNA 200-301, CompTIA Network+ y Huawei HCIA.*

---


## 1. FUNCION Y PROPOSITO DE LA CAPA DE SESION

La Capa de Sesion es responsable de iniciar, mantener, sincronizar, coordinar
y finalizar los dialogos (sesiones) entre aplicaciones de dos computadoras remotas.

Mientras que la Capa 4 (Transporte) se encarga de mover los segmentos de red de
forma confiable, la Capa 5 se asegura de que la conversación logica entre ambos
extremos tenga sentido, sepa de quien es el turno para hablar y pueda recuperarse
si ocurre una interrupcion temporal.

Su PDU (Unidad de Datos de Protocolo) es: DATOS (Data).


## 2. FUNCIONES PRINCIPALES DE LA CAPA DE SESION

### a) Control del Dialogo (Dialog Control):

   Determina la modalidad de comunicacion entre ambas partes:
   - Simplex: La comunicacion fluye en una unica direccion (unidireccional).
     Ejemplo: Telemetria de sensores, transmision de radio.
   - Semiduplex (Half-Duplex / Two-Way Alternate): La comunicacion fluye en ambas
     direcciones pero un solo dispositivo transmite a la vez. Se utiliza un testigo
     o token de control de dialogo.
   - Duplex Completo (Full-Duplex / Two-Way Simultaneous): Ambos dispositivos
     pueden transmitir y recibir simultaneamente.

### b) Sincronizacion y Puntos de Control (Checkpointing):

   Permite insertar puntos de control (checkpoints) dentro de un flujo continuo de datos:
   - Puntos de Sincronizacion Menores: Marcas periódicas que validan bloques de datos.
   - Puntos de Sincronizacion Mayores: Confirmacion formal de fases completadas.
   *Ejemplo practico de examen: Si estas descargando un archivo de 2 GB y la conexion
    se corta al 90% (1.8 GB), la Capa de Sesion permite reanudar la descarga exactamente
    desde el ultimo punto de control guardado, evitando tener que empezar desde 0.

### c) Agrupamiento y Separacion de Flujos (Session Multiplexing):

   Permite que un usuario mantenga abiertas multiples sesiones simultaneas contra
   el mismo servidor remoto (por ejemplo, varias consultas independientes a una
   misma base de datos SQL) sin que las respuestas se mezclen.


## 3. PROTOCOLOS Y TECNOLOGIAS ASOCIADAS A LA CAPA 5

- NetBIOS (Network Basic Input/Output System):
  Protocolo clasico de Microsoft que maneja nombres de red y sesiones de archivos
  (Puerto TCP 139 - NetBIOS Session Service).
- RPC (Remote Procedure Call):
  Permite que un programa en una computadora ejecute un procedimiento o subrutina
  en otra computadora remota como si fuera local (base de Active Directory y NFS).
- SIP (Session Initiation Protocol - RFC 3261):
  El protocolo estandar de la telefonia IP (VoIP) y videoconferencia. Responsable
  de iniciar la sesion de llamada (ringing), negociar codecs, gestionar transferencias
  y terminar la llamada (BYE).
- PPTP (Point-to-Point Tunneling Protocol):
  Maneja el canal de control y establecimiento de sesiones en tuneles VPN.
- SOCKS (SOCKS4 / SOCKS5):
  Protocolo de proxy que establece y gestiona circuitos virtuales de sesion entre
  clientes y servidores a traves de firewalls.
- NFS (Network File System):
  Gestiona la sesion y montaje de carpetas compartidas en red para entornos Linux/Unix.


## 4. LA CAPA DE SESION EN EL MUNDO REAL (OSI vs TCP/IP)

¿Por que la Capa 5 no existe como tal en el modelo practico TCP/IP?
En el modelo TCP/IP de Internet, las funciones de sesion fueron absorbidas por las
propias aplicaciones:
- Las aplicaciones web modernas gestionan sus sesiones mediante Cookies HTTP,
  tokens criptograficos (JWT - JSON Web Tokens) y conexiones persistentes WebSocket.
- Los protocolos de transporte como TCP ya proveen inicio y cierre de conexion.
Por ello, en el modelo TCP/IP, las capas 5, 6 y 7 se agrupan en una sola capa llamada
simplemente "Capa de Aplicacion".


## 5. PREGUNTAS CLAVE DE EXAMEN (TIPO CERTIFICACION)

### ❓ Pregunta 1
> **¿Cual es la funcion principal del mecanismo de Checkpointing en la Capa 5?**

Respuesta: Permite insertar puntos de sincronizacion en la transferencia de datos
para reanudar la transmision desde la ultima marca valida en caso de falla de conexion,
sin tener que reenviar la totalidad de los datos desde el inicio.

### ❓ Pregunta 2
> **¿En que capa del modelo OSI opera el protocolo SIP (Session Initiation Protocol)**

para senalizar y establecer llamadas de VoIP?
Respuesta: En la Capa 5 (Capa de Sesion), aunque interactua estrechamente con la Capa 7
en el modelo TCP/IP.

