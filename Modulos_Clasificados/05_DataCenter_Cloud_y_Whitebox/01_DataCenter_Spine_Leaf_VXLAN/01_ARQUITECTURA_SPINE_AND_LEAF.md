# 01. ARQUITECTURA SPINE-AND-LEAF (TOPOLOGIA CLOS Y ECMP)

> **REDES DE CENTROS DE DATOS (DATA CENTER & CLOUD NETWORKING)**


---



## 1. ORIGEN Y FUNDAMENTOS DE LA RED CLOS

En 1953, Charles Clos (investigador de Bell Labs) diseno un modelo matematico para
conmutacion telefonica libre de bloqueos multi-etapa. Con la explosion del trafico
horizontal Este-Oeste en centros de datos modernos (clusters de microservicios,
Bases de Datos distribuidas, Hadoop/Spark, VMware vMotion y entrenamiento de Modelos
de Inteligencia Artificial), la arquitectura tradicional colapso.

La red Clos de dos etapas aplicada a centros de datos se denomina "Spine-and-Leaf"
(Columna y Hoja) o IP Fabric.

```text
              +-------------------+       +-------------------+
              |      SPINE 1      |       |      SPINE 2      |  ... (SPINE N)
              |  (Conmutador L3)  |       |  (Conmutador L3)  |
              +---------+---------+       +---------+---------+
                       / \                         / \
                      /   \                       /   \
                     /     \                     /     \
                    /       \                   /       \
         +---------+         +---------+       /         \
         |                   |          +-----+           +-----+
         |                   |          |                       |
   +-----+-----+       +-----+-----+  +-+---------+       +-----+-----+
   |  LEAF 1   |       |  LEAF 2   |  |  LEAF 3   |  ...  |  LEAF N   |
   | (ToR L2/L3)|      | (ToR L2/L3)|  | (ToR L2/L3)|      | (ToR L2/L3)|
   +-----+-----+       +-----+-----+  +-----+-----+       +-----+-----+
         |                   |              |                   |
    [Servidores]        [Servidores]   [Servidores]        [Servidores]
```


## 2. LAS REGLAS DE ORO DE LA ARQUITECTURA SPINE-AND-LEAF

REGLA 1: Cada Leaf DEBE conectarse a TODOS los Spines.
REGLA 2: Los Spines NUNCA se conectan entre si (no hay enlaces Spine-to-Spine).
REGLA 3: Los Leaves NUNCA se conectan directamente entre si a nivel de Fabric
         (en fabrics L3 puros, todo pasa por los Spines. En arquitecturas L2 con
         MLAG/vPC, puede existir un peer-link local entre pares de hojas para redundancia).
REGLA 4: Los servidores, cabinas de almacenamiento y firewalls NUNCA se conectan
         a los Spines; se conectan EXCLUSIVAMENTE a los Leaves.



## 3. VENTAJAS DETERMINISTAS FRENTE AL DISENO CLASICO DE 3 CAPAS


### a) Latencia Ultra-Baja y Determinista (1 Solo Salto de Fabric):

   Cualquier servidor conectado al Leaf 1 se encuentra exactamente a 2 saltos
   de red de cualquier servidor en el Leaf N:
   Trayectoria: [Servidor A] -> Leaf 1 -> [Cualquier Spine] -> Leaf N -> [Servidor B].
   La latencia es constante, predecible y uniforme en todo el centro de datos.


### b) Muerte Total de Spanning Tree Protocol (STP):

   Todos los enlaces entre Leaf y Spine son puertos ENRUTADOS (Layer 3).
   Al ser Capa 3, STP no tiene razon de existir en la matriz de interconexion.
   No hay enlaces bloqueados: el 100% del ancho de banda instalado esta activo
   y reenviando paquetes concurrentemente.


### c) Escalabilidad Horizontal Simple:

   - ¿Se necesita mas ancho de banda entre racks? -> Se anade un nuevo Spine.
   - ¿Se necesitan mas servidores y racks? -> Se anade un nuevo par de Leaves.



## 4. ECMP (EQUAL-COST MULTI-PATH): REENVIO MASIVO EN PARALELO

En una topologia Spine-and-Leaf con 4 Spines, un Leaf dispone de 4 rutas de igual
costo para alcanzar la red del Leaf destino.

¿Como reparte el hardware los flujos sin provocar desorden de paquetes?
- Los switches utilizan un algoritmo de Hash por Hardware (5-Tuple Hashing):
  Campos evaluados:
  1. IP Origen (Source IP)
  2. IP Destino (Destination IP)
  3. Protocolo IP (TCP / UDP / ICMP)
  4. Puerto Origen L4 (Source Port)
  5. Puerto Destino L4 (Destination Port)

Resultado:
- Todos los paquetes de un mismo flujo (sesion TCP) obtienen el mismo valor Hash
  y viajan estrictamente por el MISMO Spine. Esto garantiza que NUNCA ocurra
  reordenamiento de paquetes (Out-of-Order Packets), el cual destruiria el
  rendimiento de la ventana TCP.
- Miles de flujos concurrentes se distribuyen uniformemente a traves de los 4, 8,
  16 o 32 Spines disponibles mediante ECMP de 32 a 64 vias.



## 5. RATIO DE SOBRESUSCRIPCION (OVERSUBSCRIPTION RATIO)

El calculo de sobresuscripcion determina el cuello de botella potencial entre los
puertos de acceso (hacia servidores) y los puertos de subida (Uplinks hacia Spines).

Formula:
  Ratio = Capacidad Total Puertos de Servidores : Capacidad Total Puertos Uplinks

Ejemplo Practico en un Leaf Switch:
- 48 puertos de 10 Gbps hacia servidores = 480 Gbps hacia abajo (Downlink).
- 4 puertos de 100 Gbps hacia Spines = 400 Gbps hacia arriba (Uplink).
- Ratio de Sobresuscripcion: 480 / 400 = 1.2 : 1 (Casi No-Bloqueante / Ultra Rendimiento).

Estandares de la Industria:
- Centros de Datos para IA / Computacion Cuantica / SAN: 1:1 (Non-blocking puro).
- Centros de Datos Empresariales de Alta Densidad: 2:1 a 3:1 (Aceptable y economico).



## 6. PROTOCOLOS DE ENRUTAMIENTO DEL UNDERLAY (LA BASE L3)

La red fisica que conecta Spines y Leaves se denomina "Underlay Network".
Su unico objetivo es ofrecer conectividad IP confiable y ultra-rapida para las
direcciones Loopback de los switches.

Alternativas de Underlay:
1. eBGP (External BGP - Recomendado por IETF RFC 7938 / Meta / Google):
   - Cada Leaf Switch tiene su propio Numero de Sistema Autonomo (ASN Privado 65001, 65002...).
   - Todos los Spine Switches comparten un mismo ASN comun (ej. ASN 65000).
   - Ventaja: Aislamiento total de rutas, control granular de politicas con BGP Communities,
     soporte nativo de BGP Unnumbered (utilizando direcciones IPv6 Link-Local para formar
     vecindades BGP sin necesidad de configurar una IP /30 o /31 en cada puerto).

2. OSPF / IS-IS Point-to-Point:
   - Todo el Fabric en una sola Area Backbone (Area 0 de OSPF o Nivel 2 de IS-IS).
   - Enlaces configurados como `network point-to-point`.
   - Ventaja: Convergencia ultrarrapida con BFD (Bidirectional Forwarding Detection)

en menos de 50 milisegundos ante caidas de fibra.
