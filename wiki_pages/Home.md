# 🌐 Bienvenido a la Wiki del Manual Maestro de Redes y Ciberseguridad

<p align="center">
  <img src="https://img.shields.io/badge/Wiki-Oficial-blue?style=for-the-badge&logo=github&logoColor=white" alt="Official Wiki" />
  <img src="https://img.shields.io/badge/Repositorio-Principal-005073?style=for-the-badge&logo=git&logoColor=white" alt="Main Repo" />
  <img src="https://img.shields.io/badge/Laboratorios-200%20Casos%20Reales-success?style=for-the-badge" alt="200 Labs" />
  <img src="https://img.shields.io/badge/Sintaxis-Multi--Vendor-orange?style=for-the-badge" alt="Multi-Vendor" />
</p>

---

## 📌 ¿Qué es esta Wiki?

Esta Wiki complementa la [documentación principal del repositorio](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad) sirviendo como **portal de consulta rápida, centro de recursos y guía metodológica** para estudiantes, ingenieros en operación de redes (NOC), administradores de sistemas y analistas de ciberseguridad (SOC).

Mientras que el repositorio contiene el código fuente, guías paso a paso y configuraciones de producción, esta Wiki está diseñada para responder de forma inmediata a:
- ¿Cómo preparo mi certificación (CCNA, CCNP, HCIA, Network+)?
- ¿Cuál es el comando equivalente de Cisco en Huawei, Aruba o HP?
- ¿Cómo configuro mi simulador (Packet Tracer, GNS3 o EVE-NG)?
- ¿Cómo ejecuto las herramientas de diagnóstico en Windows?
- ¿Qué significa un acrónimo o cuál es el RFC de un protocolo?

---

## 🧭 Guías Rápidas de la Wiki

Explora las secciones especializadas a través de los siguientes enlaces:

| Sección | Descripción Técnica |
| :--- | :--- |
| 🎓 **[[Rutas de Certificación\|01.-Rutas-de-Certificacion]]** | Planes de estudio alineados a Cisco CCNA, CCNP ENCOR, CompTIA y Huawei HCIA. |
| 🔄 **[[Matriz Multi-Vendor CLI\|02.-Matriz-Multi-Vendor-CLI]]** | Tabla comparativa de comandos: Cisco IOS vs Huawei VRP vs ArubaOS-CX vs HP vs 3Com vs TP-Link. |
| 🧪 **[[Entornos de Laboratorio y Simulación\|03.-Entornos-de-Laboratorio-y-Simulacion]]** | Cómo montar y aprovechar los 200 laboratorios en Packet Tracer, GNS3 y EVE-NG. |
| 🛠️ **[[Guía de Herramientas Windows\|04.-Guia-de-Herramientas-Windows]]** | Uso paso a paso de la suite en PowerShell (SuperPing, Descubridor PMTU, Wi-Fi Audit). |
| 📖 **[[Glosario y Estándares RFC\|05.-Glosario-y-Estandares-RFC]]** | Diccionario de acrónimos, números de puerto TCP/UDP y estándares oficiales IETF / IEEE. |

---

## 📚 Mapa de los 22 Módulos del Repositorio

Si deseas consultar directamente el código y las guías de configuración en el repositorio, utiliza este mapa directo:

### 1. Fundamentos & Capa Física
- [01. Modelo OSI (7 Capas)](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/OSI)
- [02. Cableado Estructurado y Fibra Óptica](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/Cableado_y_Fibra_Optica)

### 2. Conmutación Multi-Vendor (Switching L2/L3)
- [03. Conmutación Multi-Fabricante](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/SW) (Cisco, Huawei, Aruba, HP, 3Com, TP-Link)
- [19. Troubleshooting y Resolución de Fallas en Switches](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/Troubleshooting)

### 3. Enrutamiento Avanzado, WAN & Operadores
- [04. Routing y WAN](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/Routing_y_WAN) (OSPF, BGP, MPLS L3VPN, SD-WAN)
- [05. Calidad de Servicio (QoS & Traffic Shaping)](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/QoS_Traffic_Shaping)
- [15. Telecomunicaciones Carrier](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/Telecomunicaciones_Avanzadas_Carrier) (5G, DWDM, GPON, SRv6)

### 4. Movilidad & Comunicaciones Unificadas
- [06. Wireless Enterprise](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/Wireless_Enterprise) (Wi-Fi 6/7, WLC 9800, WPA3, Roaming)
- [16. Telefonía IP y VoIP](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/Telefonia) (SIP, RTP, Avaya IP Office, FreePBX)

### 5. Ciberseguridad, Firewalls & Zero Trust
- [07. Control de Acceso e Identidad (AAA)](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/AAA_y_Control_de_Acceso) (802.1X, Cisco ISE, ClearPass)
- [08. Firewalls Perimetrales y VPNs](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/Firewalls_y_VPN) (Stateful NAT, IPsec IKEv2, WireGuard)
- [09. Firewalls NGFW Líderes](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/Firewalls_NGFW_Lideres) (Fortinet, Palo Alto, Cisco FTD)
- [10. Ciberseguridad en Capas OSI](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/Ciberseguridad_OSI) (Defensa en Profundidad, MITRE ATT&CK)
- [11. Redes Industriales OT](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/Redes_Industriales_OT) (Purdue Model, ISA/IEC 62443, SCADA)

### 6. DataCenter, Cloud & Redes Abiertas
- [12. Data Center Fabric](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/DataCenter) (Spine-Leaf, VXLAN EVPN, Cisco NX-OS, SAN)
- [13. Cloud Networking](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/Cloud_Networking) (AWS VPC, Azure VNet, GCP Cloud Router)
- [14. Sistemas Operativos Abiertos (NOS)](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/Sistemas_Operativos_Abiertos_Whitebox) (SONiC, FRR, RouterOS, VyOS)

### 7. Operaciones, Monitoreo & Diagnóstico
- [17. Servicios DDI y Gestión](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/Servicios_DDI_y_Gestion) (DNS Anycast, DHCP Failover, NetBox, SNMPv3)
- [18. Análisis de Paquetes con Wireshark](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/Wireshark_Analysis) (TCP Retransmissions, VoIP, Forense)
- [22. Suite de Herramientas Windows](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/Tools) (SuperPing, Descubridor PMTU, Port Scanner)

### 8. Metodología de Ingeniería & Banco de Laboratorios
- [20. Metodología de Ingeniería y Plantillas](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/Metodologia_Ingenieria_y_Plantillas) (HLD, LLD, MOP, Rollback)
- [21. Banco de 200 Laboratorios Prácticos](https://github.com/Cru9/Manual-Maestro-Redes-Ciberseguridad/tree/main/Ejemplos) (Escenarios 001 al 200)

---

<p align="center">
  <b>Manual Maestro de Redes y Ciberseguridad</b> — Creado por <a href="https://github.com/Cru9">Ezequiel (Cru9)</a>
</p>
