# 🛣️ Pilar 03: Enrutamiento Avanzado, WAN, Telecomunicaciones Carrier y QoS
## Base de Conocimientos EDC

> **CONTENIDO DEL PILAR:** OSPFv2/v3, EIGRP, BGP-4, Redes Carrier MPLS L3VPN, Segment Routing, 5G, DWDM y Calidad de Servicio DiffServ  
> **UBICACIÓN:** `Base de Conocimientos_EDC/Modulos_Clasificados/03_Enrutamiento_WAN_Carrier_y_QoS/README.md`

---

## 📂 Submódulos Incluidos

1. **[`01_Routing_Avanzado_y_WAN/`](./01_Routing_Avanzado_y_WAN/)**  
   - Fundamentos de enrutamiento y rutas estáticas flotantes.
   - OSPF Single-Area y Multi-Area avanzado (Tipos de LSA 1 a 7, áreas Stub/NSSA, BFD).
   - EIGRP corporativo, redistribución de rutas mutua con Route-Maps y Prefix-Lists.
   - BGP-4 Internet Routing (eBGP/iBGP, atributos, peering y convergencia).
   - VPNs IPsec Site-to-Site y Hub-and-Spoke de alta disponibilidad.
   - *Mejora aplicada:* Corrección de la tabla de tipos de LSA en `01_OSPF_MULTI_AREA_AVANZADO.md`.

2. **[`02_Telecomunicaciones_Carrier_5G_Optica/`](./02_Telecomunicaciones_Carrier_5G_Optica/)**  
   - Redes móviles 4G LTE y 5G NR con Open RAN.
   - Transporte óptico de alta capacidad: DWDM, ROADM y OTN.
   - Acceso de última milla: FTTH GPON, XGS-PON y enrutadores BNG.
   - Enrutamiento carrier moderno: Segment Routing (SR-MPLS / SRv6 RFC 8986).
   - Seguridad carrier: Validación criptográfica RPKI y mitigación DDoS con BGP FlowSpec.

3. **[`03_QoS_y_Traffic_Shaping/`](./03_QoS_y_Traffic_Shaping/)**  
   - Arquitectura DiffServ (RFC 2474 / RFC 4594): Clasificación y marcado CoS y DSCP.
   - Mecanismos de colas: LLQ (Low Latency Queuing) y CBWFQ.
   - Prevención de congestión con WRED (Weighted Random Early Detection).
   - Control de tráfico: Policing vs. Traffic Shaping.

---

## 🔗 Referencia Cruzada en la Wiki
- 📘 **[`WIKI_03_Routing_Avanzado_WAN_y_Carrier.md`](../../WIKI_EDC/WIKI_03_Routing_Avanzado_WAN_y_Carrier.md)**
