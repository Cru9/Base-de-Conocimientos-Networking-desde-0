# 01. REDES MOVILES 4G LTE, 5G NR Y OPEN RAN (O-RAN)

> **TELECOMUNICACIONES AVANZADAS, REDES DE CARRIER E INFRAESTRUCTURA GLOBAL**


---



## 1. EVOLUCION CELULAR: DE LA ARQUITECTURA MONOLITICA A LA NUBE

Las redes celulares han evolucionado de sistemas basados en hardware propietario
cerrado hacia arquitecturas virtualizadas, nativas en la nube y desagregadas:


| Generacion | Red de Acceso (RAN) | Nucleo de Red (Core) | Velocidades / Latencia |
| :--- | :--- | :--- | :--- |
| 4G LTE | eNodeB (Monolitico) | EPC (Monolitico / HW) | 100-300 Mbps / ~30-50 ms |
| 5G NSA | gNodeB + eNodeB | EPC Mejorado (4G Core) | 1 Gbps / ~20 ms |
| 5G SA | gNodeB Desagregado | 5G Core SBA (Cloud) | 10-20 Gbps / < 1 ms (URLLC) |




## 2. ARQUITECTURA 4G LTE EPC (EVOLVED PACKET CORE)

La red 4G LTE separa la estacion base de radio (eNodeB) del nucleo de paquetes (EPC):

```text
+--------+   S1-MME (SCTP/S1AP)  +-----+       S6a (Diameter)      +-----+
| eNodeB | --------------------> | MME | ------------------------> | HSS |
+--------+                       +-----+                           +-----+
    |                               |
    | S1-U (GTP-U)                  | S11 (GTP-C)
    v                               v
+--------------------------------------+       Gx (Diameter)       +------+
|     SERVING GATEWAY (SGW)            | ------------------------> | PCRF |
+--------------------------------------+                           +------+
    |
    | S5/S8 (GTP-U / GTP-C)
    v
+--------------------------------------+       SGi (IP Trafico)    +---------------+
|     PACKET DATA GATEWAY (PGW)        | ------------------------> | INTERNET / IP |
+--------------------------------------+                           +---------------+

Funciones de los Nodos 4G:
1. MME (Mobility Management Entity):
   - Cerebro del Plano de Control. Gestiona la autenticacion del usuario con el HSS,
     el estado inactivo/activo (Paging), y el traspaso entre antenas (Handover).
2. SGW (Serving Gateway):
   - Enrutador local del Plano de Usuario. Actua como ancla de movilidad cuando el
     telefono se mueve entre diferentes eNodeBs dentro de la misma region.
3. PGW (Packet Data Network Gateway):
   - Punto de anclaje final hacia Internet o redes corporativas. Asigna la direccion IP
     publica/privada al telefono y aplica politicas de tarificacion (Charging).
4. HSS (Home Subscriber Server):
   - Base de datos maestra con los perfiles de todos los abonados (clave criptografica K,
     IMSI, servicios contratados).
5. PCRF (Policy and Charging Rules Function):
   - Determina las reglas de calidad de servicio (QoS) y limites de velocidad segun el plan.
```


## 3. ARQUITECTURA 5G CORE SBA (SERVICE-BASED ARCHITECTURE)

El estandar 5G Standalone (3GPP Release 15/16/17) abandona los nodos de hardware
dedicados y adopta una arquitectura de microservicios nativa en contenedores (Cloud-Native):

DIAGRAMA DEL 5G CORE (SBA):

```text
                      +------+   +------+   +------+
                      | NRF  |   | NSSF |   | NEF  |
                      +------+   +------+   +------+
                         |          |          |
   ================ BUS DE COMUNICACION SBI (HTTP/2 REST / JSON) ================
        |           |           |           |           |           |
     +-----+     +-----+     +-----+     +-----+     +-----+     +-----+
     | AMF |     | SMF |     | UDM |     | AUSF|     | PCF |     | UDR |
     +-----+     +-----+     +-----+     +-----+     +-----+     +-----+
        |           |
    N1/N2 (NAS/NGAP)| N4 (PFCP)
        |           v
   +--------+  N3  +-----------------+  N6  +--------------------------------+
   | gNodeB | ===> |       UPF       | ===> | RED DE DATOS (DN / INTERNET /  |
   | (5G NR)| GTP-U| (User Plane Fn) |      | SERVIDORES EDGE COMPUTING MEC) |
   +--------+      +-----------------+      +--------------------------------+

Funciones de Red Cloud-Native (NFs):
- AMF (Access and Mobility Management Function): Gestiona el registro y movilidad del telefono (reemplazo del MME).
- SMF (Session Management Function): Controla la creacion, modificacion y liberacion de sesiones PDU (IP).
- UPF (User Plane Function): UNICO nodo del Plano de Usuario. Procesa paquetes IP a velocidades de cientos de Gbps.
  Se puede desplegar en el borde (MEC - Multi-Access Edge Computing) junto a la antena para lograr latencias < 1 ms.
- NRF (Network Repository Function): Motor de descubrimiento (Service Discovery). Cuando el AMF necesita un SMF,
  consulta al NRF mediante API REST: GET /nnrf-disc/v1/nf-instances.
- UDM (Unified Data Management): Almacena credenciales de seguridad y perfiles de suscripcion (sucesor del HSS).
- AUSF (Authentication Server Function): Ejecuta el algoritmo criptografico 5G AKA con la tarjeta SIM/eSIM.
```


## 4. 5G NEW RADIO (NR): FRECUENCIAS, NUMEROLOGIAS Y MASSIVE MIMO

1. Rangos de Frecuencia (FR):
   - FR1 (Sub-6 GHz: 410 MHz a 7.125 GHz):
     * Banda n78 (3.5 GHz): La banda dorada global de 5G (equilibrio entre cobertura y velocidad de 1 Gbps).
     * Banda n28 (700 MHz): Banda baja para penetracion profunda en interiores y cobertura rural extensa.
   - FR2 (mmWave / Ondas Milimetricas: 24.25 GHz a 71.0 GHz):
     * Bandas n257 (28 GHz) y n258 (26 GHz): Anchos de banda masivos de hasta 800 MHz (velocidades de 4 a 10 Gbps)
       con alcance limitado a 200-500 metros (ideal para estadios, aeropuertos y fabricas inteligentes).

2. Numerologias Flexibles (SCS - Subcarrier Spacing):
   A diferencia de 4G (donde el espaciado entre subportadoras era fijo a 15 kHz), 5G NR es escalable:
   * mu=0: SCS = 15 kHz (Slot = 1 ms)   -> Ideal para bandas bajas (cobertura amplia).
   * mu=1: SCS = 30 kHz (Slot = 0.5 ms) -> Estandar para Banda n78 (3.5 GHz).
   * mu=2: SCS = 60 kHz (Slot = 0.25 ms)-> Bandas medias/altas con baja latencia.
   * mu=3: SCS = 120 kHz (Slot = 0.125 ms) -> mmWave FR2 (ultra baja latencia).

3. Massive MIMO y Beamforming Activo (64T64R):
   - Las antenas 5G contienen matrices de 64 o 128 pequenos elementos radiantes independientes.
   - En lugar de iluminar un sector ciego de 120 grados como en 4G, el sistema calcula la fase
     electromagnetica para concentrar un haz estrecho de radio (Beamforming 3D) que persigue
     dinamicamente al usuario en movimiento, multiplicando la capacidad por diez sin usar mas espectro.



## 5. OPEN RAN (O-RAN ALLIANCE): DESAGREGACION DE LA ESTACION BASE

Historicamente, un operador compraba la estacion base como una "caja negra" propietaria
a un unico fabricante (Huawei, Ericsson o Nokia).

Open RAN desagrega la estacion base en tres componentes modulares con interfaces abiertas:

      [ ANTENA / TORRE ]                   [ SITE LOCAL / EDGE ]             [ DATACENTER REGIONAL ]
```text
   +-----------------------+              +---------------------+           +------------------------+
   |  RU (Radio Unit)      | <== eCPRI == | DU (Distributed Un.)| <== F1 == | CU (Centralized Unit)  |
   | - Transceptores RF    |    (Fibra    | - Capa Fisica L1    |   (IP/    | - CU-CP: Control Plane |
   | - Conversion Digital  |   Ethernet)  | - Control MAC / RLC |   SCTP)   | - CU-UP: User Plane    |
   | - Fabricante A        |              | - Servidor x86/COTS |           | - Servidores en Cloud  |
   +-----------------------+              +---------------------+           +------------------------+
                                                    ^                                   ^
                                                    | Interfaz E2                       | Interfaz E2
                                                    +-----------------+-----------------+
                                                                      |
                                                       +-------------------------------+
                                                       |      Near-RT RIC (xApps)      |
                                                       | (RAN Intelligent Controller)  |
                                                       | - Optimizacion de Radio con IA|
                                                       +-------------------------------+

1. eCPRI (enhanced Common Public Radio Interface):
   - Protocolo estandarizado para transmitir datos de radio digitalizados en paquetes Ethernet
     estandar de 10G/25G/100G entre la antena (RU) y el procesador de banda base (DU).
   - Requiere sincronizacion estricta de fase mediante PTP (IEEE 1588v2 Telecom Profile G.8275.1).

2. RAN Intelligent Controller (RIC):
   - Cerebro de Inteligencia Artificial que ejecuta micro-aplicaciones (xApps y rApps) para
     gestionar interferencias, balancear usuarios y apagar sectores inactivos para ahorrar energia.
```


## 6. NETWORK SLICING DE EXTREMO A EXTREMO

Network Slicing permite crear multiples redes logicas virtuales e independientes sobre
la misma infraestructura fisica de fibra y radio:

Identificador de Slice: S-NSSAI = SST (Slice/Service Type) + SD (Slice Differentiator)

1. Slice eMBB (Enhanced Mobile Broadband - SST 1):
   - Prioridad: Maximo ancho de banda y velocidad de descarga (Video 8K, Realidad Virtual).
2. Slice URLLC (Ultra-Reliable Low-Latency Communication - SST 2):
   - Prioridad: Latencia < 1 milisegundo y fiabilidad del 99.9999% (Cirugia remota, vehiculos autonomos).
   - El plano de usuario (UPF) se aprovisiona en servidores Edge (MEC) junto a la antena.
3. Slice mMTC (Massive Machine-Type Communication - SST 3):
   - Prioridad: Conectar hasta 1,000,000 de dispositivos IoT por kilometro cuadrado (Medidores de gas, agua).



## 7. PROTOCOLOS DE TRANSPORTE Y DIAGNOSTICO EN REDES MOVILES

1. GTP-U (GPRS Tunneling Protocol User Plane - UDP puerto 2152):
   - Todo el trafico de datos que navega un celular viaja encapsulado en tuneles GTP-U.
   - Cada sesion de datos se identifica por un TEID (Tunnel Endpoint Identifier) de 32 bits.

2. Diameter (RFC 6733) y SCTP (Stream Control Transmission Protocol - Puerto 3868):
   - Protocolo de transporte confiable orientado a mensajes (no a flujos de bytes como TCP).
   - Utilizado en senalizacion 4G LTE y Roaming Internacional sobre la red IPX.

3. Comandos de Inspeccion y Captura de Paquetes Celulares en Servidores Linux:
   # Capturar trafico GTP-U y ver el trafico IP interno que transporta el tunel:
   sudo tshark -i eth1 -f "udp port 2152" -d udp.port==2152,gtp -Y "gtp.message_type == 255"

   # Verificar asociaciones SCTP activas de senalizacion (MME / AMF):

`cisco
cat /proc/net/sctp/assocs
`
