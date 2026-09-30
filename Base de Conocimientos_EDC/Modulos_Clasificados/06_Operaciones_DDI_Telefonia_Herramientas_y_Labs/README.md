# 🛠️ Pilar 06: Operaciones DDI, Telefonía IP, Forense Wireshark, Metodología IT, Banco de 200 Labs y Tools
## Base de Conocimientos EDC

> **CONTENIDO DEL PILAR:** Servicios centrales DDI, Telefonía VoIP Avaya/Asterisk, Análisis Wireshark, Plantillas HLD/LLD/MOP, 200 Laboratorios Prácticos y Suite de Scripts Windows  
> **UBICACIÓN:** `Base de Conocimientos_EDC/Modulos_Clasificados/06_Operaciones_DDI_Telefonia_Herramientas_y_Labs/README.md`

---

## 📂 Submódulos Incluidos

1. **[`01_Servicios_DDI_y_Gestion/`](./01_Servicios_DDI_y_Gestion/)**  
   - Anycast DNS con BGP, DHCP Failover con Opción 82 y NetBox IPAM SSoT.
   - Sincronización horaria crítica con NTPv4 autenticado (RFC 5905).
   - Monitoreo con SNMPv3 authPriv y telemetría de flujos NetFlow/IPFIX.

2. **[`02_Telefonia_VoIP_Avaya_y_Asterisk/`](./02_Telefonia_VoIP_Avaya_y_Asterisk/)**  
   - Fundamentos de VoIP: Protocolo SIP (RFC 3261), RTP (RFC 3550) y códecs G.711 / G.729.
   - Ecosistema comercial: Avaya IP Office 500v2, Manager, SCN multi-sitio y archivos `46xxsettings.txt`.
   - Ecosistema Open Source: Asterisk core, FreePBX, Issabel, módulos PJSIP, IVR y dialplans.

3. **[`03_Analisis_Wireshark/`](./03_Analisis_Wireshark/)**  
   - Filtros de captura (BPF) vs. filtros de visualización de Wireshark.
   - Diagnóstico profundo de transporte TCP: Retransmisiones RTO, Dup-ACKs, TCP ZeroWindow y resets RST.
   - Diagnóstico de VoIP y análisis de streams RTP (Jitter, pérdida de paquetes y cálculo MOS).
   - Casos forenses de red y resolución de cuellos de botella.

4. **[`04_Metodologia_Ingenieria_Plantillas/`](./04_Metodologia_Ingenieria_Plantillas/)**  
   - Estándares de documentación corporativa IT.
   - Plantilla HLD (High-Level Design).
   - Plantilla LLD (Low-Level Design).
   - Plantilla MOP (Method of Procedure) para ventanas de cambio críticas con plan de rollback.

5. **[`05_Banco_200_Laboratorios_Practicos/`](./05_Banco_200_Laboratorios_Practicos/)**  
   - Los **200 laboratorios prácticos originales** del compendio organizados en 10 partes temáticas:
     - Parte 1: 001-020 (Switching Base, VLANs, Troncales, SVI, Rutas Estáticas).
     - Parte 2: 021-040 (OSPF Single y Multi-Área, DR/BDR, Autenticación).
     - Parte 3: 041-060 (EIGRP Corporativo, Sumarización y Redistribución).
     - Parte 4: 061-080 (BGP Enterprise e ISP, Peering eBGP/iBGP, Atributos).
     - Parte 5: 081-100 (Redundancia FHRP HSRP/VRRP, IPsec IKEv2, Dual WAN).
     - Parte 6: 101-120 (Data Center Spine-Leaf Clos, Overlays VXLAN y BGP EVPN).
     - Parte 7: 121-140 (Redes Carrier MPLS L3VPN, LDP e Ingeniería de Tráfico).
     - Parte 8: 141-160 (IPv6 Empresarial, Dual-Stack, SLAAC, DHCPv6, OSPFv3).
     - Parte 9: 161-180 (Multicast PIM-SM, IGMP y Calidad de Servicio QoS MQC).
     - Parte 10: 181-200 (SD-WAN, Multi-Cloud AWS/Azure y Zero Trust NAC).

6. **[`06_Suite_Herramientas_Scripts/`](./06_Suite_Herramientas_Scripts/)**  
   - Scripts nativos de diagnóstico en PowerShell (.ps1) para Windows: SuperPing, Descubridor PMTU, Wi-Fi Audit, auditoría TCP y resolución DNS rápida.

7. **[`07_Wiki_Pages_Originales/`](./07_Wiki_Pages_Originales/)**  
   - Copia de respaldo de las páginas de wiki originales del repositorio.

---

## 🔗 Referencias Cruzadas en la Wiki
- 📘 **[`WIKI_08_Servicios_DDI_NetDevOps_y_Gestion.md`](../../WIKI_EDC/WIKI_08_Servicios_DDI_NetDevOps_y_Gestion.md)**
- 📘 **[`WIKI_09_Analisis_Wireshark_y_Troubleshooting.md`](../../WIKI_EDC/WIKI_09_Analisis_Wireshark_y_Troubleshooting.md)**
- 📘 **[`WIKI_10_Banco_Laboratorios_y_Guias_Paso_a_Paso.md`](../../WIKI_EDC/WIKI_10_Banco_Laboratorios_y_Guias_Paso_a_Paso.md)**
