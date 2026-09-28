# 00. INDICE GENERAL, ARQUITECTURA WAN Y COMPARATIVA DE TECNOLOGIAS DE ACCESO

> **ENRUTAMIENTO AVANZADO Y TECNOLOGIAS WAN (ROUTING & WAN ARCHITECTURE)**


---



## 1. ¿QUE ES UNA RED DE AREA AMPLIA (WAN)?

Una red WAN (Wide Area Network) interconecta redes LAN dispersas geograficamente
(sucursales, corporativos, centros de datos, nubes publicas como AWS o Azure)
a traves de distancias que abarcan ciudades, paises o continentes.

A diferencia de una red LAN (donde la empresa es dueña de los cables y switches),
en una red WAN la infraestructura fisica de transporte pertenece a proveedores
de servicios de telecomunicaciones (Carriers / ISPs).

El desafio de la WAN:
Maximizar la disponibilidad y el ancho de banda minimizando los costos de telecomunicaciones,
garantizando la privacidad de los datos y manteniendo una latencia baja para
aplicaciones criticas (VoIP, bases de datos y ERPs).



## 2. TOPOLOGIAS WAN EMPRESARIALES


### a) Punto a Punto (Point-to-Point):

   - Enlace dedicado y directo entre dos sitios unicos.
   - Ventaja: Maxima seguridad y ancho de banda garantizado.
   - Desventaja: Muy costoso e inescalable para muchas sucursales.


### b) Estrella / Hub-and-Spoke:

   - Todas las sucursales remotas (Spokes) se conectan a un unico sitio central
     o Corporativo (Hub).
   - Ventaja: Gestion y politicas centralizadas; economico.
   - Desventaja: Si una sucursal quiere hablar con otra, el tráfico debe viajar al Hub
     y volver a salir (latencia "trombón"); el Hub es un punto unico de falla.


### c) Malla Completa (Full Mesh):

   - Cada sitio tiene un enlace directo hacia todos los demas sitios.
   - Ventaja: Minima latencia y maxima tolerancia a fallos.
   - Desventaja: Exponencialmente costoso de implementar: N*(N-1)/2 enlaces.


### d) Malla Parcial (Partial Mesh / Hibrida - Estandar Corporativo):

   - Los centros de datos y sitios principales estan en malla completa entre si,
     mientras que las sucursales pequenas se conectan mediante Hub-and-Spoke dual
     (Dual-Homed) a dos centros de datos diferentes para redundancia.



## 3. EVOLUCION CRONOLOGICA DE LAS TECNOLOGIAS WAN


| Tecnologia | Velocidad Tipica | Ventajas | Desventajas |
| :--- | :--- | :--- | :--- |
| Lineas Dedicadas | 64 Kbps a 2 Mbps | Ancho de banda garantizado, Costo altisimo, |  |
| (T1 / E1 / T3) | (TDM / Serial) | baja latencia fija. | cero flexibilidad. |


Frame Relay / ATM     56 Kbps a 45 Mbps   Circuitos virtuales (PVC),  Tecnologia obsoleta,
                                          comparticion de ancho banda.complejidad de celdas.

MPLS (Multi-Protocol  10 Mbps a 10 Gbps   Garantia estricta de SLA,  Costo elevado por Mbps,
Label Switching)                          QoS nativo, privado.       despliegue lento (meses).

MetroEthernet / VPLS  100 Mbps a 100 Gbps Conexion Ethernet nativa   Disponible solo en
                                          Capa 2 entre edificios.    zonas metropolitanas.

Internet de Banda     100 Mbps a 1 Gbps   Bajo costo, facil de       Sin garantias de SLA,
Ancha (Fibra / Coax)                      contratar, alta velocidad.  latencia impredecible.

SD-WAN (Software-     Multi-Gigabit       Usa multiples transportes, Requiere appliances
Defined WAN)          (Agregado)          cifrado IPsec automatico, inteligentes y licencias.
                                          enrutamiento por app.



## 4. INDICE DE ARCHIVOS DE LA CARPETA ROUTING_Y_WAN

[00_INDICE_Y_ARQUITECTURA_WAN.md](./00_INDICE_Y_ARQUITECTURA_WAN.md)
    - Fundamentos de redes WAN, topologias empresariales y comparativa de medios.

[01_OSPF_MULTI_AREA_AVANZADO.md](./01_OSPF_MULTI_AREA_AVANZADO.md)
    - OSPF en entornos corporativos complejos: Jerarquia de areas, tipos de routers
      (ABR, ASBR), tipos de LSAs (1 al 7), areas Stub/NSSA, Virtual Links y afinamiento BFD.

[02_BGP_BORDER_GATEWAY_PROTOCOL.md](./02_BGP_BORDER_GATEWAY_PROTOCOL.md)
    - BGPv4 a fondo: Sistemas Autonomos (ASN), sesiones eBGP vs iBGP, Route Reflectors,
      algoritmo de seleccion de mejor ruta (Best Path Selection) y atributos (Weight,
      Local-Pref, AS-Path, MED).

[03_MPLS_Y_L3VPN_FUNDAMENTOS.md](./03_MPLS_Y_L3VPN_FUNDAMENTOS.md)
    - Conmutacion por etiquetas (Label Switching): Arquitectura LSR/LER, encabezado Shim,
      protocolo LDP, Penultimate Hop Popping (PHP) y funcionamiento de MPLS L3VPNs (VRF, RD, RT).

[04_SD_WAN_ARQUITECTURAS_Y_EVOLUCION.md](./04_SD_WAN_ARQUITECTURAS_Y_EVOLUCION.md)
    - El salto tecnologico hacia SD-WAN: Desacoplamiento de planos (Control, Datos, Gestion),
      Underlay vs Overlay, enrutamiento dinamico basado en SLAs de aplicacion (Jitter, Packet Loss).

[05_CONFIGURACIONES_AVANZADAS_POR_MARCA.md](./05_CONFIGURACIONES_AVANZADAS_POR_MARCA.md)
    - Laboratorio practico con sintaxis real para Cisco IOS-XE, Huawei VRP y ArubaOS-CX.

[06_FUNDAMENTOS_DE_RUTEO_Y_RUTAS_ESTATICAS.md](./06_FUNDAMENTOS_DE_RUTEO_Y_RUTAS_ESTATICAS.md)
    - Manual de Fundamentos: Planos de Control/Datos (RIB, FIB, CEF), Longest Prefix Match,
      Distancia Administrativa vs Metrica, tipos de rutas estaticas y laboratorio con IP SLA Failover.

[07_MANUAL_RIP_V1_V2_RIPNG_CON_EJERCICIOS.md](./07_MANUAL_RIP_V1_V2_RIPNG_CON_EJERCICIOS.md)
    - Manual de RIP (v1, v2 y RIPng): Algoritmo Bellman-Ford, conteo al infinito, prevencion
      de bucles (Split Horizon, Poison Reverse, Timers) y laboratorio de distribucion con MD5.

[08_MANUAL_IGRP_Y_EIGRP_CON_EJERCICIOS.md](./08_MANUAL_IGRP_Y_EIGRP_CON_EJERCICIOS.md)
    - Manual de IGRP y EIGRP: Historia de IGRP y por que fue retirado, Algoritmo DUAL, Sucesor
      y Sucesor Factible, formulas metricas K1-K5, variance y ejercicio en campus bancario.

[09_MANUAL_OSPF_TEORIA_Y_EJERCICIOS_PRACTICOS.md](./09_MANUAL_OSPF_TEORIA_Y_EJERCICIOS_PRACTICOS.md)
    - Manual integral de OSPF: Algoritmo Dijkstra, 5 tipos de paquetes, 7 estados de vecindad,
      eleccion DR/BDR, formula moderna de costo y ejercicio practico multi-area con Stub.

[10_MANUAL_BGP_TEORIA_Y_EJERCICIOS_PRACTICOS.md](./10_MANUAL_BGP_TEORIA_Y_EJERCICIOS_PRACTICOS.md)
    - Manual integral de BGP: Sistemas Autonomos, eBGP vs iBGP, Atributos y cascada Best Path,
      Prefix-Lists, Route-Maps y laboratorio empresarial de Multihoming con 2 ISPs.

[11_LABORATORIO_INTEGRAL_Y_REDISTRIBUCION.md](./11_LABORATORIO_INTEGRAL_Y_REDISTRIBUCION.md)
    - Laboratorio de integracion total: Redistribucion multi-protocolo entre OSPF, EIGRP, BGP
      y RIP, metricas semilla obligatorias, prevencion de bucles con Route Tagging y diagnostico.

[12_VPN_IPSEC_SITE_TO_SITE_CISCO_Y_HUAWEI.md](./12_VPN_IPSEC_SITE_TO_SITE_CISCO_Y_HUAWEI.md)
    - Manual exhaustivo de VPN IPsec Site-to-Site inter-sucursales sobre red publica de ISP:
      IKEv1 vs IKEv2, Fases 1 y 2, resolucion de MTU/MSS clamping, implementacion completa
      Route-Based (VTI) en Cisco IOS y Huawei VRP, e interoperabilidad multi-marca.

[13_VPN_IPSEC_HUB_AND_SPOKE_ESCALABILIDAD_OSPF_BGP.md](./13_VPN_IPSEC_HUB_AND_SPOKE_ESCALABILIDAD_OSPF_BGP.md)
    - Manual avanzado de crecimiento y escalabilidad WAN: Sucursales secundarias y terciarias
      conectadas a Sede Maestra sobre ISP, Dynamic VTI, mGRE/NHRP (DMVPN y DSVPN), sucursales
      con IP dinamica y enrutamiento a escala con BGP Dynamic Neighbors y OSPF Totally Stubby.

[14_VPN_IPSEC_ALTA_DISPONIBILIDAD_BALANCEO_Y_REDUNDANCIA.md](./14_VPN_IPSEC_ALTA_DISPONIBILIDAD_BALANCEO_Y_REDUNDANCIA.md)
    - Manual de Alta Disponibilidad y Resiliencia WAN: Balanceo de carga activo/activo con ECMP,
      arquitectura Dual-Hub (HSRP/VRRP en Datacenter), Dual-ISP en sucursales, BGP Multipath
      y conmutacion subsegundo (<300 ms) mediante aceleracion BFD en Cisco IOS-XE y Huawei VRP.

CARPETA EJEMPLOS/ (ENCICLOPEDIA DE 200 EJEMPLOS DE LA VIDA REAL):
    - [00_INDICE_MAESTRO_DE_LOS_200_EJEMPLOS.md](../Ejemplos/00_INDICE_DE_LOS_100_EJEMPLOS_PRACTICOS.md)
    - [01_PARTE_1_SWITCHING_Y_ENRUTAMIENTO_BASICO_001_A_020.md](../Ejemplos/01_PARTE_1_SWITCHING_Y_ENRUTAMIENTO_BASICO_001_A_020.md) (VLANs, Trunk, RoaS, SVIs, Static, RIP)
    - [02_PARTE_2_OSPF_SINGLE_Y_MULTI_AREA_021_A_040.md](../Ejemplos/02_PARTE_2_OSPF_SINGLE_Y_MULTI_AREA_021_A_040.md) (Single/Multi-Area, DR/BDR, Stub, NSSA, Virtual-Link, BFD)
    - [03_PARTE_3_EIGRP_Y_REDISTRIBUCION_041_A_060.md](../Ejemplos/03_PARTE_3_EIGRP_Y_REDISTRIBUCION_041_A_060.md) (DUAL, Variance, Named Mode, Redistribucion, Route-Tags)
    - [04_PARTE_4_BGP_ENTERPRISE_E_ISP_061_A_080.md](../Ejemplos/04_PARTE_4_BGP_ENTERPRISE_E_ISP_061_A_080.md) (eBGP/iBGP, Weight, Local-Pref, Prepend, MED, Dynamic Neighbors)
    - [05_PARTE_5_CASOS_AVANZADOS_VPN_HA_Y_VIDA_REAL_081_A_100.md](../Ejemplos/05_PARTE_5_CASOS_AVANZADOS_VPN_HA_Y_VIDA_REAL_081_A_100.md) (VRF, GRE/IPsec, VTI, HSRP/VRRP, DMVPN, QoS, Core)
    - [06_PARTE_6_DATACENTER_SPINE_LEAF_VXLAN_EVPN_101_A_120.md](../Ejemplos/06_PARTE_6_DATACENTER_SPINE_LEAF_VXLAN_EVPN_101_A_120.md) (Spine-Leaf, VXLAN, BGP EVPN, Anycast GW, vPC, M-LAG, DCI)
    - [07_PARTE_7_MPLS_CARRIER_L3VPN_Y_TRAFFIC_ENG_121_A_140.md](../Ejemplos/07_PARTE_7_MPLS_CARRIER_L3VPN_Y_TRAFFIC_ENG_121_A_140.md) (MPLS LDP, VRF, MP-BGP, PE-CE, RSVP-TE, SR-MPLS, Inter-AS)
    - [08_PARTE_8_ENRUTAMIENTO_IPV6_DUAL_STACK_141_A_160.md](../Ejemplos/08_PARTE_8_ENRUTAMIENTO_IPV6_DUAL_STACK_141_A_160.md) (SLAAC, DHCPv6, OSPFv3, MP-BGP IPv6, Tuneles 6in4, RA Guard)
    - [09_PARTE_9_MULTICAST_Y_QOS_EMPRESARIAL_161_A_180.md](../Ejemplos/09_PARTE_9_MULTICAST_Y_QOS_EMPRESARIAL_161_A_180.md) (PIM-SM, Auto-RP, BSR, Anycast RP, DiffServ, Policing, Shaping, LLQ)

## - [10_PARTE_10_SDWAN_CLOUD_CONNECTIVITY_Y_ZERO_TRUST_181_A_200.md](../Ejemplos/10_PARTE_10_SDWAN_CLOUD_CONNECTIVITY_Y_ZERO_TRUST_181_A_200.md) (AWS Direct Connect, Azure ExpressRoute, SD-WAN, SASE, ZTNA)
