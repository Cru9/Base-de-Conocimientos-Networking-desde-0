# 02. CAPA 2: CAPA DE ENLACE DE DATOS (DATA LINK LAYER) - TRAMAS Y CONMUTACION

> **MODELO OSI (OPEN SYSTEMS INTERCONNECTION) - GUIA MAESTRA PARA CERTIFICACIONES**  
> *Guía de referencia técnica y preparación para certificaciones Cisco CCNA 200-301, CompTIA Network+ y Huawei HCIA.*

---


## 1. FUNCION Y PROPOSITO DE LA CAPA DE ENLACE DE DATOS

La Capa 2 es responsable de la transferencia confiable de informacion a traves
de un enlace fisico directo entre dos nodos adyacentes (comunicacion nodo a nodo).

Su PDU (Unidad de Datos de Protocolo) es la TRAMA (Frame).

Principales responsabilidades:
- Entramado (Framing): Empaquetar los paquetes recibidos de la Capa 3 (IP) dentro
  de una estructura con encabezado y pie de pagina (Header y Trailer).
- Direccionamiento Fisico (Direcciones MAC): Identificar de forma unica al emisor
  y receptor dentro del mismo segmento de red local (LAN).
- Control de Acceso al Medio (MAC): Arbitrar quien tiene derecho a transmitir
  cuando varios dispositivos comparten el mismo canal.
- Deteccion de Errores: Validar mediante algoritmos matematicos (CRC32) que ningun
  bit se haya corrompido durante el trayecto fisico.


## 2. LAS DOS SUBCAPAS IEEE 802 (CONCEPTO CLAVE DE CERTIFICACION)

El comite IEEE dividio la Capa 2 del modelo OSI en dos subcapas complementarias:

```text
+-----------------------------------------------------------------------+
|  Capa 3 de Red (IPv4 / IPv6 / ARP / ICMP)                             |
+-----------------------------------------------------------------------+
```

|  Capa 2: Subcapa LLC (Logical Link Control - Estandar IEEE 802.2)    |
```text
+-----------------------------------------------------------------------+
|  Capa 2: Subcapa MAC (Media Access Control - IEEE 802.3 / 802.11)     |
+-----------------------------------------------------------------------+
```

|  Capa 1: Fisica (Cobre / Fibra / Aire)                                |
```text
+-----------------------------------------------------------------------+

a) Subcapa LLC (Logical Link Control - 802.2):
   - Es una interfaz de software independiente del hardware.
   - Se comunica hacia arriba con la Capa 3 y multiplexa multiples protocolos
     de red (IPv4, IPv6) sobre la misma interfaz fisica utilizando campos SAP/SNAP.
   - Maneja el control de flujo basico y la confirmacion de recepcion.

b) Subcapa MAC (Media Access Control - 802.3 Ethernet / 802.11 Wi-Fi):
   - Es una interfaz ligada directamente al hardware (tarjeta de red / NIC).
   - Maneja las direcciones MAC fisicas de 48 bits.
   - Aplica los mecanismos de acceso al medio (CSMA/CD para cable, CSMA/CA para Wi-Fi).
   - Ensambla y valida el pie de trama (FCS - Frame Check Sequence).


3. ESTRUCTURA COMPLETA DE LA TRAMA ETHERNET II
-------------------------------------------------------------------------------
Campo              Tamano      Descripcion
-------------------------------------------------------------------------------
Preambulo          7 Bytes     Secuencia alternada de 10101010 para sincronizar relojes.
SFD                1 Byte      Delimitador de inicio de trama (10101011).
MAC Destino        6 Bytes     Direccion fisica de la tarjeta de red del receptor.
MAC Origen         6 Bytes     Direccion fisica de la tarjeta de red del emisor.
Type (EtherType)   2 Bytes     Protocolo de Capa 3 encapsulado dentro del payload:
                               0x0800 = IPv4
                               0x86DD = IPv6
                               0x0806 = ARP
                               0x8100 = Trama etiquetada 802.1Q (VLAN)
Payload (Datos)    46 a 1500 B Paquete de Capa 3 (MTU maximo = 1500 bytes).
FCS (Checksum)     4 Bytes     Secuencia de Verificacion de Trama (Algoritmo CRC-32).

Tamanos Criticos de Trama en Examenes:
- Tamano Minimo de Trama: 64 Bytes (cualquier trama menor se considera una "Runt"
  provocada por una colision y se descarta).
- Tamano Maximo Estandar: 1518 Bytes (1522 Bytes si incluye etiqueta VLAN 802.1Q).
  Cualquier trama mayor a 1518 sin etiqueta se considera un "Giant".
- Jumbo Frames: Tramas extendidas de hasta 9000 bytes usadas en redes de almacenamiento (SAN/iSCSI).


4. DIRECCIONAMIENTO MAC (MEDIA ACCESS CONTROL)
-------------------------------------------------------------------------------
Una direccion MAC es un identificador de 48 bits (6 bytes) expresado en formato
hexadecimal (ejemplo: `00:1A:2B:3C:4D:5E` o en Cisco: `001a.2b3c.4d5e`).

Estructura de la direccion MAC:
[ 24 bits: OUI (Fabricante) ] [ 24 bits: Asignados por el fabricante a la tarjeta ]

- OUI (Organizationally Unique Identifier): Los primeros 3 bytes son asignados por
  el IEEE a empresas fabricantes (Cisco, Intel, Apple, HP, Huawei).
- Bits Especiales en el Primer Octeto:
  * Bit I/G (Individual/Group): Si el bit 0 es 0 = Unicast; si es 1 = Multicast.
  * Bit U/L (Universal/Local): Si el bit 1 es 0 = Universal (de fabrica); 1 = Administrada localmente.

Tipos de Direcciones MAC:
1. Unicast: Dirigida a un unico host especifico.
2. Broadcast (Difusion): Enviada a todos los hosts de la red local:
   `FF:FF:FF:FF:FF:FF` (los 48 bits estan en '1').
3. Multicast: Enviada a un grupo suscrito de dispositivos.
   Ejemplo en IPv4: Inicia con `01:00:5E:xx:xx:xx`.
   Ejemplo en IPv6: Inicia con `33:33:xx:xx:xx:xx`.


5. DOMINIOS DE COLISION vs DOMINIOS DE DIFUSION (BROADCAST)
-------------------------------------------------------------------------------
Concepto de examen fundamental:

a) Dominio de Colision (Collision Domain):
   - Area de la red donde si dos equipos transmiten al mismo tiempo ocurre una colision.
   - Un Hub tiene 1 solo dominio de colision para todos sus puertos (Half-Duplex).
   - Un Switch divide dominios de colision: CADA PUERTO DE UN SWITCH ES UN DOMINIO
     DE COLISION INDEPENDIENTE (opera en Full-Duplex libre de colisiones).

b) Dominio de Difusion (Broadcast Domain):
   - Area de la red hasta donde llega una trama de broadcast (`FF:FF:FF:FF:FF:FF`).
   - Un Switch propaga los broadcasts por todos sus puertos (1 switch = 1 dominio de difusion).
   - Las VLANs dividen dominios de difusion dentro del switch (cada VLAN es 1 dominio de broadcast).
   - Los Enrutadores (Routers / Capa 3) BLOQUEAN los broadcasts y dividen dominios de difusion.


6. COMO FUNCIONA UN CONMUTADOR (SWITCH) Y LA TABLA CAM
-------------------------------------------------------------------------------
Un switch conmuta tramas basandose en su Tabla de Direcciones MAC (Tabla CAM):
El proceso sigue 3 pasos estrictos:

1. Aprender (Learning): El switch inspecciona la direccion MAC ORIGEN de la trama
   entrante y anota en su tabla CAM: `[MAC Origen -> Puerto Fisico -> VLAN -> Temporizador (300 s)]`.
2. Reenviar o Filtrar (Forwarding / Filtering): El switch inspecciona la MAC DESTINO:
   - Si la MAC destino YA esta registrada en la tabla CAM, la envia UNICAMENTE
     por el puerto fisico asociado (reenvio unicast).
   - Si la MAC destino pertenece al mismo puerto por donde entro, la filtra (descarta).
3. Inundar (Unknown Unicast Flooding): Si la MAC destino NO esta en la tabla CAM,
   el switch retransmite la trama por TODOS los demas puertos de esa misma VLAN
   (excepto por el puerto donde ingreso), esperando que el host destino responda.


7. PROTOCOLOS PRINCIPALES DE CAPA 2
-------------------------------------------------------------------------------
- Ethernet (IEEE 802.3): La tecnologia cableada dominante del mundo.
- Wi-Fi (IEEE 802.11): Capa de enlace inalambrica con gestion de tramas Beacon, Probe, Auth.
- IEEE 802.1Q: Etiquetado de VLANs (agrega 4 bytes con el VLAN ID de 12 bits: 1 a 4094).
- Spanning Tree Protocol (STP 802.1D / RSTP 802.1w): Previene bucles bloqueando puertos redundantes.
- LACP (IEEE 802.3ad / 802.1AX): Agregacion de enlaces fisicos en un enlace logico.
- ARP (Address Resolution Protocol): Vincula una IP de Capa 3 con una MAC de Capa 2.
- Protocolos WAN de Capa 2: HDLC, PPP (Point-to-Point Protocol), Frame Relay.


8. PREGUNTAS CLAVE DE EXAMEN (TIPO CCNA / HCIA)
-------------------------------------------------------------------------------
Pregunta 1: Un switch de 24 puertos tiene 3 VLANs configuradas (VLAN 10, 20 y 30).
¿Cuantos dominios de colision y cuantos dominios de difusion tiene el switch?
Respuesta:
- Dominios de Colision: 24 (cada puerto del switch es un dominio de colision independiente).
- Dominios de Difusion: 3 (cada VLAN representa un dominio de difusion independiente).

Pregunta 2: ¿Que campo de la trama Ethernet permite detectar si los datos llegaron corruptos?
Respuesta: El campo FCS (Frame Check Sequence), que utiliza el algoritmo CRC-32 (Cyclic Redundancy Check).
===============================================================================
