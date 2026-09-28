# 00. INDICE GENERAL, ARQUITECTURA INTEGRAL Y MAPA DE CAPAS DE UN OPERADOR (ISP/TELCO)

> **TELECOMUNICACIONES AVANZADAS, REDES DE CARRIER E INFRAESTRUCTURA GLOBAL**


---



## 1. ¿QUE DEFINE A UN MAESTRO EN TELECOMUNICACIONES?

Un ingeniero de redes corporativas (Enterprise) disena y opera las redes de una
empresa: conecta oficinas, configura VLANs, gestiona firewalls y levanta tuneles VPN.

Un MAESTRO EN TELECOMUNICACIONES (Nivel Principal Carrier Architect / CCIE Service Provider)
opera la infraestructura troncal subyacente que hace posible la comunicacion del planeta:
- Conecta paises y continentes a traves de cables submarinos y redes DWDM de terabits.
- Gestiona los sistemas autonomos (ASNs) de Nivel 1 (Tier 1 ISPs) que forman la tabla
  global de enrutamiento de Internet (DFZ - Default-Free Zone).
- Construye las redes celulares 4G y 5G que dan servicio a millones de dispositivos moviles.
- Despliega redes de acceso masivo de fibra optica (FTTH GPON/XGS-PON) y radioenlaces.
- Programa la red como codigo mediante NetDevOps, APIs de silicio y telemetria en tiempo real.
- Protege la columna vertebral de Internet contra ataques de denegacion de servicio (DDoS)
  masivos y secuestros de rutas mediante criptografia RPKI.



## 2. EL MAPA DE CAPAS DE UN OPERADOR DE TELECOMUNICACIONES (CARRIER STACK)

La operacion de un gran operador de telecomunicaciones (Telco / ISP Tier-1 / Carrier)
se organiza en una jerarquia de capas interconectadas:

```text
+-----------------------------------------------------------------------------+
| CAPA 7: GESTION, NETDEVOPS Y AUTOMATIZACION (Orquestacion Global)           |
| - Programabilidad con Python (Nornir, Scrapli), APIs NETCONF / RESTCONF     |
| - Modelos de Datos YANG (OpenConfig), Streaming Telemetry gNMI/gRPC         |
| - Plataformas de Facturacion (BSS/OSS) y Aprovisionamiento Automatico      |
+-----------------------------------------------------------------------------+
                                      |
+-----------------------------------------------------------------------------+
| CAPA 6: SERVICIOS MOVILES Y DE USUARIO FINAL                                |
| - Red Celular 5G Core (SBA: AMF, SMF, UPF) y 4G LTE EPC (MME, SGW, PGW)    |
| - Open RAN (O-RAN: RU, DU, CU desagregados sobre fibra eCPRI)               |
| - Network Slicing (eMBB, URLLC < 1 ms, mMTC IoT) y Comunicacion Satelital   |
+-----------------------------------------------------------------------------+
                                      |
+-----------------------------------------------------------------------------+
| CAPA 5: SEGURIDAD DE INFRAESTRUCTURA Y CONTROL GLOBAL BGP                   |
| - Criptografia RPKI y Validacion de Origen de Rutas (ROV)                   |
| - Mitigacion DDoS Carrier: BGP Flowspec (RFC 8955) y Blackholing RTBH       |
+-----------------------------------------------------------------------------+
                                      |
+-----------------------------------------------------------------------------+
| CAPA 4: ENRUTAMIENTO TRONCAL (CARRIER CORE IP/MPLS Y SEGMENT ROUTING)       |
| - Segment Routing (SR-MPLS y SRv6 nativo con cabeceras IPv6 SRH)            |
| - Resiliencia Absoluta: TI-LFA (Topology-Independent LFA con failover <50ms)|
| - Ingenieria de Trafico Dinamica (SR-TE) y BGP Multi-Protocolo (MP-BGP)     |
+-----------------------------------------------------------------------------+
                                      |
+-----------------------------------------------------------------------------+
| CAPA 3: ACCESO Y AGREGACION METROPOLITANA (LAST MILE & METRO)               |
| - Acceso Fijo FTTH: GPON (2.5G/1.25G) y XGS-PON (10G Simetrico)             |
| - Concentradores de Banda Ancha BNG/BRAS (IPoE DHCP Option 82 / PPPoE)      |
| - Transporte Inalambrico: Radioenlaces Microondas (6-38 GHz) y E-Band (80G) |
+-----------------------------------------------------------------------------+
                                      |
+-----------------------------------------------------------------------------+
| CAPA 2: TRANSPORTE DIGITAL DE ALTA CAPACIDAD (OTN - OPTICAL TRANSPORT NET)  |
| - Tramas digitales ITU-T G.709 (OPUk, ODUk, OTUk) con conmutacion de lambdas|
| - Correccion de Errores hacia Adelante (Soft-Decision FEC)                  |
+-----------------------------------------------------------------------------+
                                      |
+-----------------------------------------------------------------------------+
| CAPA 1 / 0: CAPA FISICA Y FOTONICA (DWDM Y FIBRA OPTICA)                    |
| - Multiplexacion DWDM en Banda C / Flex-Grid (canales de 400G / 800G)       |
| - Conmutadores Opticos Reconfigurables ROADM CDC (WSS)                      |
| - Amplificadores Opticos de Luz: EDFA y Amplificacion Raman                 |
| - Fibra Optica ITU-T G.652D, G.654 (Submarina) y G.657 (Curvatura FTTH)    |
+-----------------------------------------------------------------------------+
```


## 3. INDICE ANALITICO DE LA CARPETA TELECOMUNICACIONES_AVANZADAS_CARRIER

[00_INDICE_MAESTRO_TELECOMUNICACIONES_CARRIER.md](./00_INDICE_MAESTRO_TELECOMUNICACIONES_CARRIER.md)
    - Indice general, marco metodologico y mapa de capas de un operador global de telecomunicaciones.

[01_REDES_MOVILES_4G_LTE_5G_NR_Y_OPEN_RAN.md](./01_REDES_MOVILES_4G_LTE_5G_NR_Y_OPEN_RAN.md)
    - Redes Celulares: Evolucion de 4G EPC a 5G Core Basado en Servicios (SBA).
    - Descomposicion Open RAN (RU, DU, CU, eCPRI), Network Slicing (eMBB, URLLC, mMTC) y protocolos GTP/Diameter.

[02_TRANSPORTE_OPTICO_WDM_DWDM_ROADM_Y_OTN.md](./02_TRANSPORTE_OPTICO_WDM_DWDM_ROADM_Y_OTN.md)
    - Capa Fotonica y Optica: Ventanas de transmision, tipos de fibra ITU-T, dispersion y efectos no lineales.
    - CWDM vs DWDM Flex-Grid, Amplificadores EDFA/Raman, ROADM CDC y tramas digitales OTN (G.709) con SD-FEC.

[03_ACCESO_ULTIMA_MILLA_FTTH_GPON_XGSPON_Y_BNG.md](./03_ACCESO_ULTIMA_MILLA_FTTH_GPON_XGSPON_Y_BNG.md)
    - Redes de Acceso de Fibra: Topologia ODN pasiva (splitters 1:64), GPON y XGS-PON simetrico (10 Gbps).
    - Protocolo de gestion OMCI y concentradores de acceso BNG/BRAS con IPoE (Option 82), PPPoE y Dual-Stack IPv6.

[04_NETDEVOPS_AUTOMATIZACION_PYTHON_YANG_NETCONF_RESTCONF.md](./04_NETDEVOPS_AUTOMATIZACION_PYTHON_YANG_NETCONF_RESTCONF.md)
    - Automatizacion y Programabilidad Carrier: Modelado de datos con YANG (OpenConfig), APIs NETCONF (XML/SSH),
      RESTCONF (JSON/HTTPS) y Streaming Telemetry gNMI/gRPC. Scripts de produccion con Python (Scrapli, Nornir).

[05_ENRUTAMIENTO_CARRIER_SEGMENT_ROUTING_SR_MPLS_Y_SRV6.md](./05_ENRUTAMIENTO_CARRIER_SEGMENT_ROUTING_SR_MPLS_Y_SRV6.md)
    - La evolucion del Core Carrier: De LDP/RSVP-TE a Segment Routing (Source Routing sin estado intermedio).
    - SR-MPLS con SRGB y SRv6 nativo con cabeceras de extension SRH (Micro-SIDs). Resiliencia TI-LFA (<50 ms).

[06_RADIOENLACES_MICROONDAS_PTP_PTMP_Y_EBAND.md](./06_RADIOENLACES_MICROONDAS_PTP_PTMP_Y_EBAND.md)
    - Transmision Inalambrica de Transporte: Bandas licenciadas (6 a 38 GHz) y Bandas milimetricas E-Band (70/80 GHz).
    - Calculo de Enlace (Link Budget), Zona de Fresnel, atenuacion por lluvia (ITU-R P.530) y modulacion adaptativa (ACM).

[07_COMUNICACIONES_SATELITALES_LEO_GEO_VSAT_Y_NTN.md](./07_COMUNICACIONES_SATELITALES_LEO_GEO_VSAT_Y_NTN.md)
    - Comunicaciones Espaciales: Orbitas GEO vs LEO (Starlink/OneWeb), redes no terrestres (3GPP NTN Direct-to-Cell),
      arquitectura de terminales VSAT (BUC, LNB, modems DVB-S2X), acceso MF-TDMA/SCPC y protocolos DTN.

[08_SEGURIDAD_CARRIER_RPKI_BGP_FLOWSPEC_Y_ANTIDDOS.md](./08_SEGURIDAD_CARRIER_RPKI_BGP_FLOWSPEC_Y_ANTIDDOS.md)
    - Defensa de la Infraestructura Global de Internet: RPKI ROV contra secuestros de prefijos (BGP Hijacking),

normas MANRS, mitigacion de DDoS volumetrico con BGP Flowspec (RFC 8955) y Blackholing remoto (RTBH).
