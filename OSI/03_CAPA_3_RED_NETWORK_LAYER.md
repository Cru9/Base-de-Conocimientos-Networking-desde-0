# 03. CAPA 3: CAPA DE RED (NETWORK LAYER) - ENRUTAMIENTO, IPv4, IPv6 Y SUBNETTING

> **MODELO OSI (OPEN SYSTEMS INTERCONNECTION) - GUIA MAESTRA PARA CERTIFICACIONES**  
> *Guía de referencia técnica y preparación para certificaciones Cisco CCNA 200-301, CompTIA Network+ y Huawei HCIA.*

---


## 1. FUNCION Y PROPOSITO DE LA CAPA DE RED

La Capa de Red es el corazon del enrutamiento en Internet. Su responsabilidad
fundamental es el transporte de datos de extremo a extremo (End-to-End) a traves
de multiples redes intermedias interconectadas.

A diferencia de la Capa 2 (que solo entrega tramas dentro de la misma LAN local),
la Capa 3 sabe como guiar los paquetes a traves de continentes y proveedores de
servicios (ISPs) diferentes.

Su PDU (Unidad de Datos de Protocolo) es el PAQUETE (Packet).

Funciones principales:
- Direccionamiento Logico: Asignar direcciones IP unicas y jerarquicas.
- Determinacion de la Mejor Ruta (Routing): Seleccionar el camino optimo mediante
  tablas de enrutamiento y protocolos dinamicos (OSPF, BGP, EIGRP).
- Conmutacion de Paquetes (Packet Forwarding): Mover paquetes desde la interfaz
  de entrada hacia la interfaz de salida correspondiente.
- Fragmentacion y Reensamblaje: Dividir paquetes grandes cuando el MTU de la
  red siguiente es menor (ej. MTU Ethernet 1500 bytes vs WAN 1492 bytes).


## 2. ESTRUCTURA COMPLETA DEL ENCABEZADO IPv4 (20 A 60 BYTES)

| Campo | Bits | Descripcion |
| :--- | :--- | :--- |
| Version | 4 bits | Version del protocolo IP (0100 = IPv4). |
| IHL | 4 bits | Internet Header Length (Longitud del encabezado; min 5 = 20 B). |
| Type of Service/DSCP 8 bits | Calidad de Servicio (QoS): Clasifica prioridad de trafico y ECN. |  |
| Total Length | 16 bits | Tamano total del paquete (Encabezado + Datos; max 65,535 B). |
| Identification | 16 bits | Numero unico para identificar fragmentos del mismo paquete. |
| Flags | 3 bits | Control de fragmentacion: Bit 0 (Reservado), Bit 1 (DF - Don't |
| Fragment: no dividir), Bit 2 (MF - More Fragments: vienen mas). |  |  |
| Fragment Offset | 13 bits | Posicion del fragmento dentro del paquete original (en bloques de 8B). |
| TTL (Time to Live) | 8 bits | Tiempo de Vida (0-255). Se decrementa en 1 en cada salto de router. |
| Si llega a 0, el paquete se DESCARTA y se envia un ICMP Time |  |  |
| Exceeded. ¡PREVIENE BUCLES INFINITOS DE ENRUTAMIENTO! |  |  |
| Protocol | 8 bits | Protocolo de Capa 4 transportado: |
| 1 = ICMP, 6 = TCP, 17 = UDP, 89 = OSPF. |  |  |
| Header Checksum | 16 bits | Suma de verificacion matematica exclusiva del encabezado IP. |
| Source IP Address | 32 bits | Direccion IP de origen (Emisor original). |
| Destination IP | 32 bits | Direccion IP de destino (Receptor final). |
| Options / Padding | Variable Opciones opcionales de seguridad y relleno. |  |



## 3. DIRECCIONAMIENTO IPv4 Y CLASES HISTORICAS

Una direccion IPv4 consta de 32 bits divididos en 4 octetos en formato decimal:
`192.168.1.1` = `11000000.10101000.00000001.00000001`

Clases de Redes Historicas:
| Clase | Rango de Primer Octeto | Mascara por Defecto | Proposito Original |
| :--- | :--- | :--- | :--- |
| A | 1.0.0.0 a 126.255.255.255 | /8 (255.0.0.0) | Redes gigantescas (16M hosts) |
| (127.0.0.0 reservado para Loopback de prueba local: 127.0.0.1) |  |  |  |
| B | 128.0.0.0 a 191.255.255.255 | /16 (255.255.0.0) | Redes medianas (65,534 hosts) |
| C | 192.0.0.0 a 223.255.255.255 | /24 (255.255.255.0) | Redes pequeñas (254 hosts) |
| D | 224.0.0.0 a 239.255.255.255 | Sin mascara | Trafico Multicast |
| E | 240.0.0.0 a 255.255.255.255 | Sin mascara | Investigacion / Experimental |


Rangos Privados (RFC 1918) - No enrutables en Internet publico:
- Clase A: `10.0.0.0` a `10.255.255.255` (Prefijo /8)
- Clase B: `172.16.0.0` a `172.31.255.255` (Prefijo /12)
- Clase C: `192.168.0.0` a `192.168.255.255` (Prefijo /16)

Direcciones Especiales en Examenes:
- `169.254.0.0/16`: APIPA (Automatic Private IP Addressing) - asignada por Windows
  cuando el cliente NO encuentra ningun servidor DHCP en la red.
- `255.255.255.255`: Broadcast limitado a la red local.
- `0.0.0.0/0`: Ruta por defecto (Gateway of Last Resort).


## 4. MATEMATICAS DE SUBNETTING Y FORMULAS PARA CERTIFICACION

El Subnetting divide una red grande en subredes mas pequenas para optimizar
el espacio de direcciones y la seguridad.

Formulas Obligatorias:
- Cantidad de Subredes creadas = 2^N  (donde N = bits robados a la porcion de host).
- Cantidad de Hosts Utiles por subred = (2^H) - 2  (donde H = bits restantes de host).
  *Se restan 2 direcciones: la Direccion de Red (ID) y la Direccion de Broadcast.

Tabla Rapida de Prefijos CIDR (/24 a /30):
| Prefijo | Mascara Decimal | Bits Host | Hosts Totales | Hosts Utiles | Salto de Red |
| :--- | :--- | :--- | :--- | :--- | :--- |
| /24 | 255.255.255.0 | 8 bits | 256 | 254 | 1 |
| /25 | 255.255.255.128 | 7 bits | 128 | 126 | 128 |
| /26 | 255.255.255.192 | 6 bits | 64 | 62 | 64 |
| /27 | 255.255.255.224 | 5 bits | 32 | 30 | 32 |
| /28 | 255.255.255.240 | 4 bits | 16 | 14 | 16 |
| /29 | 255.255.255.248 | 3 bits | 8 | 6 | 8 |
| /30 | 255.255.255.252 | 2 bits | 4 | 2 (P2P WAN) | 4 |
| /31 | 255.255.255.254 | 1 bit | 2 | 2 (RFC 3021) | 2 |
| /32 | 255.255.255.255 | 0 bits | 1 | 1 (Host unico) 1 |  |



## 5. ARQUITECTURA IPv6 (EL ESTANDAR MODERNO)

IPv6 resuelve el agotamiento de IPv4 ofreciendo 128 bits (3.4 x 10^38 direcciones).
Se representa en 8 bloques hexadecimales (hextetos) de 16 bits cada uno:
`2001:0db8:85a3:0000:0000:8a2e:0370:7334`

Reglas de Compresion de Direcciones IPv6:
1. Omitir ceros a la izquierda: `0000` pasa a ser `0`; `0db8` pasa a ser `db8`.
2. Reemplazo de ceros consecutivos por doble dos puntos `::`:
   `2001:db8:85a3:0:0:8a2e:370:7334` ==> `2001:db8:85a3::8a2e:370:7334`
   *Regla de examen: `::` solo se puede usar UNA VEZ en toda la direccion.

Encabezado Fijo y Simplificado de IPv6 (40 Bytes):
- Version (4b), Traffic Class (8b), Flow Label (20b), Payload Length (16b),
  Next Header (8b - reemplaza al campo 'Protocol'), Hop Limit (8b - reemplaza al TTL),
  Source IPv6 (128b), Destination IPv6 (128b).
- ¡NO HAY CAMPO CHECKSUM EN EL ENCABEZADO IPv6! (Acelera el enrutamiento por hardware).

Tipos de Direcciones IPv6 en Examenes:
- Global Unicast (GUA): Inician con `2000::/3` (Direcciones publicas de Internet).
- Link-Local (LLA): Inician con `fe80::/10` (Obligatoria en toda interfaz; comunicacion local).
- Unique Local (ULA): Inician con `fc00::/7` (Equivalente a privadas RFC 1918).
- Multicast: Inician con `ff00::/8` (`ff02::1` = Todos los nodos; `ff02::2` = Todos los routers).
- Loopback: `::1`
- Generacion EUI-64: Convierte una MAC de 48 bits en un Interface ID de 64 bits
  insertando `FF:FE` en el medio e invirtiendo el septimo bit (bit U/L).


## 6. CONCEPTOS CLAVE DE ENRUTAMIENTO (ROUTING)

Distancia Administrativa (AD - Administrative Distance):
Representa la confiabilidad del origen de la ruta (menor numero = mayor prioridad):
| Origen de Ruta | Distancia Administrativa (AD) en Cisco |
| :--- | :--- |
| Directamente Conectada (C) | 0 |
| Ruta Estatica (S) | 1 |
| eBGP (BGP Externo) | 20 |
| EIGRP Interno | 90 |
| OSPF | 110 |
| IS-IS | 115 |
| RIP | 120 |
| iBGP (BGP Interno) | 200 |


Clasificacion de Protocolos de Enrutamiento Dinamico:
- Vector Distancia (Distance Vector): Algoritmo Bellman-Ford (RIP, EIGRP). Envian
  su tabla de rutas a los vecinos periodica o incrementalmente ("enrutamiento por rumor").
- Estado de Enlace (Link-State): Algoritmo Dijkstra / SPF (OSPF, IS-IS). Cada router
  conoce el mapa topologico completo de toda el area antes de calcular las mejores rutas.
- Vector Ruta (Path Vector): BGP (Border Gateway Protocol). Protocolo EGP que conecta
  sistemas autonomos en Internet basandose en politicas y lista de AS recorridos.


## 7. PREGUNTAS CLAVE DE EXAMEN (TIPO CCNA / HCIA)

### ❓ Pregunta 1
> **Un paquete IP tiene el campo TTL en valor 1. El router recibe el paquete**

y debe reenviarlo al siguiente salto. ¿Que accion tomara el router?
Respuesta: El router decrementa el TTL a 0, DESCARTA el paquete y envia un mensaje
ICMP Type 11 (Time-to-Live Exceeded) a la direccion IP de origen.

### ❓ Pregunta 2
> **¿Cual es la direccion de red y de broadcast de la IP 192.168.10.75/28?**

Respuesta:
- Prefijo /28 tiene mascara 255.255.255.240 -> Salto de red = 256 - 240 = 16.
- Subredes: 0, 16, 32, 48, 64, 80...
- El host 75 cae en la subred 64:
  * Direccion de Red: 192.168.10.64
  * Primer Host util: 192.168.10.65
  * Ultimo Host util: 192.168.10.78
## * Direccion de Broadcast: 192.168.10.79

