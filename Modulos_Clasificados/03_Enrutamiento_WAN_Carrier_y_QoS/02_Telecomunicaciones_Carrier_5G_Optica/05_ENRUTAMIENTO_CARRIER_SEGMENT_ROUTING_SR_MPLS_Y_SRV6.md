# 05. ENRUTAMIENTO CARRIER: SEGMENT ROUTING (SR-MPLS Y SRV6) Y TI-LFA

> **TELECOMUNICACIONES AVANZADAS, REDES DE CARRIER E INFRAESTRUCTURA GLOBAL**


---



## 1. LA REVOLUCION DE SEGMENT ROUTING (RFC 8402)

Durante mas de 20 anos, las redes troncales de telecomunicaciones (Carriers e ISPs)
dependieron de dos protocolos MPLS para el transporte de trafico:
1. LDP (Label Distribution Protocol): Distribuye etiquetas a ciegas siguiendo la ruta
   de menor costo del IGP, pero carece de ingenieria de trafico (no puede desviar
   flujos hacia rutas con menor latencia).
2. RSVP-TE (Resource Reservation Protocol - Traffic Engineering): Permite ingenieria
   de trafico mediante reserva de ancho de banda, pero crea un "estado de flujo"
   (Soft State) en cada router de transito. En redes con 10,000 nodos y millones
   de tuneles, el consumo de memoria y CPU provocaba caidas masivas del Core ante fallas.

FILOSOFIA DE SEGMENT ROUTING: "SOURCE ROUTING" SIN ESTADO EN EL NUCLEO:
- Toda la inteligencia reside en el router de entrada (Ingress PE / Headend).
- El router de entrada codifica la ruta completa como una lista ordenada de instrucciones
  (Segments) incrustada en la cabecera del paquete.
- Los routers intermedios (P routers) NO mantienen ningun estado de sesion ni tunel en memoria;
  unicamente leen la instruccion activa en la cabecera, reenvian y desapilan.



## 2. TIPOS DE SEGMENTOS E IDENTIFICADORES (SIDs)

Un segmento representa una instruccion topologica o de servicio:

1. Prefix-SID / Node-SID (Segmento de Prefijo o Nodo):
   - Identifica globalmente a un router dentro del dominio de red.
   - El paquete se enruta siguiendo el camino de menor metrica IGP (ECMP soportado).
   - Ejemplo: El Router Core 1 tiene asignado el Node-SID 16001; el Router Core 5 tiene el 16005.

2. Adjacency-SID (Adj-SID - Segmento de Adyacencia):
   - Identifica un enlace fisico o interfaz especifica hacia un router vecino.
   - Es localmente significativo para el router que lo anuncia.
   - Fuerza al paquete a cruzar ese cable especifico, permitiendo construir rutas
     estrictas ignorando por completo la metrica del protocolo IGP.

3. Anycast-SID:
   - Asigna un mismo SID a un conjunto redundante de routers (ej. servidores DNS o pasarelas de salida).

4. Binding-SID (BSID):
   - Vincula un unico SID a una politica compleja de ingenieria de trafico (SR-TE).
   - Permite componer rutas jerarquicas entre diferentes paises o sistemas autonomos
     ocultando la topologia interna.



## 3. PLANOS DE DATOS: SR-MPLS VS SRV6

Segment Routing puede ejecutarse sobre dos planos de reenvio de hardware:

A. SR-MPLS (Segment Routing sobre MPLS):
   - Reutiliza el hardware y chips ASIC existentes compatibles con conmutacion de etiquetas MPLS.
   - Los SIDs se representan como etiquetas MPLS estandar de 20 bits.
   - SRGB (Segment Routing Global Block): Rango de etiquetas reservado para Prefix-SIDs
     (el estandar de la industria es 16000 a 23999).
   - Los SIDs se distribuyen directamente dentro de las extensiones de OSPFv2 (Opaque LSAs Type 10)
     o IS-IS (TLV 242 y TLV 135/235), eliminando la necesidad de correr el protocolo LDP.

B. SRv6 (Segment Routing sobre IPv6 Nativo - RFC 8754):
   - LA CUSPIDE DEL ENRUTAMIENTO MODERNO. Elimina las etiquetas MPLS por completo.
   - Todo el paquete viaja bajo formato IPv6 puro utilizando la cabecera de extension
     Segment Routing Header (SRH).
   - Un SID en SRv6 es una direccion IPv6 completa de 128 bits estructurada en tres campos:
     Locator : Function : Arguments (ejemplo: 2001:db8:1:f100::)
     * Locator: Prefijo IPv6 que enruta el paquete hacia el nodo correcto.
     * Function: Accion programable que debe ejecutar el router al recibir el paquete:
       - End: Avanza al siguiente SID de la lista.
       - End.X: Reenvia por un enlace de adyacencia fisico especifico.
       - End.DT4 / End.DT6: Desencapsula el paquete IPv4/IPv6 y lo inyecta en la tabla VRF (L3VPN).
   - Micro-SIDs (uSID): Agrupa varios SIDs comprimidos en una sola cabecera IPv6 para
     reducir el impacto de bytes en el paquete (Overhead).



## 4. RESILIENCIA ABSOLUTA: TI-LFA (TOPOLOGY-INDEPENDENT LFA)

En las redes tradicionales de telecomunicaciones, cuando un enlace de fibra se corta,
el protocolo de enrutamiento puede tardar de 500 ms a 3 segundos en converger,
provocando la caida de millones de llamadas telefonicas y transacciones bancarias.

TI-LFA GARANTIZA RECUPERACION ANTE FALLAS EN MENOS DE 50 MILISEGUNDOS:
- Proteccion al 100% de la red: A diferencia de las tecnicas antiguas de LFA clasico
  (que dejaban desprotegidas hasta el 40% de las topologías complejas), TI-LFA
  ofrece una ruta de respaldo precalculada en hardware para el 100% de los enlaces y nodos.
- Calculo del Espacio P y Espacio Q:
  * Espacio P: Conjunto de routers que el origen puede alcanzar sin cruzar el enlace fallido.
  * Espacio Q: Conjunto de routers que pueden alcanzar el destino sin cruzar el enlace fallido.
  * Nodo PQ: Interseccion donde el router de origen pre-programa una etiqueta Segment Routing
    hacia el nodo PQ. En el microsegundo en que el hardware detecta perdida de luz optica,
    el chip ASIC conmuta instantaneamente el trafico hacia la ruta alterna sin bucles.



## 5. INGENIERIA DE TRAFICO MODERNA: SR-TE (TRAFFIC ENGINEERING)

Con Segment Routing, la ingenieria de trafico ya no requiere mantener tuneles abiertos.
Se definen Politicas de Enrutamiento (SR Policies) basadas en SLA:

Politica 1: Trafico Critico de Voz y Gaming (Minima Latencia):
- El Ingress PE consulta las metricas de retardo medidas activamente con sondas
  TWAMP o BFD y apila los SIDs para forzar al paquete a viajar por la ruta geografica
  con menor latencia en microsegundos, ignorando el ancho de banda.

Politica 2: Trafico Masivo de Descarga (Maximo Ancho de Banda):
- El Ingress PE enruta el trafico a traves de caminos secundarios desocupados
  para evitar congestionar las troncales principales.



## 6. CONFIGURACION PRACTICA EN CISCO IOS-XR (ROUTERS CARRIER ASR 9000 / NCS 5500)

! 1. Habilitar Segment Routing globalmente con bloque SRGB
segment-routing
 global-block 16000 23999
!

! 2. Configurar IS-IS con soporte de Segment Routing y TI-LFA
router isis BACKBONE-CORE
 is-type level-2-only
 net 49.0001.0000.0000.0001.00
 !
 address-family ipv4 unicast
  metric-style wide
  segment-routing mpls
 !
 interface Loopback0
  passive
  address-family ipv4 unicast
   prefix-sid index 1          ! Node-SID 16001 para el Router Core 1
  !
 !
 interface TenGigE0/0/0/1
  description ENLACE_CORE_A_ROUTER_2
  point-to-point
  address-family ipv4 unicast
   fast-reroute per-prefix ti-lfa   ! Habilitar conmutacion TI-LFA < 50 ms
  !
 !
commit



## 7. VERIFICACION Y COMANDOS DE DIAGNOSTICO EN CARRIER CORE

1. Verificar la tabla de reenvio de etiquetas de Segment Routing (MPLS FIB):
```text
   show mpls forwarding
   ! Debe mostrar el rango 16000-23999 con accion 'Pop' o 'Swap' hacia el siguiente salto.

2. Verificar que TI-LFA tenga una ruta de respaldo precalculada en hardware:
   show isis fast-reroute 10.255.0.5/32 detail
   ! Muestra: "LFA: Protected by TI-LFA, Backup Path via TenGigE0/0/0/2, Repair List: [16003]"

3. Trazar la ruta de etiquetas de un paquete con Segment Routing:
```


`cisco
traceroute sr-mpls 10.255.0.5/32
`
