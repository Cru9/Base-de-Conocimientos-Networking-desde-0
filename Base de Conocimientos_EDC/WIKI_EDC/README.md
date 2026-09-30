# 📖 Wiki Maestra EDC: Compendio Enciclopédico Modular
## Base de Conocimientos de Ingeniería de Redes y Ciberseguridad

> **ÍNDICE GENERAL Y GUÍA DE APRENDIZAJE ESTRUCTURADO**  
> **Ubicación:** `Base de Conocimientos_EDC/WIKI_EDC/README.md`  
> **Ecosistema:** 10 Volúmenes Temáticos de Alta Especialidad Técnica

---

## 🏛️ Estructura Modular de la Wiki EDC

La **Wiki EDC** condensa el conocimiento técnico del repositorio en 10 volúmenes rigurosos, corrigiendo las tablas rotas, omisiones y problemas de redacción del proyecto original, e incorporando estándares contemporáneos (Wi-Fi 7, SRv6, EVPN, Zero Trust, NIST SP 800-207 y RFC 9293).

```text
WIKI_EDC/
├── README.md                                         <- Este índice general
├── WIKI_01_Fundamentos_Fisicos_y_Modelo_OSI.md      <- Capa 1 a 7, Medios, TIA-568-D, Fibra, Transceptores, TCP/IP
├── WIKI_02_Switching_MultiVendor_y_Capa2.md         <- Cisco, Huawei, Aruba, HP, 3Com, TP-Link, VLANs, STP, LACP, DAI
├── WIKI_03_Routing_Avanzado_WAN_y_Carrier.md        <- OSPFv2/v3, BGP-4, MPLS L3VPN, SRv6, SD-WAN, QoS DiffServ, BFD
├── WIKI_04_Ciberseguridad_Firewalls_ZeroTrust.md    <- Defensa L1-L7, NGFWs, IPsec IKEv2, WireGuard, 802.1X, Zero Trust
├── WIKI_05_DataCenter_Fabric_y_Cloud_Hybrid.md      <- Spine-Leaf Clos, VXLAN EVPN (RFC 7348/8365), Multi-Cloud, SONiC
├── WIKI_06_Wireless_Enterprise_y_Movilidad.md       <- Wi-Fi 6/6E/7 (802.11ax/be), WLC CAPWAP, WPA3, Roaming 802.11k/v/r
├── WIKI_07_Redes_Industriales_OT_e_IoT.md           <- Modelo Purdue, ISA/IEC 62443, Modbus, DNP3, CIP, Hardening DIN
├── WIKI_08_Servicios_DDI_NetDevOps_y_Gestion.md     <- DNS Anycast, DHCP Failover, NetBox SSoT, NTP, Telemetría, YANG
├── WIKI_09_Analisis_Wireshark_y_Troubleshooting.md   <- Análisis L2-L7, anomalías TCP, VoIP Jitter, Metrología RFC 2544
└── WIKI_10_Banco_Laboratorios_y_Guias_Paso_a_Paso.md<- Matriz de los 200 labs, emulación en EVE-NG, GNS3, CML y Docker
```

---

## 📚 Síntesis de los 10 Volúmenes Temáticos

### [Volumen 01: Fundamentos Físicos y Arquitectura de Modelos](./WIKI_01_Fundamentos_Fisicos_y_Modelo_OSI.md)
- Física de la transmisión de datos (cobre, fibra óptica y radiofrecuencia).
- Estándares de cableado estructurado ANSI/TIA-568-D (Cat 5e a Cat 8) y normas de ponchado T568A vs T568B.
- Fibra óptica monomodo (OS1/OS2) y multimodo (OM1 a OM5), transceptores SFP28/QSFP-DD y presupuesto de potencia óptica.
- Análisis exhaustivo de las 7 capas del modelo OSI vs pila TCP/IP de 4/5 capas, encapsulamiento y ciclo de vida de PDUs.

### [Volumen 02: Conmutación Multi-Vendor y Seguridad de Capa 2](./WIKI_02_Switching_MultiVendor_y_Capa2.md)
- Arquitectura interna de un conmutador: planos de control y reenvío, ASICs, TCAM y tabla CAM.
- Segmentación lógica VLAN (IEEE 802.1Q), enlaces troncales, VLAN nativa y enrutamiento inter-VLAN (Router-on-a-Stick y SVI).
- Protocolos de prevención de bucles: STP clásico (802.1D), Rapid STP (802.1w) y Multiple STP (802.1s).
- Agregación dinámica de enlaces con LACP (IEEE 802.3ad / 802.1AX).
- Hardening de Capa 2: Port Security, DHCP Snooping, Dynamic ARP Inspection (DAI), IP Source Guard y Storm Control.

### [Volumen 03: Enrutamiento Avanzado, Redes WAN y Telecomunicaciones Carrier](./WIKI_03_Routing_Avanzado_WAN_y_Carrier.md)
- Algoritmos de enrutamiento: Vector de distancias (DUAL EIGRP) vs Estado de enlace (Dijkstra OSPF).
- OSPFv2 y OSPFv3 multi-área, jerarquía de áreas (Backbone Área 0, Stub, Totally Stubby, NSSA) y los 11 tipos de LSAs.
- BGP-4 e Internet Routing: Peering eBGP vs iBGP, máquina de estados, algoritmo de decisión y manipulación de atributos.
- MPLS L3VPN (RFC 4364): Etiquetas LDP, VRF, Route Distinguisher (RD) y Route Targets (RT).
- Nuevas tecnologías de transporte: Segment Routing (SR-MPLS / SRv6 RFC 8986) y convergencia BFD sub-segundo.
- Arquitectura de Calidad de Servicio (QoS): Clases DiffServ (RFC 4594), marcado DSCP/CoS, colas LLQ/CBWFQ y descarte WRED.

### [Volumen 04: Ciberseguridad Defensiva, Firewalls NGFW y Zero Trust](./WIKI_04_Ciberseguridad_Firewalls_ZeroTrust.md)
- Modelo de Defensa en Profundidad aplicado de Capa 1 a Capa 7, alineado a la matriz MITRE ATT&CK.
- Cortafuegos de Siguiente Generación (NGFW): Fortinet FortiGate, Palo Alto Networks (App-ID/User-ID) y Cisco FTD (Snort3).
- Cifrado perimetral y túneles VPN: IPsec IKEv2 (ESP, AES-GCM, DH Groups 19/20), WireGuard y DMVPN.
- Control de acceso e identidad: IEEE 802.1X, suplicante/autenticador/servidor, RADIUS, TACACS+ y Cisco ISE.
- Arquitectura Zero Trust según **NIST SP 800-207**: Microsegmentación, eliminación de confianza perimetral implícita y políticas dinámicas.

### [Volumen 05: Data Center Fabrics, Virtualización y Cloud Networking Híbrido](./WIKI_05_DataCenter_Fabric_y_Cloud_Hybrid.md)
- Evolución de centros de datos: De la topología tradicional de 3 capas al diseño Spine-and-Leaf Clos de 2 capas no bloqueante.
- Redes Overlay con VXLAN (RFC 7348) y plano de control BGP EVPN (RFC 7432 / RFC 8365), tipos de ruta 1 a 5.
- Interconexión de nube híbrida y multi-nube: AWS VPC / Transit Gateway, Azure VNet / Virtual WAN / ExpressRoute y GCP Cloud Router.
- Conmutación abierta y Whitebox: Sistema operativo SONiC (arquitectura Docker/SAI), FRRouting y VyOS.

### [Volumen 06: Redes Inalámbricas Corporativas (Wireless Enterprise) y Movilidad](./WIKI_06_Wireless_Enterprise_y_Movilidad.md)
- Fundamentos de radiofrecuencia (RF), bandas de 2.4 GHz, 5 GHz y 6 GHz, espectro de canales y atenuación en espacio libre.
- Evolución de estándares: Wi-Fi 5 (802.11ac), Wi-Fi 6/6E (802.11ax con OFDMA, MU-MIMO y BSS Coloring) y Wi-Fi 7 (802.11be con 320 MHz y MLO).
- Arquitecturas WLC centralizadas con túneles CAPWAP (Split MAC vs Local MAC).
- Seguridad inalámbrica empresarial: WPA3-Personal (SAE) vs WPA3-Enterprise 192-bit y roaming sin interrupciones (802.11k/v/r).

### [Volumen 07: Redes Industriales OT, SCADA e Infraestructura Crítica](./WIKI_07_Redes_Industriales_OT_e_IoT.md)
- Convergencia IT/OT y diferencias en la tríada de seguridad (Disponibilidad e Integridad > Confidencialidad).
- Modelo Purdue (PERA / ISA-95): Niveles 0 a 5 y diseño de la Zona Desmilitarizada Industrial (IDMZ Nivel 3.5).
- Protocolos industriales nativos: Modbus TCP, DNP3, CIP / Ethernet/IP y Profinet.
- Marco de seguridad industrial **ISA/IEC 62443**: Zonas, conductos, niveles de seguridad (SL1 a SL4) y conmutadores rugerizados DIN-Rail.

### [Volumen 08: Servicios Centrales DDI, NetDevOps y Gestión Programática](./WIKI_08_Servicios_DDI_NetDevOps_y_Gestion.md)
- Tríada DDI: Anycast DNS distribuido, alta disponibilidad DHCP Failover (RFC 3074) y NetBox como SSoT.
- Sincronización horaria crítica con NTPv4 (RFC 5905) e introducción a PTP (IEEE 1588).
- Gestión y monitoreo: Migración de SNMPv1/v2c a SNMPv3 seguro (authPriv SHA/AES) y exportación NetFlow/IPFIX.
- NetDevOps y automatización moderna: Modelado de datos YANG (RFC 6020), protocolos NETCONF/RESTCONF y scripts en Python.

### [Volumen 09: Análisis Forense de Paquetes con Wireshark y Resolución de Fallas](./WIKI_09_Analisis_Wireshark_y_Troubleshooting.md)
- Metodología de captura en vivo: Espejeo de puertos SPAN/RSPAN/ERSPAN y TAPs ópticos.
- Filtros de captura (BPF) vs filtros de visualización (Display Filters) de alto nivel.
- Diagnóstico de patologías de transporte TCP: Retransmisiones, paquetes duplicados (Dup-ACK), caída de ventana (ZeroWindow) y reset TCP.
- Análisis de tráfico en tiempo real: VoIP SIP/RTP, cálculo de Jitter, pérdida de paquetes y calificación MOS.
- Metrología y pruebas de enlaces WAN según estándares **RFC 2544** e **ITU-T Y.1564 (EtherSAM)**.

### [Volumen 10: Banco de 200 Laboratorios Prácticos y Guías de Emulación](./WIKI_10_Banco_Laboratorios_y_Guias_Paso_a_Paso.md)
- Estructura y catálogo clasificado de los 200 laboratorios del módulo `Ejemplos/` en 10 partes temáticas.
- Guías de despliegue y topologías en entornos de virtualización: EVE-NG Professional, GNS3, Cisco Modeling Labs (CML) y Containerlab.
- Flujo de trabajo para resolución metódica de laboratorios: Verificación de topología, configuración por bloques y comandos de validación.
