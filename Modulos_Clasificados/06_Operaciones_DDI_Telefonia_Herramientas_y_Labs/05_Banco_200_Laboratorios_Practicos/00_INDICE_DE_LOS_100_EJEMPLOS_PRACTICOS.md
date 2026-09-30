# 00. INDICE MAESTRO DE LOS 100 EJEMPLOS DE SWITCHING Y ROUTING DE LA VIDA REAL

> **ENRUTAMIENTO AVANZADO Y REDES WAN - GUIA PRACTICA DEFINITIVA**


---


Bienvenido a la coleccion de 100 ejemplos practicos disenados desde los conceptos mas
elementales de Switching y Enrutamiento hasta las arquitecturas mas complejas de
Datacenter, BGP Multihoming, Alta Disponibilidad y VPNs IPsec sobre Internet.

Cada ejemplo cuenta con:
1. Objetivo y Escenario Practico de la Vida Real.
2. Diagrama Topologico ASCII claro y facil de interpretar.
3. Tabla de Direccionamiento IP y Asignacion de Puertos.
4. Configuracion exacta paso a paso lista para copiar y pegar (Cisco IOS-XE / Huawei VRP).
5. Comando de Verificacion y Diagnostico en Produccion.


## ESTRUCTURA DE LOS ARCHIVOS POR NIVELES Y TEMATICAS:



## [PARTE 1] [01_PARTE_1_SWITCHING_Y_ENRUTAMIENTO_BASICO_001_A_020.md](./01_PARTE_1_SWITCHING_Y_ENRUTAMIENTO_BASICO_001_A_020.md)

  Ejemplo 001: Conexion basica de dos switches con VLAN de gestion y acceso.
  Ejemplo 002: Segmentacion departamental con VLANs independientes (VLAN 10 y 20).
  Ejemplo 003: Enlace Troncal 802.1Q con asignacion de VLAN Nativa segura.
  Ejemplo 004: Enrutamiento Inter-VLAN mediante Router-on-a-Stick (Subinterfaces).
  Ejemplo 005: Enrutamiento Inter-VLAN en Switch Layer 3 mediante SVIs e IP Routing.
  Ejemplo 006: Puerto enrutado directo (no switchport) en Switch Multicapa.
  Ejemplo 007: Agregacion de enlaces L2 con LACP (Port-Channel / EtherChannel).
  Ejemplo 008: EtherChannel Layer 3 con direccion IP directa entre switches Core.
  Ejemplo 009: Servidor DHCP configurado en Router con pools por VLAN y exclusiones.
  Ejemplo 010: Agente de Reenvio DHCP (ip helper-address) hacia servidor central.
  Ejemplo 011: Ruta Estatica Directa punto a punto entre dos sedes.
  Ejemplo 012: Ruta por Defecto (0.0.0.0/0) hacia el Gateway de salida a Internet.
  Ejemplo 013: Ruta Estatica Flotante (Floating Route) con AD 10 para backup automatico.
  Ejemplo 014: Ruta de Host (/32) para dirigir trafico hacia un servidor critico.
  Ejemplo 015: Ruta de Descarte hacia Null0 para mitigar ataques y prevenir bucles.
  Ejemplo 016: RIPv2 basico entre routers con desactivacion de auto-sumarizacion.
  Ejemplo 017: RIPv2 con interfaces pasivas (passive-interface) en puertos de usuarios.
  Ejemplo 018: Inyeccion de ruta por defecto en RIPv2 (default-information originate).
  Ejemplo 019: RIPv2 con autenticacion criptografica MD5 entre sucursales.
  Ejemplo 020: Sumarizacion manual de prefijos en RIPv2 por interfaz WAN.


## [PARTE 2] [02_PARTE_2_OSPF_SINGLE_Y_MULTI_AREA_021_A_040.md](./02_PARTE_2_OSPF_SINGLE_Y_MULTI_AREA_021_A_040.md)

  Ejemplo 021: OSPF Single-Area basico en Area 0 mediante comando network y wildcard.
  Ejemplo 022: OSPF activado directamente bajo la interfaz fisica (ip ospf 1 area 0).
  Ejemplo 023: Asignacion manual y estandarizada de Router-ID (Loopback0).
  Ejemplo 024: Ajuste de Ancho de Banda de Referencia (auto-cost reference-bandwidth).
  Ejemplo 025: Seguridad en OSPF mediante passive-interface default.
  Ejemplo 026: Eleccion forzada de DR y BDR mediante prioridades de interfaz (255 y 0).
  Ejemplo 027: Red OSPF Punto a Punto en Ethernet para suprimir DR/BDR y acelerar.
  Ejemplo 028: Modificacion de metricas OSPF con costo manual (ip ospf cost).
  Ejemplo 029: Propagacion de ruta por defecto en OSPF (default-information originate).
  Ejemplo 030: Autenticacion OSPF por interfaz con clave criptografica MD5 / SHA-256.
  Ejemplo 031: OSPF Multi-Area basico conectando Area 0 (Core) con Area 10 (Planta).
  Ejemplo 032: Identificacion de roles (ABR, ASBR) e inspeccion de LSAs 1, 2 y 3.
  Ejemplo 033: Sumarizacion Inter-Area en el ABR (area range) para optimizar tablas.
  Ejemplo 034: Area Stub en sucursal para bloquear rutas externas (LSA 4 y 5).
  Ejemplo 035: Area Totally Stubby (Cisco) para inyectar solo la ruta por defecto.
  Ejemplo 036: Area NSSA (Not-So-Stubby Area) con ASBR redistribuyendo rutas externas.
  Ejemplo 037: Area Totally NSSA con bloqueo de LSAs 3, 4 y 5.
  Ejemplo 038: Enlace Virtual OSPF (Virtual-Link) para conectar un area aislada al Area 0.
  Ejemplo 039: Afinacion de temporizadores OSPF Hello/Dead y BFD para convergencia subsegundo.
  Ejemplo 040: Filtrado de prefijos entre areas mediante Filter-Lists en el ABR.


## [PARTE 3] [03_PARTE_3_EIGRP_Y_REDISTRIBUCION_041_A_060.md](./03_PARTE_3_EIGRP_Y_REDISTRIBUCION_041_A_060.md)

  Ejemplo 041: EIGRP clasico basico con Sistema Autonomo (AS 100).
  Ejemplo 042: EIGRP con mascaras wildcard exactas y no auto-summary.
  Ejemplo 043: Asignacion de Router-ID y passive-interface en EIGRP.
  Ejemplo 044: Inspeccion de DUAL: Calculo de FD, RD, Sucesor y Sucesor Factible.
  Ejemplo 045: Balanceo de carga en rutas desiguales mediante multiplicador variance.
  Ejemplo 046: EIGRP Stub Routing para proteger sucursales y evitar consultas SIA.
  Ejemplo 047: Sumarizacion manual de rutas en interfaces de salida EIGRP.
  Ejemplo 048: Autenticacion criptografica MD5 con Key-Chain en EIGRP clasico.
  Ejemplo 049: EIGRP Named Mode (Modo Nombrado moderno de Cisco IOS-XE).
  Ejemplo 050: Autenticacion HMAC-SHA-256 en EIGRP Named Mode.
  Ejemplo 051: Redistribucion de rutas conectadas hacia OSPF con subnets.
  Ejemplo 052: Redistribucion de rutas estaticas hacia EIGRP con metrica semilla K1-K5.
  Ejemplo 053: Redistribucion mutua controlada OSPF <-> EIGRP en router de frontera.
  Ejemplo 054: Prevencion de bucles por redistribucion mediante Route-Tagging (Tags 90/110).
  Ejemplo 055: Filtrado granular de prefijos en redistribucion con Prefix-Lists.
  Ejemplo 056: Redistribucion de RIPv2 hacia OSPF: Comparativa de Metrica E1 vs E2.
  Ejemplo 057: Modificacion de Distancia Administrativa para resolver ruteo suboptimo.
  Ejemplo 058: Inyeccion de ruta por defecto desde EIGRP hacia el dominio OSPF.
  Ejemplo 059: Afinacion de Hello y Hold-Time en EIGRP para enlaces WAN satelitales.
  Ejemplo 060: Diagnostico y correccion de error por discrepancia de valores K (K-Mismatch).


## [PARTE 4] [04_PARTE_4_BGP_ENTERPRISE_E_ISP_061_A_080.md](./04_PARTE_4_BGP_ENTERPRISE_E_ISP_061_A_080.md)

  Ejemplo 061: Sesion eBGP basica entre dos Sistemas Autonomos diferentes.
  Ejemplo 062: Anuncio de prefijos en BGP con coincidencia estricta de mascara.
  Ejemplo 063: Sesion eBGP sobre direcciones Loopback con ebgp-multihop.
  Ejemplo 064: Sesion iBGP interna en el mismo ASN mediante direccion Loopback.
  Ejemplo 065: Correccion de Next-Hop inalcanzable con neighbor next-hop-self en iBGP.
  Ejemplo 066: BGP Route Reflector (RR) para suprimir la malla completa de sesiones iBGP.
  Ejemplo 067: Manipulacion del atributo WEIGHT para forzar salida por router local.
  Ejemplo 068: Control de trafico de salida (Outbound) con LOCAL PREFERENCE.
  Ejemplo 069: Control de trafico de entrada (Inbound) con AS-PATH PREPENDING.
  Ejemplo 070: Control de entrada entre enlaces redundantes al mismo ISP con MED.
  Ejemplo 071: Filtrado de prefijos entrantes del ISP con Prefix-Lists de seguridad.
  Ejemplo 072: Politica estricta de exportacion para evitar ser Sistema Autonomo de Transito.
  Ejemplo 073: Uso de BGP Communities para etiquetar y automatizar politicas de trafico.
  Ejemplo 074: Sumarizacion y condensacion de rutas BGP con aggregate-address summary-only.
  Ejemplo 075: Actualizacion de politicas en caliente con BGP Soft Reconfiguration y Route Refresh.
  Ejemplo 076: BGP Multipath (maximum-paths) para balanceo de carga ECMP sobre Internet.
  Ejemplo 077: Multihoming corporativo conectado a dos ISPs diferentes con failover.
  Ejemplo 078: BGP Dynamic Neighbors (bgp listen range) para recepcion automatica de sucursales.
  Ejemplo 079: Autenticacion TCP MD5 en sesiones BGP para proteccion de peering.
  Ejemplo 080: Aceleracion de conmutacion BGP con BFD (fall-over bfd) en 300 ms.


## [PARTE 5] [05_PARTE_5_CASOS_AVANZADOS_VPN_HA_Y_VIDA_REAL_081_A_100.md](./05_PARTE_5_CASOS_AVANZADOS_VPN_HA_Y_VIDA_REAL_081_A_100.md)

  Ejemplo 081: VRF Lite para aislamiento logico de trafico Corporativo vs Invitados.
  Ejemplo 082: Enrutamiento Inter-VRF mediante servicios compartidos y rutas estaticas.
  Ejemplo 083: Tunel GRE punto a punto simple sin cifrar sobre Internet.
  Ejemplo 084: Tunel GRE sobre IPsec (GRE over IPsec) para transportar OSPF seguro.
  Ejemplo 085: VPN IPsec VTI Route-Based con IKEv2 moderna entre dos oficinas.
  Ejemplo 086: Ajuste obligatorio de MTU y TCP MSS Clamping en interfaces de tunel.
  Ejemplo 087: Redundancia de Gateway LAN con HSRP en routers Cisco.
  Ejemplo 088: Redundancia de Gateway con VRRP v2/v3 y tracking de interfaz WAN.
  Ejemplo 089: Balanceo de carga en Gateway LAN con GLBP (Gateway Load Balancing Protocol).
  Ejemplo 090: Conmutacion automatica Fibra a 5G mediante IP SLA y Object Tracking.
  Ejemplo 091: DMVPN Fase 1 (Hub-and-Spoke basico con mGRE y NHRP).
  Ejemplo 092: DMVPN Fase 2 con atajos directos Spoke-to-Spoke por Internet.
  Ejemplo 093: DMVPN Fase 3 con NHRP Redirect y Shortcut para cientos de sucursales.
  Ejemplo 094: Redundancia Dual-Hub en Datacenter (Hub 1 y Hub 2 con BGP).
  Ejemplo 095: Sucursal con IP publica dinamica por DHCP conectandose a Hub con IKEv2 Wildcard.
  Ejemplo 096: Interoperabilidad multi-marca: Router Cisco Core y Router Huawei AR con IPsec.
  Ejemplo 097: Policy-Based Routing (PBR) para desviar trafico critico por enlace dedicado.
  Ejemplo 098: Calidad de Servicio (QoS) en WAN: Marcado DSCP y cola prioritaria LLQ para VoIP.
  Ejemplo 099: Mitigacion de inestabilidad WAN mediante IP Event Dampening (Anti-Flapping).
  Ejemplo 100: Arquitectura Integral de Red Empresarial: Core redundante, Edge Dual-ISP,

## Firewalls en Cluster y OSPF/BGP hacia sucursales remotas.
