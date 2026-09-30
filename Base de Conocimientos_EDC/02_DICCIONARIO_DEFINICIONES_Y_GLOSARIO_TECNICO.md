# 📖 Diccionario Enciclopédico de Redes y Ciberseguridad EDC
## Network Engineering & Cybersecurity Master Compendium

> **DICCIONARIO TÉCNICO DE LA A A LA Z (+160 TÉRMINOS, ESTÁNDARES Y PROTOCOLOS)**  
> **Ubicación:** `Base de Conocimientos_EDC/02_DICCIONARIO_DEFINICIONES_Y_GLOSARIO_TECNICO.md`  
> **Criterio Editorial:** Rigor técnico formal, capa OSI/dominio, estándar rector y aplicación operativa real.

---

## 🔤 Índice Alfabético Rápido
[A](#a) • [B](#b) • [C](#c) • [D](#d) • [E](#e) • [F](#f) • [G](#g) • [H](#h) • [I](#i) • [J](#j) • [K](#k) • [L](#l) • [M](#m) • [N](#n) • [O](#o) • [P](#p) • [Q](#q) • [R](#r) • [S](#s) • [T](#t) • [U](#u) • [V](#v) • [W](#w) • [X](#x) • [Y](#y) • [Z](#z)

---

### A

#### **AAA (Authentication, Authorization, and Accounting)**
- **Dominio / Capa:** Ciberseguridad / Capa 7 (Aplicación).
- **Estándares:** RFC 2865 (RADIUS), RFC 8907 (TACACS+).
- **Definición:** Marco arquitectónico de seguridad que gestiona tres fases críticas de control de acceso:
  1. *Autenticación:* Validación de la identidad del sujeto mediante credenciales o certificados digitales.
  2. *Autorización:* Determinación de qué recursos o comandos específicos tiene permitido ejecutar.
  3. *Auditoría (Accounting):* Registro exhaustivo y con marca temporal de qué acciones realizó el usuario en el sistema.

#### **ACL (Access Control List)**
- **Dominio / Capa:** Seguridad y Switching / Capas 2, 3 y 4.
- **Definición:** Lista secuencial y jerárquica de sentencias condicionales (`permit` o `deny`) evaluadas secuencialmente con una regla de denegación implícita al final (`deny any`). Se clasifican en Estándar (solo IP origen), Extendidas (IP origen/destino, protocolo y puertos L4) y de Capa 2 (direcciones MAC).

#### **AES (Advanced Encryption Standard)**
- **Dominio / Capa:** Criptografía / Capas 2 a 7.
- **Estándares:** FIPS PUB 197, NIST SP 800-38D (AES-GCM).
- **Definición:** Algoritmo de cifrado simétrico por bloques (tamaño fijo de 128 bits) con longitudes de clave de 128, 192 o 256 bits. El modo AES-GCM (Galois/Counter Mode) proporciona cifrado autenticado con datos asociados (AEAD), garantizando confidencialidad e integridad sin sobrecarga de hash separado.

#### **AF (Assured Forwarding - DiffServ)**
- **Dominio / Capa:** Calidad de Servicio (QoS) / Capa 3.
- **Estándar:** RFC 2597.
- **Definición:** Esquema de marcación QoS en el campo DSCP que define 4 clases de tráfico (AF1 a AF4) y 3 niveles de probabilidad de descarte por congestión (Drop Precedence: Low, Medium, High). Por ejemplo, AF41 indica tráfico de alta prioridad con mínima probabilidad de descarte.

#### **AMF (Access and Mobility Management Function)**
- **Dominio / Capa:** Telecomunicaciones Carrier / 5G Core (3GPP).
- **Estándar:** 3GPP TS 23.501.
- **Definición:** Función del plano de control en el núcleo 5G Standalone (5G SA) responsable de la terminación de la señalización NAS (Non-Access Stratum), gestión del registro de usuarios, control de movilidad y autenticación de dispositivos (UE).

#### **Anycast (BGP Anycast Routing)**
- **Dominio / Capa:** Enrutamiento y Servicios / Capa 3.
- **Estándar:** RFC 4786.
- **Definición:** Técnica de direccionamiento y enrutamiento en la que múltiples servidores físicos o centros de datos distribuidos geográficamente comparten la misma dirección IP pública unicast. BGP enruta las solicitudes del cliente hacia el nodo topológicamente más cercano según las métricas de AS-Path y retardo.

#### **AOC (Active Optical Cable)**
- **Dominio / Capa:** Infraestructura Física / Capa 1.
- **Definición:** Cable ensamblado de fábrica compuesto por transceptores ópticos fijados permanentemente en ambos extremos de una fibra óptica multimodo. A diferencia de los cables de cobre DAC, elimina las interferencias electromagnéticas y permite distancias de hasta 100 metros en centros de datos.

#### **ARP (Address Resolution Protocol)**
- **Dominio / Capa:** Conectividad LAN / Capa 2 a 3.
- **Estándar:** RFC 826.
- **Definición:** Protocolo fundamental que resuelve una dirección lógica conocida de Capa 3 (IPv4) a una dirección física de Capa 2 (MAC) dentro del mismo dominio de difusión local mediante solicitudes en broadcast (`who-has`) y respuestas en unicast.

#### **AS (Autonomous System - Sistema Autónomo)**
- **Dominio / Capa:** Enrutamiento WAN e Internet / Capa 3.
- **Estándar:** RFC 1930, RFC 4271.
- **Definición:** Colección conectada de prefijos IP bajo el control administrativo de una sola entidad u organización que presenta una política de enrutamiento común hacia Internet mediante BGP. Se identifica mediante un ASN (Autonomous System Number) de 16 o 32 bits (RFC 4893).

---

### B

#### **BFD (Bidirectional Forwarding Detection)**
- **Dominio / Capa:** Enrutamiento y Conmutación / Capa 3.
- **Estándares:** RFC 5880, RFC 5881.
- **Definición:** Protocolo de detección rápida de fallas de enlace en submilisegundos entre routers adyacentes. Al ser independiente del medio y del protocolo de enrutamiento, BFD interactúa con OSPF, BGP o IS-IS para forzar la convergencia instantánea sin esperar a que expiren los temporizadores muertos de dichos protocolos.

#### **BGP-4 (Border Gateway Protocol Version 4)**
- **Dominio / Capa:** Enrutamiento Global / Capa 3 (usa TCP 179).
- **Estándar:** RFC 4271.
- **Definición:** El protocolo de vector de rutas (Path-Vector) estándar que interconecta Internet y redes wan corporativas. BGP intercambia prefijos acompañados de atributos de ruta (AS-Path, Next-Hop, Local Preference, Multi-Exit Discriminator - MED) para prevenir bucles de enrutamiento y aplicar políticas de tráfico complejas.

#### **BGP EVPN (Ethernet VPN)**
- **Dominio / Capa:** Data Center Fabric / Capas 2 y 3.
- **Estándares:** RFC 7432, RFC 8365.
- **Definición:** Plano de control unificado basado en extensiones multiprotocolo de BGP (MP-BGP) diseñado para descubrir y distribuir información de accesibilidad de direcciones MAC (Capa 2) e IP (Capa 3) a través de redes overlay como VXLAN. Introduce tipos de rutas estandarizados (Route Types 1 a 5).

#### **BNG (Broadband Network Gateway)**
- **Dominio / Capa:** Telecomunicaciones Carrier / ISP Edge.
- **Estándar:** Broadband Forum TR-101 / TR-384.
- **Definición:** Enrutador de borde de proveedor de acceso a Internet encargado de autenticar suscriptores residenciales y comerciales (vía PPPoE o IPoE), aplicar políticas de ancho de banda (QoS/Policing) y enrutar el tráfico hacia el núcleo IP del ISP.

#### **BPDU (Bridge Protocol Data Unit)**
- **Dominio / Capa:** Switching / Capa 2.
- **Estándares:** IEEE 802.1D, IEEE 802.1w.
- **Definición:** Trama especial de control transmitida periódicamente (por defecto cada 2 segundos) por los conmutadores Ethernet para elegir el Switch Raíz (Root Bridge), calcular la topología libre de bucles y detectar cambios de estado en enlaces físicos.

---

### C

#### **CAM Table (Content Addressable Memory)**
- **Dominio / Capa:** Hardware de Conmutación / Capa 2.
- **Definición:** Memoria de alta velocidad en switches que realiza búsquedas en un solo ciclo de reloj. Asocia las direcciones MAC de origen aprendidas con el número de puerto físico y la VLAN correspondiente. Si se desborda mediante un ataque de MAC Flooding, el switch se degrada comportándose como un hub de difusión.

#### **CAPWAP (Control and Provisioning of Wireless Access Points)**
- **Dominio / Capa:** Redes Inalámbricas / Capa 4 a 7 (UDP 5246/5247).
- **Estándar:** RFC 5415, RFC 5416.
- **Definición:** Protocolo estándar de interoperabilidad que permite a un Controlador de LAN Inalámbrica (WLC) gestionar de forma centralizada y segura múltiples Access Points ligeros (Lightweight APs), dividiendo el plano de control (cifrado con DTLS) del plano de datos.

#### **CBWFQ (Class-Based Weighted Fair Queuing)**
- **Dominio / Capa:** Calidad de Servicio (QoS) / Capa 3.
- **Definición:** Mecanismo de encolamiento que extiende WFQ para ofrecer soporte de clases de tráfico definidas por el usuario. Permite garantizar una cantidad mínima exacta de ancho de banda a cada clase durante períodos de congestión sin penalizar el tráfico interactivo.

#### **CIDR (Classless Inter-Domain Routing)**
- **Dominio / Capa:** Direccionamiento IP / Capa 3.
- **Estándar:** RFC 1519, RFC 4632.
- **Definición:** Metodología que eliminó la división rígida de direcciones IP por clases (Clase A, B, C), introduciendo la notación de prefijo de longitud variable (`/24`, `/28`, etc.) y permitiendo la agregación y sumarización de rutas en las tablas globales de Internet.

#### **CIP (Common Industrial Protocol)**
- **Dominio / Capa:** Redes Industriales OT / Capa 7.
- **Estándar:** ODVA Spec (IEC 61158).
- **Definición:** Protocolo industrial de nivel de aplicación orientado a objetos que unifica los servicios de automatización, control de movimiento y seguridad para redes industriales sobre Ethernet/IP, ControlNet y DeviceNet.

#### **Clos Network (Arquitectura Spine-and-Leaf)**
- **Dominio / Capa:** Data Center Fabric / Capas 2 y 3.
- **Definición:** Topología de interconexión conmutada no bloqueante de múltiples etapas formulada originalmente por Charles Clos en 1953. En centros de datos modernos, cada conmutador Leaf se conecta a todos los Spines, garantizando latencia predecible y ancho de banda constante de Este a Oeste mediante ECMP.

#### **CoA (Change of Authorization - RADIUS)**
- **Dominio / Capa:** Control de Acceso AAA / Capa 7.
- **Estándar:** RFC 5176.
- **Definición:** Extensión del protocolo RADIUS que permite a un servidor de políticas (como Cisco ISE o Aruba ClearPass) enviar una solicitud dinámica al switch o WLC para modificar los atributos de una sesión activa (ej. cambiar una VLAN, aplicar una dACL o desconectar un cliente infractor) sin necesidad de reiniciar la sesión del usuario.

#### **CoS (Class of Service)**
- **Dominio / Capa:** Conmutación L2 / Capa 2.
- **Estándar:** IEEE 802.1p (subcampo de IEEE 802.1Q).
- **Definición:** Campo de 3 bits presente en la etiqueta 802.1Q de las tramas Ethernet troncales que permite definir 8 niveles de prioridad de servicio (de 0 a 7) para diferenciar tráfico de voz, video y datos en la capa de enlace.

---

### D

#### **DAC (Direct Attach Copper)**
- **Dominio / Capa:** Conectividad Física / Capa 1.
- **Definición:** Cable de cobre de par coaxial apantallado terminado con conectores de transceptor fijos (SFP+, SFP28, QSFP28) en ambos extremos. Ofrece latencia ultra baja (< 0.1 µs) y consumo eléctrico despreciable, siendo el estándar de interconexión Top-of-Rack (ToR) entre servidores y conmutadores para distancias de hasta 5 metros.

#### **DAI (Dynamic ARP Inspection)**
- **Dominio / Capa:** Seguridad L2 / Capa 2.
- **Definición:** Mecanismo de seguridad en conmutadores que intercepta todas las solicitudes y respuestas ARP en puertos no confiables y las valida contra la tabla de enlaces seguros de DHCP Snooping (o ACLs estáticas de ARP). Descarta de inmediato los paquetes ARP maliciosos, neutralizando ataques de Man-in-the-Middle y envenenamiento de caché ARP.

#### **DDI (DNS, DHCP, and IPAM)**
- **Dominio / Capa:** Servicios de Red / Capas 3 y 7.
- **Definición:** Acrónimo que designa la tríada de servicios centrales de infraestructura IP: Resolución de nombres (DNS), configuración dinámica de direccionamiento (DHCP) y gestión de inventario y espacio de direcciones (IPAM), conformando la Fuente Única de Verdad (SSoT).

#### **DHCP Snooping**
- **Dominio / Capa:** Seguridad L2 / Capa 2.
- **Definición:** Característica de conmutación que clasifica los puertos físicos en *confiables* (conectados a servidores DHCP legítimos o uplinks) y *no confiables* (puertos de usuario final). Bloquea mensajes `DHCP Offer` y `DHCP Ack` en puertos no confiables y construye una tabla de asociaciones IP-MAC-VLAN-Puerto utilizada por DAI e IP Source Guard.

#### **DiffServ (Differentiated Services Architecture)**
- **Dominio / Capa:** Calidad de Servicio (QoS) / Capa 3.
- **Estándar:** RFC 2474, RFC 2475, RFC 4594.
- **Definición:** Modelo escalable de QoS que clasifica y marca paquetes en el borde de la red asignándoles valores DSCP en la cabecera IP. Los nodos intermedios procesan el tráfico basándose exclusivamente en el comportamiento de salto por salto (PHB - Per-Hop Behavior) sin mantener el estado individual de cada flujo.

#### **DMVPN (Dynamic Multipoint VPN)**
- **Dominio / Capa:** Redes WAN y VPN / Capas 3 y 4.
- **Definición:** Arquitectura propietaria de Cisco (reproducible con estándares abiertos) que combina túneles mGRE (Multipoint GRE), resolución NHRP (Next Hop Resolution Protocol) y cifrado IPsec dinámico. Permite establecer túneles VPN directos entre sucursales (Spoke-to-Spoke) bajo demanda sin sobrecargar el enrutador central (Hub).

#### **DNP3 (Distributed Network Protocol 3)**
- **Dominio / Capa:** Redes Industriales OT / Capa 7 (TCP/UDP 20000).
- **Estándar:** IEEE 1815.
- **Definición:** Protocolo de telecomunicaciones para sistemas SCADA ampliamente utilizado en el sector eléctrico, hídrico y de petróleo/gas. Proporciona sellado de tiempo de eventos y confirmación de mensajes, pero carece de cifrado y autenticación nativa en su versión clásica (requiere Secure DNP3).

#### **DSCP (Differentiated Services Code Point)**
- **Dominio / Capa:** QoS / Capa 3.
- **Estándar:** RFC 2474.
- **Definición:** Campo de 6 bits ubicado en el byte de Tipo de Servicio (ToS) de la cabecera IPv4 (o Traffic Class en IPv6). Proporciona hasta 64 clases de servicio posibles, incluyendo CS (Class Selector), AF (Assured Forwarding) y EF (Expedited Forwarding).

#### **DWDM (Dense Wavelength Division Multiplexing)**
- **Dominio / Capa:** Óptica y Telecomunicaciones Carrier / Capa 1.
- **Estándar:** ITU-T G.694.1.
- **Definición:** Tecnología de transporte óptico que multiplexa múltiples señales portadoras ópticas independientes en una sola fibra monomodo utilizando diferentes longitudes de onda en la banda C (1530-1565 nm) con un espaciado estrecho (50 GHz o 100 GHz), alcanzando capacidades superiores a los 32 Terabits por segundo por hilo de fibra.

---

### E

#### **EAP (Extensible Authentication Protocol)**
- **Dominio / Capa:** Control de Acceso / Capa 2.
- **Estándar:** RFC 3748.
- **Definición:** Marco universal de autenticación utilizado en redes 802.1X y enlaces PPP. No especifica un mecanismo de autenticación concreto, sino que define el formato de mensajes que transporta métodos especializados como EAP-TLS (basado en certificados), PEAP (cifrado por túnel TLS) y EAP-FAST.

#### **ECMP (Equal-Cost Multi-Path)**
- **Dominio / Capa:** Enrutamiento / Capa 3.
- **Definición:** Estrategia de reenvío donde los enrutadores balancean el tráfico a través de múltiples rutas de igual costo hacia un mismo destino utilizando una función hash basada en la 5-tupla del paquete (IP origen, IP destino, Protocolo, Puerto origen, Puerto destino) para preservar el orden de las tramas.

#### **EF (Expedited Forwarding - DiffServ)**
- **Dominio / Capa:** QoS / Capa 3.
- **Estándar:** RFC 3246.
- **Definición:** Clase de servicio de máxima prioridad en DiffServ (valor DSCP 46 o binario `101110`). Destinada al tráfico de voz sobre IP (VoIP), garantiza un servicio con mínima latencia, mínimo jitter y tasa de pérdida garantizada mediante colas de prioridad estricta (LLQ - Low Latency Queuing).

#### **EIGRP (Enhanced Interior Gateway Routing Protocol)**
- **Dominio / Capa:** Enrutamiento Interior / Capa 3 (Protocolo IP 88).
- **Estándar:** RFC 7868.
- **Definición:** Protocolo avanzado de vector de distancias desarrollado originalmente por Cisco que implementa el algoritmo DUAL (Diffusing Update Algorithm) para garantizar una convergencia ultrarrápida y libre de bucles calculando un Sucesor Factible (Feasible Successor) como respaldo inmediato.

#### **err-disabled (Estado de Puerto)**
- **Dominio / Capa:** Operación de Conmutación / Capas 1 y 2.
- **Definición:** Estado operativo en switches Cisco y compatibles en el cual el sistema operativo apaga administrativamente un puerto físico al detectar una condición anormal grave, tal como violación de Port Security, colisión dúplex, recepción no autorizada de BPDUs (BPDU Guard) o tormentas de broadcast.

#### **ESP (Encapsulating Security Payload - IPsec)**
- **Dominio / Capa:** Seguridad en Redes / Capa 3 (Protocolo IP 50).
- **Estándar:** RFC 4303.
- **Definición:** Protocolo fundamental del suite IPsec que proporciona confidencialidad de datos (mediante cifrado simétrico), autenticación del origen de datos, verificación de integridad y protección contra ataques de repetición (Anti-Replay).

---

### F

#### **FHRP (First Hop Redundancy Protocol)**
- **Dominio / Capa:** Resiliencia de Red / Capa 3.
- **Definición:** Familia de protocolos que permite a un grupo de enrutadores o conmutadores de capa 3 compartir una dirección IP y MAC virtual común para actuar como puerta de enlace predeterminada redundante y transparente para los hosts finales. Incluye HSRP (Cisco), VRRP (estándar RFC 5798) y GLBP (balanceo de carga).

#### **FlowSpec (BGP Flow Specification)**
- **Dominio / Capa:** Seguridad Carrier / Capas 3 y 4.
- **Estándar:** RFC 5575, RFC 8955.
- **Definición:** Extensión de BGP que permite distribuir dinámicamente reglas de filtrado y mitigación de tráfico granular (basadas en tuplas L3/L4) a todos los routers del sistema autónomo, facilitando la neutralización y desvío de ataques masivos de Denegación de Servicio Distribuida (DDoS) en el borde carrier.

#### **FTTH (Fiber to the Home)**
- **Dominio / Capa:** Redes de Acceso / Capa 1 y 2.
- **Estándares:** ITU-T G.984 (GPON), ITU-T G.9807.1 (XGS-PON).
- **Definición:** Arquitectura de telecomunicaciones de última milla basada en redes ópticas pasivas (PON) donde la fibra óptica llega directamente hasta el interior de la vivienda o empresa del suscriptor, conectando una OLT central con la ONT del cliente mediante splitters ópticos pasivos sin alimentación eléctrica intermedia.

---

### G

#### **G.711 / G.729 (Códecs de Telefonía VoIP)**
- **Dominio / Capa:** Voz sobre IP / Capa 6 y 7.
- **Estándares:** ITU-T Recommendations.
- **Definición:** 
  - *G.711:* Códec estándar de modulación por impulsos codificados (PCM) sin compresión. Utiliza 64 kbps de ancho de banda bruto (µ-law en América/Japón y A-law en Europa) ofreciendo máxima fidelidad acústica (MOS ~4.4).
  - *G.729:* Códec de compresión CS-ACELP que reduce el consumo a sólo 8 kbps de payload sacrificando ligeramente la fidelidad acústica (MOS ~3.9), ideal para enlaces WAN restringidos.

#### **GPON (Gigabit Passive Optical Network)**
- **Dominio / Capa:** Telecomunicaciones Carrier / Capas 1 y 2.
- **Estándar:** ITU-T G.984.
- **Definición:** Tecnología de acceso de banda ancha punto a multipunto sobre fibra monomodo que ofrece tasas nominales de 2.488 Gbps descendentes (1490 nm) y 1.244 Gbps ascendentes (1310 nm), divididas entre hasta 64 o 128 usuarios mediante splitters ópticos pasivos.

#### **gRPC / Streaming Telemetry**
- **Dominio / Capa:** NetDevOps y Telemetría / Capas 5 a 7 (HTTP/2).
- **Definición:** Marco RPC de código abierto desarrollado por Google que reemplaza el sondeo periódico tradicional de SNMP por un modelo basado en suscripciones donde el router transmite continuamente métricas de estado de hardware e interfaces a un colector central en tiempo real, codificado con Protocol Buffers.

---

### H

#### **HLD (High-Level Design)**
- **Dominio / Capa:** Metodología de Ingeniería IT.
- **Definición:** Documento arquitectónico formal que describe la visión global de la infraestructura tecnológica, los requerimientos de negocio, el diagrama de bloques lógicos, los criterios de alta disponibilidad, la matriz de riesgos y la interoperabilidad de componentes antes de la fase de diseño detallado.

#### **HSRP (Hot Standby Router Protocol)**
- **Dominio / Capa:** Redundancia L3 / Capa 3 (UDP 1985 / 224.0.0.2).
- **Estándar:** RFC 2281 (Cisco Propietario).
- **Definición:** Protocolo FHRP pionero desarrollado por Cisco que permite a dos o más routers compartir una IP virtual y una MAC virtual compartida (`0000.0c07.acXX`). El router con mayor prioridad asume el rol Activo (Active), mientras que los demás permanecen en espera (Standby).

#### **HSTS (HTTP Strict Transport Security)**
- **Dominio / Capa:** Ciberseguridad Web / Capa 7.
- **Estándar:** RFC 6797.
- **Definición:** Cabecera de respuesta del servidor web (`Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`) que instruye al navegador web a comunicarse exclusivamente mediante HTTPS cifrado, bloqueando ataques de intermediario como SSL Stripping.

---

### I

#### **IEEE 802.1Q**
- **Dominio / Capa:** Conmutación LAN / Capa 2.
- **Definición:** Estándar de la industria para el etiquetado de tramas Ethernet en enlaces troncales. Inserta una etiqueta adicional de 4 bytes (VLAN Tag) entre la dirección MAC de origen y el campo EtherType original. Contiene el identificador de VLAN (VID de 12 bits, soportando de 1 a 4094 VLANs) y el campo de prioridad CoS de 3 bits.

#### **IEEE 802.1X**
- **Dominio / Capa:** Seguridad de Acceso / Capas 2 y 7.
- **Definición:** Estándar internacional para el control de acceso a puertos físicos y redes inalámbricas basado en identidades. Estructura el ecosistema en tres componentes fundamentales:
  1. *Suplicante (Supplicant):* Software del cliente que solicita conectividad.
  2. *Autenticador (Authenticator):* Switch o WLC que bloquea el tráfico no autorizado.
  3. *Servidor de Autenticación:* RADIUS (Cisco ISE / FreeRADIUS) que evalúa las credenciales del cliente.

#### **IKEv2 (Internet Key Exchange Version 2)**
- **Dominio / Capa:** VPNs y Criptografía / Capas 4 y 7 (UDP 500 / UDP 4500).
- **Estándar:** RFC 7296.
- **Definición:** Protocolo criptográfico sucesor de IKEv1 utilizado para autenticar a los extremos de un túnel VPN IPsec y negociar dinámicamente las asociaciones de seguridad (Security Associations - SAs). Soporta nativamente NAT Traversal (NAT-T), movilidad de clientes (MOBIKE RFC 4555) y autenticación asimétrica EAP.

#### **IPAM (IP Address Management)**
- **Dominio / Capa:** Gestión y NetDevOps / Capa 3.
- **Definición:** Disciplina y conjunto de herramientas automatizadas para planificar, registrar, asignar y auditar el espacio de direcciones IP públicas y privadas (IPv4 e IPv6), subredes, dominios DNS y asociaciones VLAN en una corporación.

#### **ISA/IEC 62443**
- **Dominio / Capa:** Ciberseguridad Industrial OT / Transversal.
- **Definición:** Serie integral de normas internacionales de ciberseguridad para Sistemas de Automatización y Control Industrial (IACS). Introduce conceptos esenciales como la segmentación por *Zonas y Conductos (Zones and Conduits)* y clasifica los requisitos técnicos en cuatro Niveles de Seguridad (Security Levels: SL 1 a SL 4).

---

### J

#### **Jitter (Variación de Retardo de Paquete)**
- **Dominio / Capa:** Calidad de Servicio (QoS) y VoIP / Capa 4.
- **Estándar:** RFC 3393, RFC 3550.
- **Definición:** Variación estadística en el tiempo de llegada entre paquetes consecutivos pertenecientes a un mismo flujo de datos. Para que una llamada de telefonía IP mantenga una calidad aceptable, el jitter unidireccional debe mantenerse estrictamente por debajo de los 30 milisegundos.

#### **Jumbo Frames**
- **Dominio / Capa:** Conmutación y Data Center / Capa 2.
- **Definición:** Tramas Ethernet cuyo tamaño de unidad de transmisión máxima (MTU) supera el estándar histórico de 1500 bytes, típicamente configuradas a 9000 o 9216 bytes. Reducen drásticamente el consumo de CPU en servidores y switches al procesar menos cabeceras por gigabyte transferido en redes de almacenamiento SAN (iSCSI, NFS) y overlays VXLAN.

---

### L

#### **LACP (Link Aggregation Control Protocol)**
- **Dominio / Capa:** Conmutación LAN / Capa 2.
- **Estándares:** IEEE 802.3ad / IEEE 802.1AX.
- **Definición:** Protocolo dinámico y abierto que permite negociar la agregación de múltiples interfaces Ethernet físicas en un solo canal lógico de alta disponibilidad y mayor ancho de banda (LAG / Port-Channel / Eth-Trunk), detectando automáticamente desajustes de configuración y cortes de cable.

#### **LDP (Label Distribution Protocol)**
- **Dominio / Capa:** Redes Carrier MPLS / Capas 3 y 4 (TCP/UDP 646).
- **Estándar:** RFC 5036.
- **Definición:** Protocolo de la arquitectura MPLS mediante el cual los enrutadores de conmutación de etiquetas (LSR) intercambian recíprocamente asignaciones de etiquetas basadas en la información aprendida de la tabla de enrutamiento IGP, estableciendo rutas conmutadas por etiquetas (LSPs).

#### **LLD (Low-Level Design)**
- **Dominio / Capa:** Metodología de Ingeniería IT.
- **Definición:** Documento de ingeniería de detalle minucioso que contiene el plan de direccionamiento IP completo, tablas de cableado y conexionado puerto por puerto, configuraciones CLI exactas de cada equipo, parámetros de temporizadores y planes de prueba de aceptación.

#### **LLQ (Low Latency Queuing)**
- **Dominio / Capa:** QoS / Capa 3.
- **Definición:** Algoritmo de programación de colas que añade una cola de prioridad estricta preferente (Priority Queue - PQ) a la arquitectura CBWFQ. Todo paquete asignado a la cola LLQ (típicamente voz VoIP) se transmite antes que cualquier otro paquete, con un mecanismo de limitación (Policer) que evita que sature por completo el enlace.

#### **LSA (Link State Advertisement)**
- **Dominio / Capa:** Enrutamiento OSPF / Capa 3.
- **Estándar:** RFC 2328.
- **Definición:** Paquete de datos de estado de enlace que los routers OSPF generan y transmiten para describir el estado de sus interfaces directas, costos y vecinos adyacentes. La colección consolidada de todos los LSAs en un área conforma la Base de Datos de Estado de Enlace (LSDB).

---

### M

#### **MAB (MAC Authentication Bypass)**
- **Dominio / Capa:** Seguridad de Acceso / Capa 2.
- **Definición:** Mecanismo de respaldo (Fallback) en redes 802.1X que permite autenticar dispositivos heredados que no disponen de software suplicante 802.1X (impresoras de red, cámaras IP, sistemas de control de acceso) utilizando su dirección física MAC como nombre de usuario y contraseña ante el servidor RADIUS.

#### **MITRE ATT&CK (Adversarial Tactics, Techniques, and Common Knowledge)**
- **Dominio / Capa:** Ciberseguridad / Transversal.
- **Definición:** Base de conocimiento de libre acceso y matriz estructurada que documenta las tácticas, técnicas y procedimientos (TTPs) observados en el comportamiento real de ciberatacantes globales a lo largo de las distintas etapas de intrusión (Acceso Inicial, Movimiento Lateral, Exfiltración).

#### **MLO (Multi-Link Operation)**
- **Dominio / Capa:** Redes Inalámbricas Wi-Fi 7 / Capas 1 y 2.
- **Estándar:** IEEE 802.11be.
- **Definición:** Característica revolucionaria de Wi-Fi 7 que permite a un cliente inalámbrico transmitir y recibir paquetes de datos simultáneamente a través de múltiples bandas de frecuencia (2.4 GHz, 5 GHz y 6 GHz) y canales distintos, reduciendo la latencia al mínimo extremo y multiplicando la tasa de transferencia.

#### **MOP (Method of Procedure)**
- **Dominio / Capa:** Metodología y Operaciones IT.
- **Definición:** Documento operativo detallado y cronometrado paso a paso diseñado para ejecutar cambios críticos en producción durante una ventana de mantenimiento. Contiene las verificaciones previas (Pre-Checks), comandos CLI exactos, verificaciones posteriores (Post-Checks) y un plan de contingencia de reversión inmediata (Rollback Plan).

#### **MPLS (Multi-Protocol Label Switching)**
- **Dominio / Capa:** Transporte Carrier y WAN / Capa 2.5.
- **Estándares:** RFC 3031, RFC 4364 (BGP/MPLS IP VPNs).
- **Definición:** Tecnología de conmutación de alto rendimiento en operadores de telecomunicaciones que sustituye la inspección de la cabecera IP en cada enrutador intermedio por la lectura de etiquetas fijas de 20 bits (MPLS Shim Header), permitiendo crear Redes Privadas Virtuales de Capa 3 (L3VPN) totalmente aisladas.

---

### N

#### **NetBox**
- **Dominio / Capa:** NetDevOps y Gestión IT / Capa 7.
- **Definición:** Aplicación web de código abierto diseñada específicamente para actuar como la Fuente Única de Verdad (Single Source of Truth - SSoT) para la gestión de infraestructura de red, abarcando IPAM, racks de centros de datos, conmutadores, cableado físico y circuitos WAN.

#### **NETCONF / RESTCONF**
- **Dominio / Capa:** Automatización de Redes / Capa 7.
- **Estándares:** RFC 6241 (NETCONF sobre SSH), RFC 8040 (RESTCONF sobre HTTPS).
- **Definición:** Protocolos estándar de gestión programática de dispositivos de red que manipulan datos de configuración y estado modelados formalmente en lenguaje YANG, sustituyendo el raspado de texto plano CLI (Screen Scraping) por llamadas estructuradas en XML o JSON.

#### **NGFW (Next-Generation Firewall)**
- **Dominio / Capa:** Seguridad Perimetral / Capas 2 a 7.
- **Definición:** Dispositivo de seguridad avanzada que supera las capacidades de los cortafuegos de estado tradicionales (L3/L4) al integrar inspección profunda de paquetes a nivel de aplicación (Capa 7 independiente de puertos), prevención de intrusiones en flujo (IPS), descifrado e inspección TLS/SSL, filtrado web por reputación e integración con identidades de usuario (User-ID).

#### **NIST SP 800-207**
- **Dominio / Capa:** Ciberseguridad y Gobernanza.
- **Definición:** Publicación especial del Instituto Nacional de Estándares y Tecnología de EE.UU. que establece la arquitectura formal de referencia para el modelo de seguridad **Zero Trust (Confianza Cero)**, definiendo los componentes del Motor de Políticas (PE), Administrador de Políticas (PA) y Punto de Cumplimiento de Políticas (PEP).

---

### O

#### **OFDMA (Orthogonal Frequency-Division Multiple Access)**
- **Dominio / Capa:** Redes Inalámbricas / Capas 1 y 2.
- **Estándares:** IEEE 802.11ax (Wi-Fi 6), 3GPP LTE/5G.
- **Definición:** Esquema de modulación digital que divide un canal de radiofrecuencia en subportadoras individuales agrupadas en Unidades de Recurso (RUs). Permite que un Punto de Acceso transmita o reciba datos de múltiples clientes simultáneamente en un solo ciclo de transmisión, reduciendo la contención de radio en entornos de alta densidad.

#### **OSPF (Open Shortest Path First)**
- **Dominio / Capa:** Enrutamiento Interior / Capa 3 (Protocolo IP 89).
- **Estándares:** RFC 2328 (OSPFv2 para IPv4), RFC 5340 (OSPFv3 para IPv6).
- **Definición:** Protocolo de enrutamiento interior de estado de enlace no propietario ampliamente adoptado en redes corporativas y centros de datos. Utiliza el algoritmo de Dijkstra (SPF) para calcular el árbol de rutas de menor costo libre de bucles, organizando la red en áreas jerárquicas con el Área 0 como backbone central.

#### **OT (Operational Technology - Tecnologías de Operación)**
- **Dominio / Capa:** Redes Industriales e Infraestructura Crítica.
- **Definición:** Conjunto de hardware y software de comunicaciones dedicado a monitorizar y controlar directamente dispositivos físicos, actuadores, válvulas, generadores eléctricos y procesos industriales continuos (SCADA, DCS, PLCs), priorizando la disponibilidad y la seguridad de la vida humana sobre la confidencialidad de datos.

---

### P

#### **PFS (Perfect Forward Secrecy)**
- **Dominio / Capa:** Criptografía y VPNs / Capas 4 y 7.
- **Definición:** Propiedad matemática de los protocolos de intercambio de claves (como Diffie-Hellman) que garantiza que el compromiso de una clave privada a largo plazo no comprometerá la confidencialidad de sesiones pasadas ni de claves de sesión previamente negociadas.

#### **Purdue Model (PERA - Purdue Enterprise Reference Architecture)**
- **Dominio / Capa:** Arquitectura de Redes Industriales OT / ISA-95.
- **Definición:** Modelo jerárquico clásico de segmentación que divide las redes de fabricación e industriales en niveles funcionales estrictos:
  - *Nivel 0:* Proceso físico (sensores, bombas, actuadores).
  - *Nivel 1:* Control básico (PLCs, RTUs).
  - *Nivel 2:* Control de área y supervisión (HMIs locales, consolas de operador).
  - *Nivel 3:* Operaciones de manufactura y gestión de planta (Servidores SCADA, Historian).
  - *Nivel 3.5 (IDMZ):* Zona Desmilitarizada Industrial que aísla físicamente OT de IT.
  - *Nivel 4 / 5:* Red corporativa empresarial y servicios de nube (ERP, correo, internet).

---

### Q

#### **QinQ (IEEE 802.1ad - VLAN Stacking)**
- **Dominio / Capa:** Carrier Ethernet / Capa 2.
- **Estándar:** IEEE 802.1ad.
- **Definición:** Tecnología de conmutación de capa 2 que añade una segunda etiqueta VLAN 802.1Q externa (Service VLAN o S-VLAN) sobre la etiqueta original del cliente (Customer VLAN o C-VLAN). Permite a los proveedores de telecomunicaciones transportar el tráfico de múltiples clientes a través de su red MAN preservando intacta la segmentación interna del cliente.

#### **QUIC (Quick UDP Internet Connections)**
- **Dominio / Capa:** Transporte y Web / Capas 4 a 7 (UDP 443).
- **Estándar:** RFC 9000.
- **Definición:** Protocolo de capa de transporte moderno y multiplexado sobre UDP que conforma el núcleo del estándar **HTTP/3**. Integra cifrado TLS 1.3 de forma nativa, elimina el bloqueo de cabeza de línea (Head-of-Line Blocking) inherente a TCP y reduce la latencia de establecimiento de conexión a 0-RTT.

---

### R

#### **RADIUS (Remote Authentication Dial-In User Service)**
- **Dominio / Capa:** Seguridad AAA / Capa 7 (UDP 1812/1813).
- **Estándar:** RFC 2865, RFC 2866.
- **Definición:** Protocolo de cliente-servidor para autenticación y contabilidad centralizada de usuarios. Combina las fases de autenticación y autorización en una sola transacción, y cifra únicamente el campo de la contraseña del usuario en el paquete de solicitud (a diferencia de TACACS+, que cifra todo el cuerpo del paquete).

#### **RPKI (Resource Public Key Infrastructure)**
- **Dominio / Capa:** Seguridad en Enrutamiento Carrier / Capa 3.
- **Estándares:** RFC 6480, RFC 6811.
- **Definición:** Marco de seguridad basado en criptografía de clave pública (certificados X.509) que permite a los propietarios legítimos de prefijos IP firmar autorizaciones de origen de ruta (ROAs). Los routers de borde validan las ROAs para descartar anuncios BGP ilegítimos, previniendo secuestros de rutas (BGP Hijacking).

#### **RSTP (Rapid Spanning Tree Protocol)**
- **Dominio / Capa:** Conmutación LAN / Capa 2.
- **Estándar:** IEEE 802.1w (incorporado en IEEE 802.1D-2004).
- **Definición:** Evolución del protocolo clásico de Spanning Tree que reduce drásticamente el tiempo de convergencia de una topología libre de bucles de 30-50 segundos a unos pocos milisegundos mediante un mecanismo activo de propuesta/acuerdo (Proposal-Agreement Handshake) entre conmutadores contiguos.

---

### S

#### **Segment Routing (SR-MPLS / SRv6)**
- **Dominio / Capa:** Transporte Carrier y WAN / Capa 3.
- **Estándares:** RFC 8402, RFC 8986 (SRv6 Network Programming).
- **Definición:** Paradigma moderno de enrutamiento basado en la técnica de enrutamiento en el origen (Source Routing). El nodo emisor antepone una lista ordenada de instrucciones (segmentos identificados por SIDs o direcciones IPv6 de 128 bits) que obligan al paquete a recorrer un camino determinado, eliminando la necesidad de mantener estados dinámicos con LDP o RSVP-TE en los routers centrales.

#### **SONiC (Software for Open Networking in the Cloud)**
- **Dominio / Capa:** Sistemas Operativos de Conmutación (Whitebox) / NOS.
- **Definición:** Sistema operativo de red abierto y modular basado en Debian Linux fundado por Microsoft y gobernado por la Open Compute Project (OCP). Desacopla el software de control del hardware de conmutación mediante la interfaz SAI (Switch Abstraction Interface) y ejecuta sus procesos centrales (BGP, LLDP, SNMP) en microservicios dentro de contenedores Docker.

#### **Spine-and-Leaf**
- *(Ver Clos Network).*

#### **SVI (Switch Virtual Interface)**
- **Dominio / Capa:** Conmutación Multicapa / Capa 3.
- **Definición:** Interfaz lógica enrutada configurada en un switch de Capa 3 asociada directamente a una VLAN específica (ej. `interface Vlan 10`). Actúa como la puerta de enlace predeterminada (Default Gateway) para todos los hosts ubicados en dicha VLAN, posibilitando el enrutamiento inter-VLAN local a velocidad de cable (Line-Rate).

---

### T

#### **TACACS+ (Terminal Access Controller Access-Control System Plus)**
- **Dominio / Capa:** Administración Segura AAA / Capa 7 (TCP 49).
- **Estándar:** RFC 8907 (Cisco Propietario / Estandarizado).
- **Definición:** Protocolo AAA diseñado específicamente para la administración y control de acceso de ingenieros a la consola de conmutadores, enrutadores y firewalls. Separa completamente la autenticación, la autorización comando por comando y la auditoría, y cifra íntegramente la carga útil de los paquetes TCP.

#### **TCAM (Ternary Content Addressable Memory)**
- **Dominio / Capa:** Hardware de Conmutación y Enrutamiento / Capas 2 a 4.
- **Definición:** Memoria de silicio especializada de conmutación que permite comparar claves contra patrones utilizando tres estados lógicos: `0`, `1` y `X` (Don't Care o comodín). Es el motor de hardware que permite a los conmutadores y enrutadores evaluar listas de control de acceso (ACLs), tablas de enrutamiento CIDR y políticas de QoS en tiempo real sin impacto en el rendimiento de la CPU.

#### **TIA-568-D**
- **Dominio / Capa:** Infraestructura Física de Cableado / Capa 1.
- **Definición:** Conjunto de normas técnicas de telecomunicaciones emitidas por la Telecommunications Industry Association (TIA) que define los estándares de diseño, instalación, prueba y categorías de rendimiento para sistemas de cableado estructurado comercial de cobre y fibra óptica.

---

### V

#### **VLAN (Virtual Local Area Network)**
- **Dominio / Capa:** Conmutación LAN / Capa 2.
- **Estándar:** IEEE 802.1Q.
- **Definición:** Segmentación lógica de una red de área local física en múltiples dominios de difusión independientes. El tráfico entre distintas VLANs no puede fluir en Capa 2 y requiere obligatoriamente un dispositivo de Capa 3 (router o conmutador multicapa) para su reenvío.

#### **VRF (Virtual Routing and Forwarding)**
- **Dominio / Capa:** Enrutamiento / Capa 3.
- **Definición:** Tecnología que permite virtualizar un enrutador físico creando múltiples instancias independientes de tablas de enrutamiento que coexisten simultáneamente. Permite que segmentos de red de distintos clientes compartan el mismo hardware físico sin riesgo de fuga de tráfico ni conflictos de direccionamiento IP idéntico (RFC 1918 superpuesto).

#### **VRRP (Virtual Router Redundancy Protocol)**
- **Dominio / Capa:** Alta Disponibilidad L3 / Capa 3 (Protocolo IP 112 / Multicast 224.0.0.18).
- **Estándar:** RFC 5798 (VRRPv3 para IPv4 e IPv6).
- **Definición:** Protocolo estándar de la IETF para redundancia de puerta de enlace por defecto. Un router actúa como Master gestionando la IP virtual (`00-00-5E-00-01-XX`), mientras que uno o más enrutadores actúan como Backup monitoreando los paquetes de aviso periódicos transmitidos cada 1 segundo.

#### **VTEP (VXLAN Tunnel Endpoint)**
- **Dominio / Capa:** Data Center Fabric Overlay / Capas 2 a 4.
- **Estándar:** RFC 7348.
- **Definición:** Entidad originadora o terminadora de túneles VXLAN ubicada en los conmutadores Leaf del datacenter o en hipervisores de virtualización. Encapsula las tramas Ethernet del servidor local en paquetes UDP/IP para enviarlas a través del underlay y las desencapsula en el extremo receptor para entregarlas a la máquina virtual destino.

#### **VXLAN (Virtual Extensible LAN)**
- **Dominio / Capa:** Data Center Overlays / Capa 4 (UDP 4789).
- **Estándar:** RFC 7348.
- **Definición:** Tecnología de virtualización de red que encapsula tramas completas de Capa 2 (Ethernet) dentro de datagramas IP/UDP de Capa 4 (Mac-in-UDP). Incorpora un identificador de red (VNI - VXLAN Network Identifier) de 24 bits que expande el límite de segmentación de las 4,094 VLANs tradicionales a más de 16 millones de segmentos virtuales.

---

### W

#### **WPA3-Enterprise (Wi-Fi Protected Access 3)**
- **Dominio / Capa:** Seguridad Inalámbrica / Capas 2 y 7.
- **Estándar:** Wi-Fi Alliance Specification.
- **Definición:** Modo de seguridad inalámbrica corporativa que requiere autenticación 802.1X y ofrece un modo de alta seguridad de 192 bits (Suite B de la NSA) basado en criptografía elíptica (ECDSA con curva P-384 y AES-256 en modo GCM/GCMP), garantizando máxima resistencia frente a ataques de fuerza bruta y descifrado fuera de línea.

#### **WireGuard**
- **Dominio / Capa:** Redes Privadas Virtuales / Capa 3 (UDP).
- **Estándar:** RFC 8439 (ChaCha20-Poly1305), RFC 7748 (Curve25519).
- **Definición:** Protocolo de túnel VPN de código abierto extremadamente ligero y rápido integrado en el kernel de Linux. Utiliza exclusivamente criptografía moderna de última generación (Noise Protocol Framework, Curve25519 para intercambio de claves, ChaCha20 para cifrado simétrico y Poly1305 para autenticación), eliminando la complejidad y sobrecarga de negociación de IPsec y OpenVPN.

#### **WRED (Weighted Random Early Detection)**
- **Dominio / Capa:** Gestión de Congestión QoS / Capa 3.
- **Definición:** Mecanismo de prevención de congestión que descarta paquetes TCP aleatoriamente antes de que las colas de hardware del router se saturen por completo. Al descartar selectivamente paquetes basados en su valor IP Precedence o DSCP, fuerza a los emisores TCP a reducir su ventana de congestión gradualmente, evitando el fenómeno catastrófico de sincronización global de flujos TCP.

---

### Z

#### **Zero Trust Architecture (ZTA)**
- **Dominio / Capa:** Paradigma de Seguridad Integral.
- **Estándar:** NIST SP 800-207.
- **Definición:** Estrategia integral de ciberseguridad basada en la premisa fundamental de que no existe una confianza implícita concedida a los activos o usuarios en función exclusiva de su ubicación física o propiedad de red. Exige que cada solicitud de acceso sea explícitamente autenticada, rigurosamente autorizada bajo el principio de privilegio mínimo y continuamente cifrada y validada antes de conceder acceso a los datos.
