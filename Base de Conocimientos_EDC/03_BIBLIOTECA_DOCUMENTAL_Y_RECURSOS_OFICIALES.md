# 📚 Biblioteca Documental, Bibliografía Maestra y Recursos Oficiales EDC
## Network Engineering & Cybersecurity Master Compendium

> **COMPENDIO DE FUENTES DE INFORMACIÓN TÉCNICA OFICIAL, ESTÁNDARES Y ENLACES DIRECTOS**  
> **Ubicación:** `Base de Conocimientos_EDC/03_BIBLIOTECA_DOCUMENTAL_Y_RECURSOS_OFICIALES.md`  
> **Ecosistema:** IETF (RFCs), IEEE, TIA/EIA, ISO/IEC, NIST, ITU-T, Cisco Press, Huawei y O'Reilly

---

## 1. Bibliografía Maestra de Libros Fundamentales y de Certificación

### A. Libros de Conmutación, Enrutamiento y Arquitectura IP
1. **Doyle, Jeff & Carroll, Jennifer.** *Routing TCP/IP, Volume 1 (2nd Edition).* Cisco Press. ISBN: 978-1587052026.
   - *Relevancia:* El texto canónico para dominar en profundidad OSPF, IS-IS, manipulación de métricas, diseño de áreas y algoritmos de estado de enlace.
2. **Doyle, Jeff & Carroll, Jennifer.** *Routing TCP/IP, Volume 2 (2nd Edition).* Cisco Press. ISBN: 978-1587054709.
   - *Relevancia:* La referencia de cabecera para BGP-4, enrutamiento multicast PIM-SM/SSM, NAT y políticas de enrutamiento exterior.
3. **Odom, Wendell.** *CCNA 200-301 Official Cert Guide, Volumes 1 & 2.* Cisco Press. ISBN: 978-0136766421.
   - *Relevancia:* La guía fundamental para los exámenes de certificación CCNA, abordando conmutación Ethernet, subredes, ruteo estático, OSPF y servicios IP.
4. **Edgeworth, Brad; Garza, Rios; Gooley, Jason.** *CCNP and CCIE Enterprise Core ENCOR 350-401 Official Cert Guide.* Cisco Press. ISBN: 978-1587145230.
   - *Relevancia:* Texto indispensable para diseño corporativo avanzado, alta disponibilidad L3, virtualización de redes, SD-WAN y automatización REST/YANG.
5. **Zhang, Randy & Bartell, Jim.** *BGP Design and Implementation.* Cisco Press. ISBN: 978-1587051098.
   - *Relevancia:* Guía definitiva para el diseño de peering de Internet, mitigación de flapping de rutas y optimización de atributos BGP corporativos.
6. **Huawei Technologies Co., Ltd.** *Data Communication and Networking: Master Advanced HCIP Datacom.* Springer. ISBN: 978-9811985003.
   - *Relevancia:* Texto oficial para ingenieros que operan infraestructura Huawei VRP, cubriendo switches CloudEngine, routers AR y conmutación Eth-Trunk.

### B. Ciberseguridad, Firewalls y Defensa en Profundidad
1. **Gilman, Evan & Barth, Doug.** *Zero Trust Networks: Building Secure Systems in Untrusted Networks.* O'Reilly Media. ISBN: 978-1491962190.
   - *Relevancia:* Fundamentos conceptuales de la arquitectura Zero Trust, control de identidad dinámico, microsegmentación y eliminación del perímetro estático.
2. **McNab, Chris.** *Network Security Assessment: Know Your Network (3rd Edition).* O'Reilly Media. ISBN: 978-1491910955.
   - *Relevancia:* Metodologías prácticas de auditoría técnica, escaneo de puertos, análisis de debilidades en servicios L4-L7 e intercepción de tráfico.
3. **Sanders, Chris.** *Practical Packet Analysis: Using Wireshark to Solve Real-World Network Problems (3rd Edition).* No Starch Press. ISBN: 978-1593278021.
   - *Relevancia:* El manual definitivo para dominar Wireshark, decodificar anomalías de transporte TCP, cuellos de botella de ancho de banda y rastreo de intrusiones.
4. **Stallings, William.** *Cryptography and Network Security: Principles and Practice (8th Edition).* Pearson. ISBN: 978-0135764039.
   - *Relevancia:* Fundamentos matemáticos y operativos de algoritmos de cifrado simétrico (AES-GCM), asimétrico (RSA, ECC), funciones hash (SHA-2/SHA-3) e IPsec/TLS.

### C. Data Center, Cloud Híbrido y Carrier Networking
1. **Banks, Ethan & Lindberg, Ned.** *IP Fabric Architecture: Modern Data Center Networks with VXLAN EVPN.* O'Reilly.
   - *Relevancia:* Guía práctica para ingenieros de datacenter que despliegan fábricas Spine-Leaf no bloqueantes basadas en RFC 7348 y RFC 8365.
2. **Filsfils, Clarence et al.** *Segment Routing: Part I & II (SR-MPLS and SRv6).* Cisco Press.
   - *Relevancia:* Redactado por los creadores de Segment Routing en la IETF, desglosa la simplificación del plano de control en redes 5G y de proveedores de servicios.
3. **Hunt, Craig.** *TCP/IP Network Administration (3rd Edition).* O'Reilly Media. ISBN: 978-0596002978.
   - *Relevancia:* Referencia operativa para servicios esenciales Linux DDI: BIND DNS, ISC-DHCP, NTP e interfaces de red.

---

## 2. Catálogo Oficial de RFCs de la IETF por Dominio Técnico (con Enlaces Activos)

### A. Capa de Enlace y Red Básica (L2 / L3)
* [RFC 791 - Internet Protocol (IPv4 Specification)](https://datatracker.ietf.org/doc/html/rfc791) - Define la estructura original del paquete IPv4, fragmentación y direccionamiento de 32 bits.
* [RFC 826 - Address Resolution Protocol (ARP)](https://datatracker.ietf.org/doc/html/rfc826) - Protocolo para resolver direcciones lógicas de capa de red en direcciones físicas de capa de enlace.
* [RFC 1918 - Address Allocation for Private Internets](https://datatracker.ietf.org/doc/html/rfc1918) - Asigna los rangos privados `10.0.0.0/8`, `172.16.0.0/12` y `192.168.0.0/16`.
* [RFC 4632 - Classless Inter-domain Routing (CIDR)](https://datatracker.ietf.org/doc/html/rfc4632) - Especifica la agregación y división flexible de prefijos IP sin clases fijas.
* [RFC 8200 - Internet Protocol, Version 6 (IPv6) Specification](https://datatracker.ietf.org/doc/html/rfc8200) - Norma estándar de Internet completa para IPv6 (reemplaza a la RFC 2460).

### B. Capa de Transporte (L4)
* [RFC 768 - User Datagram Protocol (UDP)](https://datatracker.ietf.org/doc/html/rfc768) - Protocolo simple de transporte no orientado a conexión ni a control de flujo.
* [RFC 9293 - Transmission Control Protocol (TCP)](https://datatracker.ietf.org/doc/html/rfc9293) - **Especificación maestra moderna de TCP** que unifica y actualiza formalmente la histórica RFC 793 y sus extensiones.
* [RFC 9000 - QUIC: A UDP-Based Multiplexed and Secure Transport](https://datatracker.ietf.org/doc/html/rfc9000) - Protocolo de transporte multiplexado sobre UDP que impulsa HTTP/3.

### C. Enrutamiento Dinámico Interior y Exterior (IGP / EGP)
* [RFC 2328 - OSPF Version 2](https://datatracker.ietf.org/doc/html/rfc2328) - Protocolo de enrutamiento interior de estado de enlace para IPv4.
* [RFC 3101 - The OSPF Not-So-Stubby Area (NSSA) Option](https://datatracker.ietf.org/doc/html/rfc3101) - Define el tipo de área NSSA y la conversión de LSAs Tipo 7 a Tipo 5 en el ABR.
* [RFC 5340 - OSPF for IPv6 (OSPFv3)](https://datatracker.ietf.org/doc/html/rfc5340) - Adapta el funcionamiento de OSPF al direccionamiento de 128 bits e introduce nuevas LSAs.
* [RFC 4271 - A Border Gateway Protocol 4 (BGP-4)](https://datatracker.ietf.org/doc/html/rfc4271) - Especificación del protocolo de vector de rutas de Internet.
* [RFC 4760 - Multiprotocol Extensions for BGP-4 (MP-BGP)](https://datatracker.ietf.org/doc/html/rfc4760) - Permite a BGP transportar información de enrutamiento para IPv6, MPLS VPNs y EVPN.
* [RFC 5880 - Bidirectional Forwarding Detection (BFD)](https://datatracker.ietf.org/doc/html/rfc5880) - Detección rápida de fallas de enlace en submilisegundos.
* [RFC 8955 - Dissemination of Flow Specification Rules (BGP FlowSpec)](https://datatracker.ietf.org/doc/html/rfc8955) - Mitigación distribuida de ataques DDoS mediante reglas de filtrado propagadas por BGP.
* [RFC 6811 - BGP Prefix Origin Validation (RPKI)](https://datatracker.ietf.org/doc/html/rfc6811) - Validación criptográfica de anuncios de rutas para evitar secuestros (Hijacking).

### D. Calidad de Servicio (QoS DiffServ)
* [RFC 2474 - Definition of the Differentiated Services Field (DS Field)](https://datatracker.ietf.org/doc/html/rfc2474) - Estructura del byte ToS en 6 bits de DSCP y 2 bits de ECN.
* [RFC 2597 - Assured Forwarding PHB Group](https://datatracker.ietf.org/doc/html/rfc2597) - Especificación de las 4 clases AF y 3 niveles de descarte.
* [RFC 3246 - An Expedited Forwarding PHB (EF)](https://datatracker.ietf.org/doc/html/rfc3246) - Comportamiento de reenvío acelerado con latencia mínima para VoIP.
* [RFC 4594 - Configuration Guidelines for DiffServ Service Classes](https://datatracker.ietf.org/doc/html/rfc4594) - **Guía maestra de la industria** para clasificar y marcar todo el tráfico empresarial.

### E. Data Center Overlays, MPLS y Segment Routing
* [RFC 3031 - Multiprotocol Label Switching Architecture (MPLS)](https://datatracker.ietf.org/doc/html/rfc3031) - Conmutación de paquetes basada en etiquetas.
* [RFC 4364 - BGP/MPLS IP Virtual Private Networks (VPNs)](https://datatracker.ietf.org/doc/html/rfc4364) - Arquitectura de L3VPNs con aislamiento mediante VRF y Route Targets.
* [RFC 7348 - Virtual eXtensible Local Area Network (VXLAN)](https://datatracker.ietf.org/doc/html/rfc7348) - Encapsulamiento de tramas L2 sobre UDP en puerto 4789.
* [RFC 7432 - BGP MPLS-Based Ethernet VPN (EVPN)](https://datatracker.ietf.org/doc/html/rfc7432) - Plano de control moderno para interconexión L2/L3 en datacenters.
* [RFC 8365 - A Network Virtualization Overlay Solution Using BGP EVPN](https://datatracker.ietf.org/doc/html/rfc8365) - Guía para desplegar EVPN con overlays VXLAN y NVGRE.
* [RFC 8402 - Segment Routing Architecture](https://datatracker.ietf.org/doc/html/rfc8402) - Paradigma de enrutamiento basado en origen mediante Segment IDs.
* [RFC 8986 - Segment Routing over IPv6 (SRv6) Network Programming](https://datatracker.ietf.org/doc/html/rfc8986) - Funciones e instrucciones codificadas en direcciones IPv6.

### F. Ciberseguridad, Identidad y VPNs
* [RFC 4301 - Security Architecture for the Internet Protocol (IPsec)](https://datatracker.ietf.org/doc/html/rfc4301) - Marco general de seguridad, bases de datos SPD y SAD.
* [RFC 4303 - IP Encapsulating Security Payload (ESP)](https://datatracker.ietf.org/doc/html/rfc4303) - Cifrado y autenticación de paquetes de red.
* [RFC 7296 - Internet Key Exchange Protocol Version 2 (IKEv2)](https://datatracker.ietf.org/doc/html/rfc7296) - Negociación automática de túneles y claves de sesión.
* [RFC 3948 - UDP Encapsulation of IPsec ESP Packets (NAT-T)](https://datatracker.ietf.org/doc/html/rfc3948) - Transporte de IPsec a través de routers NAT usando el puerto UDP 4500.
* [RFC 8446 - The Transport Layer Security (TLS) Protocol Version 1.3](https://datatracker.ietf.org/doc/html/rfc8446) - Estándar criptográfico para comunicaciones seguras en la web.
* [RFC 2865 - Remote Authentication Dial In User Service (RADIUS)](https://datatracker.ietf.org/doc/html/rfc2865) - Protocolo cliente-servidor para autenticación de usuarios.
* [RFC 8907 - The Terminal Access Controller Access-Control System Plus (TACACS+) Protocol](https://datatracker.ietf.org/doc/html/rfc8907) - Formalización como estándar de TACACS+.
* [RFC 3748 - Extensible Authentication Protocol (EAP)](https://datatracker.ietf.org/doc/html/rfc3748) - Marco de autenticación extensible para 802.1X.

---

## 3. Normas Internacionales Oficiales (IEEE, TIA, ISO, NIST)

| Organismo | Código del Estándar | Título y Alcance Técnico |
| :--- | :--- | :--- |
| **IEEE** | **IEEE 802.1Q** | Virtual Bridged Local Area Networks (VLAN Tagging, CoS 802.1p y QinQ 802.1ad). |
| **IEEE** | **IEEE 802.1X** | Port-Based Network Access Control (Control de Acceso a Puertos con EAP). |
| **IEEE** | **IEEE 802.1w** | Rapid Spanning Tree Protocol (RSTP - Reemplazo de 802.1D). |
| **IEEE** | **IEEE 802.1s** | Multiple Spanning Tree Protocol (MSTP - Instancias de Spanning Tree agrupadas). |
| **IEEE** | **IEEE 802.3ad** | Link Aggregation Control Protocol (LACP - Incorporado en 802.1AX). |
| **IEEE** | **IEEE 802.3bt** | 4-Pair Power over Ethernet (PoE++ Tipo 3 de 60W y Tipo 4 de 90W). |
| **IEEE** | **IEEE 802.11ax** | High Efficiency Wireless (Wi-Fi 6 y Wi-Fi 6E con OFDMA y MU-MIMO en 2.4, 5 y 6 GHz). |
| **IEEE** | **IEEE 802.11be** | Extremely High Throughput (Wi-Fi 7 con canales de 320 MHz, 4096-QAM y MLO). |
| **TIA/EIA** | **ANSI/TIA-568-D** | Commercial Building Telecommunications Cabling Standard (Categorías Cat 5e a Cat 8). |
| **TIA/EIA** | **ANSI/TIA-942-B** | Telecommunications Infrastructure Standard for Data Centers (Tier I a Tier IV). |
| **ISO/IEC** | **ISO/IEC 11801** | Generic Cabling for Customer Premises (Clases de Enlace de Cobre y Fibra OM1-OM5, OS1-OS2). |
| **NIST** | **NIST SP 800-207** | [Zero Trust Architecture](https://csrc.nist.gov/publications/detail/sp/800-207/final) (Marco oficial de referencia de Confianza Cero). |
| **NIST** | **NIST SP 800-53 r5** | [Security and Privacy Controls for Information Systems](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final) (Catálogo de Controles de Seguridad). |
| **ISA/IEC** | **ISA/IEC 62443** | Industrial Communication Networks - Network and System Security (Ciberseguridad OT/SCADA). |
| **ITU-T** | **ITU-T Y.1564** | Ethernet Service Activation Test Methodology (EtherSAM para validación de SLAs). |

---

## 4. Recursos Oficiales de Fabricantes y Enlaces a Diseños Validados

### A. Cisco Systems (Cisco Validated Designs - CVD)
* [Cisco Design Zone for Enterprise Networks](https://www.cisco.com/c/en/us/solutions/enterprise/design-zone-technologies/index.html) - Diseños validados para Campus LAN, SD-Access y Wireless.
* [Cisco SD-WAN Design Guide (CVD)](https://www.cisco.com/c/en/us/td/docs/solutions/CVD/SDWAN/cisco-sdwan-design-guide.html) - Topologías Hub-and-Spoke, Full Mesh y políticas de aplicaciones.
* [Cisco Data Center Spine-and-Leaf Fabric Architecture (NX-OS)](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/7-x/vxlan/configuration/guide/b_Cisco_Nexus_9000_Series_NX-OS_VXLAN_Configuration_Guide_7x.html) - Configuración oficial de VXLAN EVPN en Nexus 9000.

### B. Huawei Enterprise
* [Huawei Enterprise Documentation Portal (Hedex)](https://support.huawei.com/enterprise/en/index.html) - Manuales técnicos para CloudEngine, Routers serie AR y conmutadores Campus.
* [Huawei Campus Network Solution Documentation](https://support.huawei.com/enterprise/en/solutions/campus-network-solution-sol0000000001) - Arquitecturas CloudCampus, iMaster NCE y Wi-Fi 6.

### C. Aruba Networks (HPE)
* [Aruba Validated Solution Guides (VSG)](https://www.arubanetworks.com/solutions/validated-solution-guides/) - Diseños para ArubaOS-CX, conmutadores serie 6000/8000 y segmentación dinámica con ClearPass.

### D. Fortinet & Palo Alto Networks (Ciberseguridad NGFW)
* [Fortinet Document Library (FortiOS Administration Guide)](https://docs.fortinet.com/) - Guías paso a paso de políticas de firewall, VDOMs, SD-WAN e inspección SSL profunda.
* [Palo Alto Networks TechDocs & Reference Architectures](https://docs.paloaltonetworks.com/) - Implementación de App-ID, User-ID, Content-ID, perfiles de seguridad y Zero Trust.

---

## 5. Directorio de Documentos PDF y Whitepapers de Libre Descarga

Para profundizar en la ingeniería aplicada, se recomiendan los siguientes documentos técnicos disponibles gratuitamente en los portales oficiales de la industria:

1. **NIST SP 800-207 - Zero Trust Architecture (PDF Oficial):**  
   🔗 `https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf`  
   *Contenido:* 59 páginas con la definición formal de los principios, modelos de implementación y componentes PDP/PEP.
2. **IETF RFC 9293 - Transmission Control Protocol (TCP):**  
   🔗 `https://www.rfc-editor.org/rfc/pdfrfc/rfc9293.txt.pdf`  
   *Contenido:* El documento formal que rige la máquina de estados de TCP, gestión de ventanas y algoritmos de control de congestión.
3. **Broadband Forum TR-101 - Migration to Ethernet-Based DSL/FTTH Access:**  
   🔗 `https://www.broadband-forum.org/technical/download/TR-101.pdf`  
   *Contenido:* Arquitectura de transporte de última milla para proveedores de telecomunicaciones.
4. **CISA (Cybersecurity & Infrastructure Security Agency) - Cross-Sector Cybersecurity Performance Goals (CPGs):**  
   🔗 `https://www.cisa.gov/sites/default/files/2023-01/CISA_CPG_Report_508c.pdf`  
   *Contenido:* Controles mínimos de ciberseguridad recomendados para infraestructuras críticas y redes OT/IT.
