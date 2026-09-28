# 04. CAPA 4: CAPA DE TRANSPORTE (TRANSPORT LAYER) - TCP, UDP, PUERTOS Y FLUJO

> **MODELO OSI (OPEN SYSTEMS INTERCONNECTION) - GUIA MAESTRA PARA CERTIFICACIONES**  
> *Guía de referencia técnica y preparación para certificaciones Cisco CCNA 200-301, CompTIA Network+ y Huawei HCIA.*

---


## 1. FUNCION Y PROPOSITO DE LA CAPA DE TRANSPORTE

La Capa de Transporte es el nexo de union entre las capas orientadas a la red
(Capas 1, 2 y 3) y las capas orientadas a las aplicaciones (Capas 5, 6 y 7).

Su responsabilidad es la comunicacion logica entre procesos y aplicaciones que se
ejecutan en diferentes hosts (comunicacion Proceso a Proceso).

Su PDU (Unidad de Datos de Protocolo) es:
- SEGMENTO (Segment) cuando se utiliza el protocolo TCP.
- DATAGRAMA (Datagram) cuando se utiliza el protocolo UDP.

Funciones principales:
- Multiplexacion y Demultiplexacion: Permitir que multiples aplicaciones compartan
  la misma conexion de red simultaneamente utilizando NUMEROS DE PUERTO.
- Segmentacion y Reensamblaje: Dividir grandes bloques de datos de aplicacion en
  trozos pequenos adecuados para la red y reordenarlos en el receptor.
- Confiabilidad y Reenvio de Paquetes Perdidos (en TCP): Garantizar que todo dato
  enviado llegue integro a su destino.
- Control de Flujo: Evitar que un emisor rapido sature el buffer de un receptor lento.
- Control de Congestion: Detectar cuellos de botella en los routers de Internet
  y reducir dinamicamente la tasa de transmision.


## 2. NUMEROS DE PUERTO Y EL CONCEPTO DE SOCKET

Un puerto es un numero de 16 bits (rango: 0 a 65,535) que identifica que programa
o servicio especifico debe recibir la informacion.

Clasificacion Oficial de Puertos (IANA):
| Rango | Nombre | Descripcion |
| :--- | :--- | :--- |
| 0 a 1023 | Puertos Bien Conocidos | Servicios estandar del sistema (HTTP 80, |
| (Well-Known Ports) | HTTPS 443, SSH 22, DNS 53, DHCP 67/68). |  |
| 1024 a 49151 | Puertos Registrados | Asignados a aplicaciones comerciales |
| (Registered Ports) | (MySQL 3306, RDP 3389, SIP 5060). |  |
| 49152 a 65535 | Puertos Dinamicos | Puertos efimeros aleatorios elegidos por |
| (Dynamic / Ephemeral) | los clientes para iniciar una conexion. |  |


El Concepto de SOCKET:
Un Socket es la combinacion unica de una Direccion IP y un Numero de Puerto:
  `192.168.1.50:49152`
Una sesion de red queda univocamente identificada por la Tupla de 5 elementos (5-Tuple):
[ IP Origen, Puerto Origen, IP Destino, Puerto Destino, Protocolo (TCP o UDP) ]


## 3. PROTOCOLO TCP (TRANSMISSION CONTROL PROTOCOL - RFC 793)

TCP es orientado a la conexion, confiable, secuenciado y con control de flujo.

Estructura Completa del Encabezado TCP (20 a 60 Bytes):
| Campo | Bits | Descripcion |
| :--- | :--- | :--- |
| Source Port | 16 bits | Puerto de la aplicacion emisora en el cliente. |
| Destination Port | 16 bits | Puerto del servicio en el servidor (ej. 443 HTTPS). |
| Sequence Number | 32 bits | Numero de secuencia: Rastrea la posicion de cada byte |
| para reconstruir el orden original exacto. |  |  |
| Acknowledgment Num | 32 bits | Numero de Acuse de Recibo (ACK): Indica el siguiente |
| byte que el receptor espera recibir. |  |  |
| Data Offset | 4 bits | Longitud del encabezado TCP (en palabras de 32 bits). |
| Reserved | 3 bits | Reservado para uso futuro. |
| Flags de Control | 9 bits | Banderas de control de la sesion: |
| - SYN (Synchronize): Inicia la conexion y sincroniza numeros de secuencia. |  |  |
| - ACK (Acknowledgment): Indica que el campo Acknowledgment Number es valido. |  |  |
| - FIN (Finish): Cierra la conexion de forma ordenada (no hay mas datos). |  |  |
| - RST (Reset): Aborta y reinicia la conexion de inmediato (error o rechazo). |  |  |
| - PSH (Push): Ordena enviar los datos directo a la app sin esperar el buffer. |  |  |
| - URG (Urgent): Indica que los datos senalados deben procesarse con prioridad. |  |  |
| Window Size | 16 bits | Ventana de Recepcion (Flow Control): Cantidad de bytes |
| que el receptor puede almacenar en su buffer sin desbordarse. |  |  |
| Checksum | 16 bits | Verificacion matematica de integridad de todo el segmento. |
| Urgent Pointer | 16 bits | Puntero de datos urgentes si la bandera URG esta activa. |
| Options / Padding | Variable Parametros opcionales (MSS, Window Scale, SACK). |  |



## 4. EL APRETON DE MANOS DE TRES VIAS DE TCP (THREE-WAY HANDSHAKE)

Antes de transferir un solo byte de datos, TCP establece un canal de comunicacion
mediante el intercambio de tres paquetes:

      Cliente                                    Servidor
         |                                           |
         | -------- 1. [SYN] (Seq=100) ------------> | (Cliente pide conexion)
         |                                           |
         | <--- 2. [SYN, ACK] (Seq=300, Ack=101) --- | (Servidor acepta y sincroniza)
         |                                           |
         | -------- 3. [ACK] (Seq=101, Ack=301) ---> | (Cliente confirma recepcion)
| | | | |
| :--- | :--- |
| | | | |
| | ======= TRANSFERENCIA DE DATOS ========== | |  |


Cierre Ordenado de la Conexion (Four-Way Teardown):
1. Emisor envia `[FIN]` -> 2. Receptor responde `[ACK]`
3. Receptor envia su propio `[FIN]` -> 4. Emisor responde `[ACK]`.


## 5. CONTROL DE FLUJO (SLIDING WINDOW) Y CONTROL DE CONGESTION

### a) Ventana Deslizante (Sliding Window):

   - El receptor anuncia en cada paquete el campo 'Window Size' (ej. 65,535 bytes).
   - El emisor puede enviar rafagas continuas de datos hasta llenar esa ventana
     sin detenerse a esperar una confirmacion por cada paquete individual.
   - Si el buffer del receptor se llena, envia una "Ventana Cero" (Window Size = 0)
     ordenando al emisor que pause de inmediato la transmision.

### b) Control de Congestion:

   - Evita colapsar los routers de la red mediante 4 algoritmos principales:
     Slow Start (inicio lento exponencial), Congestion Avoidance (incremento aditivo),
     Fast Retransmit (retransmision rapida tras 3 ACKs duplicados) y Fast Recovery.


## 6. PROTOCOLO UDP (USER DATAGRAM PROTOCOL - RFC 768)

UDP es un protocolo NO orientado a la conexion, no confiable (Best-Effort), sin
secuenciacion y sin control de flujo.

## Encabezado Ultra-Ligero de UDP (SOLO 8 BYTES):

|  Source Port (16 bits)       |  Destination Port (16 bits)   |
| | | Length (16 bits) | | | Checksum (16 bits) | | |
| :--- | :--- | :--- | :--- | :--- |


¿Por que usar UDP si "no es confiable"?
1. Cero Latencia de Establecimiento: No pierde tiempo negociando un 3-way handshake.
2. Minima Sobrecarga (Overhead): 8 bytes de cabecera vs 20 a 60 bytes de TCP.
3. Ideal para Tiempo Real: En transmisiones de VoIP, videoconferencias o videojuegos
   en linea, si un paquete de audio se pierde, no tiene sentido retransmitirlo 500 ms
   despues porque sonaria con retraso. Es mejor descartarlo y continuar en vivo.
4. Consultas Simples Peticion/Respuesta: DNS, DHCP, SNMP, NTP, TFTP.


## 7. COMPARATIVA EXHAUSTIVA: TCP vs UDP (TABLA DE EXAMEN)

| Caracteristica | TCP | UDP |
| :--- | :--- | :--- |
| Orientacion | Orientado a conexion | No orientado a conexion |
| Confiabilidad | Garantizada (Reenvia perdidos) | No garantizada (Best-Effort) |
| Encabezado | 20 a 60 Bytes | 8 Bytes fijos |
| Orden de Entrega | Garantizado (reensambla por Seq) Sin orden (llegan como salgan) |  |
| Control de Flujo | Si (Window Size) | No |
| Control de Congestion | Si (Slow start / AIMD) | No |
| Velocidad de Transferencia | Mas lenta (mayor control) | Ultrarrapida |
| Transmisiones Soportadas | Solo Unicast (1 a 1) | Unicast, Multicast, Broadcast |
| Protocolos Tipicos | HTTP, HTTPS, SSH, FTP, SMTP, BGP DNS, DHCP, VoIP, TFTP, SNMP |  |



## 8. BANCO DE PREGUNTAS DE EXAMEN (TIPO CCNA / NETWORK+)

### ❓ Pregunta 1
> **Un cliente TCP envia un segmento con numero de secuencia 500 y un**

payload de 200 bytes. ¿Que valor de Acknowledgment Number devolvera el receptor?
Respuesta: 701.
(Explicacion: El receptor confirma los 200 bytes recibidos [500 a 700] y solicita
el siguiente byte esperado: 500 + 200 + 1 = 701).

### ❓ Pregunta 2
> **¿Cual de los siguientes protocolos de aplicacion utiliza TCP y UDP en el puerto 53?**

Respuesta: DNS (Domain Name System).
(Explicacion: Utiliza UDP 53 para consultas y resoluciones normales de nombres
por velocidad, pero utiliza TCP 53 para transferencias de zona [Zone Transfers]
entre servidores DNS debido a la necesidad de confiabilidad).

