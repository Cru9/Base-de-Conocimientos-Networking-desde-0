# 01. CLASIFICACION Y MARCADO DE PAQUETES: COS (CAPA 2) Y DSCP (CAPA 3)

> **CALIDAD DE SERVICIO Y CONFORMACION DE TRAFICO (QOS & TRAFFIC SHAPING)**


---



## 1. MARCADO EN CAPA DE ENLACE: ETHERNET 802.1Q CoS (CAPA 2)

Dentro de la etiqueta IEEE 802.1Q (utilizada en enlaces troncales VLAN), existen
3 bits denominados PCP (Priority Code Point) o CoS (Class of Service).

Al disponer de 3 bits, permite definir 8 niveles de prioridad (del 0 al 7):


| Valor CoS | Nombre Estandar | Tipo de Trafico Asignado |
| :--- | :--- | :--- |
| CoS 0 | Best Effort | Trafico normal de datos no clasificado (Default) |
| CoS 1 | Background | Respaldos masivos, descargas no criticas |
| CoS 2 | Standard | Trafico corporativo general |
| CoS 3 | Critical Data | Aplicaciones transaccionales (ERP, SQL) |
| CoS 4 | Video | Videoconferencias interactivas y streaming |
| CoS 5 | Voice | Trafico de Audio en tiempo real (RTP de VoIP) |
| CoS 6 | Internetwork Control | Protocolos de enrutamiento (OSPF, BGP, STP) |
| CoS 7 | Network Control | Reservado para control de red de maxima prioridad |


LIMITACION CRITICA DE CoS:
- La etiqueta CoS solo existe fisicamente en tramas Ethernet que tienen una cabecera
  802.1Q (enlaces troncales).
- En cuanto el paquete cruza un puerto enrutado de Capa 3 (un router o firewall)
  o entra a un enlace WAN o Internet, la cabecera Ethernet original se destruye
  y la marca CoS se pierde para siempre.



## 2. MARCADO EN CAPA DE RED: IP PRECEDENCE Y DIFFSERV DSCP (CAPA 3)

Para que la marca de calidad de servicio sobreviva a traves de routers, nubes y
enlaces WAN, el marcado debe residir dentro de la cabecera del paquete IP.

EVOLUCION DEL BYTE "TYPE OF SERVICE" (ToS):
- En el estandar original IPv4 (RFC 791), se utilizaban los primeros 3 bits
  denominados "IP Precedence" (IPP 0 al 7).
- En el estandar moderno DiffServ (RFC 2474), el byte ToS se redefinio:
  * Los primeros 6 bits se denominan DSCP (Differentiated Services Code Point),
    permitiendo 64 valores de clasificacion (del 0 al 63).
  * Los ultimos 2 bits se denominan ECN (Explicit Congestion Notification / RFC 3168).

```text
  +-----------------------------------+-------+
  |        DSCP (6 bits)              |  ECN  |
  |  b5   b4   b3   b2   b1   b0      | b1 b0 |
  +-----------------------------------+-------+
```


## 3. CATEGORIAS Y VALORES ESTANDAR DE DSCP


### a) Default Forwarding (DF):

   - Valor: DSCP 0 (Binario `000000`).
   - Equivale al servicio clasico "Best Effort".


### b) Class Selector (CS1 a CS7):

   - Creados para garantizar 100% de compatibilidad retrospectiva con IP Precedence.
   - Formula: DSCP Decimal = 8 * IP Precedence (Terminan en binario `xxx000`).
   - CS1 (DSCP 8)  : Trafico Scavenger (degradado).
   - CS2 (DSCP 16) : Gestion de red (OAM, SSH, SNMP).
   - CS3 (DSCP 24) : Senalizacion telefonica (SIP / H.323).
   - CS4 (DSCP 32) : Video interactivo o broadcast.
   - CS5 (DSCP 40) : Transmision de video de alta prioridad.
   - CS6 (DSCP 48) : Protocolos de enrutamiento (OSPF, BGP, EIGRP).
   - CS7 (DSCP 56) : Control interno critico de infraestructura.


### c) Assured Forwarding (AFxy - RFC 2597):

   - Define 4 clases de servicio (x = 1, 2, 3, 4) y 3 niveles de descarte (y = 1, 2, 3).
   - Formula de conversion: DSCP Decimal = 8*x + 2*y

```text
   +----------------+---------------+---------------+---------------+
   |                | Descarte Bajo | Descarte Med. | Descarte Alto |
   |                |  (Drop Low)   |  (Drop Med)   |  (Drop High)  |
   +----------------+---------------+---------------+---------------+
   | Clase 1 (Bulk) | AF11 (DSCP 10)| AF12 (DSCP 12)| AF13 (DSCP 14)|
   | Clase 2 (Trans)| AF21 (DSCP 18)| AF22 (DSCP 20)| AF23 (DSCP 22)|
   | Clase 3 (Sign) | AF31 (DSCP 26)| AF32 (DSCP 28)| AF33 (DSCP 30)|
   | Clase 4 (Video)| AF41 (DSCP 34)| AF42 (DSCP 36)| AF43 (DSCP 38)|
   +----------------+---------------+---------------+---------------+
```

   REGLA DE ORO: A mayor numero 'y', mayor probabilidad de que el router descarte
   el paquete en caso de congestion (ej. si se satura el buffer, AF43 se descarta
   mucho antes que AF41).


### d) Expedited Forwarding (EF - RFC 3246):

   - Valor: DSCP 46 (Binario `101110`).
   - Maxima prioridad estandar de la industria para datos de usuario.
   - Ofrece minima latencia, minimo jitter y cero descarte.
   - RESERVADO EXCLUSIVAMENTE PARA EL AUDIO DE TELEFONIA IP (RTP Streams).



## 4. TABLA DE MAPEO RECOMENDADA: CoS (CAPA 2) A DSCP (CAPA 3)

Cuando un switch recibe una trama con etiqueta CoS y la enruta a Capa 3, debe
reescribir la marca hacia el campo DSCP siguiendo este estandar:


| CoS (L2) | DSCP Equivalente | Tipo de Aplicacion |
| :--- | :--- | :--- |
| CoS 0 | DSCP 0 (DF) | Trafico general de datos (Web, correo, descargas) |
| CoS 1 | DSCP 8 (CS1) | Trafico Scavenger (P2P, backups no prioritarios) |
| CoS 2 | DSCP 18 (AF21) | Datos transaccionales (Bases de datos, SAP) |
| CoS 3 | DSCP 26 (AF31) | Senalizacion de llamadas de voz (SIP / H.323) |
| CoS 4 | DSCP 34 (AF41) | Videoconferencia interactiva (Zoom, Teams, Webex) |
| CoS 5 | DSCP 46 (EF) | Medios de Voz en Tiempo Real (RTP VoIP) |
| CoS 6 | DSCP 48 (CS6) | Control de Red (OSPF Hello, BGP Keepalive) |
| CoS 7 | DSCP 56 (CS7) | Control de Hardware / BPDU STP |
