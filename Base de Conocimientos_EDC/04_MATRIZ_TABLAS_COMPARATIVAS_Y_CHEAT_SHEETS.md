# 📊 Matriz Comparativa Multi-Vendor y Cheat Sheets de Ingeniería EDC
## Network Engineering & Cybersecurity Master Compendium

> **TABLAS MAESTRAS DE EQUIVALENCIA CLI, SUBNETTING, PUERTOS IANA, ÓPTICOS Y FÓRMULAS**  
> **Ubicación:** `Base de Conocimientos_EDC/04_MATRIZ_TABLAS_COMPARATIVAS_Y_CHEAT_SHEETS.md`  
> **Aplicación:** Operación en campo, configuración multi-fabricante, diseño y resolución de incidentes

---

## 1. Matriz Comparativa Multi-Vendor de Comandos CLI

Equivalencias sintácticas directas entre **Cisco (IOS-XE)**, **Huawei (VRP)**, **Aruba (ArubaOS-CX)**, **HP (ProCurve / AOS-S)**, **3Com / H3C (Comware)** y **TP-Link (JetStream)**:

### A. Modos de Navegación y Operaciones Básicas

| Tarea Operativa | Cisco IOS / IOS-XE | Huawei VRP | Aruba ArubaOS-CX | HP ProCurve | 3Com / H3C Comware | TP-Link JetStream |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Entrar a Configuración** | `configure terminal` | `system-view` | `configure terminal` | `configure` | `system-view` | `configure` |
| **Retroceder un Nivel** | `exit` | `quit` | `exit` | `exit` | `quit` | `exit` |
| **Ir al Modo Raíz Exec** | `end` o `Ctrl+Z` | `return` | `end` | `end` | `return` | `end` |
| **Guardar Configuración** | `write memory` / `copy run start` | `save` | `write memory` | `write memory` | `save` | `copy running-config startup-config` |
| **Reiniciar Equipo** | `reload` | `reboot` | `boot system` | `boot` | `reboot` | `reboot` |
| **Ver Configuración Activa** | `show running-config` | `display current-configuration` | `show running-config` | `show run` | `display current-configuration` | `show running-config` |
| **Ver Configuración Guardada** | `show startup-config` | `display saved-configuration` | `show config` | `show config` | `display saved-configuration` | `show startup-config` |

---

### B. Configuración de Interfaces y Puertos L2 (Access / Trunk)

| Tarea de Configuración | Cisco IOS / IOS-XE | Huawei VRP | Aruba ArubaOS-CX | HP ProCurve (AOS-S) | 3Com / H3C Comware | TP-Link JetStream |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Entrar a Interfaz** | `interface Gi0/1` | `interface GE0/0/1` | `interface 1/1/1` | `interface 1` | `interface GE1/0/1` | `interface gigabitEthernet 1/0/1` |
| **Modo Puerto de Acceso** | `switchport mode access` | `port link-type access` | `no routing` | *(Por asignación)* | `port link-type access` | `switchport mode access` |
| **Asignar VLAN Acceso (ej. 10)**| `switchport access vlan 10`| `port default vlan 10` | `vlan access 10` | `vlan 10 untagged 1` | `port default vlan 10` | `switchport access vlan 10` |
| **Modo Puerto Troncal** | `switchport mode trunk` | `port link-type trunk` | `no routing` | *(Por asignación)* | `port link-type trunk` | `switchport mode trunk` |
| **Permitir VLANs en Troncal** | `switchport trunk allowed vlan 10,20` | `port trunk allow-pass vlan 10 20` | `vlan trunk allowed 10,20` | `vlan 10,20 tagged 1` | `port trunk permit vlan 10 20` | `switchport trunk allowed vlan 10,20` |
| **VLAN Nativa en Troncal** | `switchport trunk native vlan 99` | `port trunk pvid vlan 99` | `vlan trunk native 99` | `vlan 99 untagged 1` | `port trunk pvid vlan 99` | `switchport trunk pvid 99` |
| **Apagar / Encender Puerto** | `shutdown` / `no shutdown` | `shutdown` / `undo shutdown` | `shutdown` / `no shutdown` | `disable` / `enable` | `shutdown` / `undo shutdown` | `shutdown` / `no shutdown` |

---

### C. Agregación de Enlaces (LACP) y Spanning Tree (RSTP)

| Tarea Técnica | Cisco IOS / IOS-XE | Huawei VRP | Aruba ArubaOS-CX | HP ProCurve | 3Com / H3C Comware | TP-Link JetStream |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Crear Canal Lógico** | `interface Port-channel 1` | `interface Eth-Trunk 1` | `interface lag 1` | `trunk 1-2 trk1 lacp` | `interface Bridge-Aggregation 1` | `interface port-channel 1` |
| **Asociar Puerto Físico (LACP)**| `channel-group 1 mode active`| `eth-trunk 1` *(en trunk)* | `lag 1` | *(Definido en trunk)*| `port link-aggregation group 1`| `channel-group 1 mode active` |
| **Activar Modo RSTP** | `spanning-tree mode rapid-pvst`| `stp mode rstp` | `spanning-tree mode rstp`| `spanning-tree` | `stp mode rstp` | `spanning-tree mode rstp` |
| **Habilitar BPDU Guard** | `spanning-tree bpduguard enable`| `stp bpdu-protection` | `spanning-tree bpdu-guard`| `spanning-tree 1 bpdu-filter` | `stp bpdu-protection` | `spanning-tree bpdu-guard` |
| **Puerto Rápido (Edge Port)** | `spanning-tree portfast` | `stp edged-port enable` | `spanning-tree port-type admin-edge` | `spanning-tree 1 admin-edge-port` | `stp edged-port enable` | `spanning-tree portfast` |

---

### D. Enrutamiento L3, SVI y Diagnóstico

| Tarea Operativa | Cisco IOS / IOS-XE | Huawei VRP | Aruba ArubaOS-CX | HP ProCurve | 3Com / H3C Comware | TP-Link JetStream |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Crear SVI de Gestión L3** | `interface Vlan10` | `interface Vlanif10` | `interface vlan 10` | `vlan 10 ip address ...` | `interface Vlan-interface10` | `interface vlan 10` |
| **Asignar IP / Máscara** | `ip address 10.1.1.1 255.255.255.0` | `ip address 10.1.1.1 24` | `ip address 10.1.1.1/24` | `ip address 10.1.1.1 255.255.255.0` | `ip address 10.1.1.1 24` | `ip address 10.1.1.1 255.255.255.0` |
| **Ruta Estática por Defecto**| `ip route 0.0.0.0 0.0.0.0 10.1.1.254`| `ip route-static 0.0.0.0 0 10.1.1.254`| `ip route 0.0.0.0/0 10.1.1.254`| `ip route 0.0.0.0 0.0.0.0 10.1.1.254`| `ip route-static 0.0.0.0 0 10.1.1.254`| `ip route 0.0.0.0 0.0.0.0 10.1.1.254`|
| **Ver Tabla de Enrutamiento**| `show ip route` | `display ip routing-table` | `show ip route` | `show ip route` | `display ip routing-table` | `show ip route` |
| **Ver Tabla de Direcciones MAC**| `show mac address-table` | `display mac-address` | `show mac-address` | `show mac-address` | `display mac-address` | `show mac address-table` |
| **Ver Vecinos LLDP** | `show lldp neighbors` | `display lldp neighbor brief`| `show lldp info remote-device`| `show lldp info remote` | `display lldp neighbor-information list`| `show lldp neighbor` |

---

## 2. Cheat Sheet Maestro de Subnetting IPv4 y Prefijos IPv6

### Tabla Completa de Prefijos IPv4 (/8 a /32)

| Prefijo CIDR | Máscara Decimal | Máscara Wildcard (Inversa) | Total IPs | Hosts Usables | Clase Histórica / Aplicación Típica |
| :-: | :--- | :--- | :-: | :-: | :--- |
| **/8** | `255.0.0.0` | `0.255.255.255` | 16,777,216 | 16,777,214 | Red Clase A histórica (ej. `10.0.0.0/8` privada RFC 1918) |
| **/12** | `255.240.0.0` | `0.15.255.255` | 1,048,576 | 1,048,574 | Bloque privado RFC 1918 (`172.16.0.0/12`) |
| **/16** | `255.255.0.0` | `0.0.255.255` | 65,536 | 65,534 | Red Clase B histórica / Bloque `192.168.0.0/16` privado |
| **/20** | `255.255.240.0` | `0.0.15.255` | 4,096 | 4,094 | Supernetting corporativo / Nube AWS VPC subnet grande |
| **/24** | `255.255.255.0` | `0.0.0.255` | 256 | 254 | Red Clase C estándar / Subred LAN empresarial típica |
| **/25** | `255.255.255.128` | `0.0.0.127` | 128 | 126 | Segmentación LAN departamental |
| **/26** | `255.255.255.192` | `0.0.0.63` | 64 | 62 | Segmentos medianos (VLAN de Voz o Administración) |
| **/27** | `255.255.255.224` | `0.0.0.31` | 32 | 30 | Pequeñas oficinas o subred de servidores DMZ |
| **/28** | `255.255.255.240` | `0.0.0.15` | 16 | 14 | Segmentos de equipos de red o balanceadores |
| **/29** | `255.255.255.248` | `0.0.0.7` | 8 | 6 | Enlace WAN multi-punto / Bloques de IPs públicas fijas |
| **/30** | `255.255.255.252` | `0.0.0.3` | 4 | 2 | Enlaces Punto a Punto tradicionales |
| **/31** | `255.255.255.254` | `0.0.0.1` | 2 | 2 | Enlaces Punto a Punto modernos (RFC 3021 - Sin red ni broadcast) |
| **/32** | `255.255.255.255` | `0.0.0.0` | 1 | 1 | Dirección de Host único / Interfaces Loopback de Router |

### Resumen de Direccionamiento IPv6 Especial

| Prefijo IPv6 | Tipo de Dirección | Propósito y Equivalencia IPv4 |
| :--- | :--- | :--- |
| `::/128` | Dirección no especificada | Equivalente a `0.0.0.0` en IPv4 (solicitudes DHCPv6) |
| `::1/128` | Dirección de Loopback | Equivalente a `127.0.0.1` en IPv4 |
| `fe80::/10` | Link-Local (Enlace Local) | Obligatoria en cada interfaz activa; no enrutable más allá del enlace |
| `fc00::/7` | Unique Local Address (ULA) | Equivalente a direcciones privadas RFC 1918 (RFC 4193) |
| `2000::/3` | Global Unicast Address (GUA) | Direcciones públicas globales enrutables en Internet |
| `ff00::/8` | Multicast | Direcciones de multidifusión (reemplaza por completo el broadcast) |
| `ff02::1` | Multicast Todos los Nodos | Equivalente al broadcast local de capa 2/3 |
| `ff02::2` | Multicast Todos los Routers | Mensajes de Router Solicitation (RS) de clientes |
| `ff02::5` / `ff02::6` | OSPFv3 Multicast | `ff02::5` (Todos los routers OSPF) / `ff02::6` (Todos los DR/BDR) |

---

## 3. Catálogo de Puertos IANA (TCP / UDP) con Análisis de Riesgo y Mitigación

| Puerto | Protocolo | Capa Transporte | Servicio | Nivel de Riesgo | Vector de Amenaza Típico | Medida de Mitigación / Contramedida |
| :-: | :--- | :-: | :--- | :-: | :--- | :--- |
| **20 / 21** | FTP | TCP | Transferencia de archivos | 🔴 Alto | Credenciales y datos en texto claro, rebote FTP | Deshabilitar y sustituir por SFTP (puerto 22) |
| **22** | SSH / SFTP | TCP | Consola segura / SCP | 🟡 Medio | Fuerza bruta de claves, explotación OpenSSH | Autenticación obligatoria por llaves públicas, Fail2ban |
| **23** | Telnet | TCP | Consola remota | 🔴 Crítico | Intercepción pasiva de contraseñas de red | **Prohibido en producción**: Reemplazar por SSHv2 |
| **25** | SMTP | TCP | Envío de correo | 🟡 Medio | Open Relay, spam masivo, spoofing de remitente | Configurar SPF, DKIM, DMARC y autenticación TLS |
| **49** | TACACS+ | TCP | Administración AAA | 🟢 Bajo | Fuerza bruta si se comparte clave pre-compartida | Clave secreta robusta de 32+ caracteres, túnel TLS |
| **53** | DNS | UDP / TCP | Resolución de nombres | 🔴 Alto | Envenenamiento de caché, DDoS por amplificación | Implementar DNSSEC, rate-limiting RRL, Anycast |
| **67 / 68** | DHCP | UDP | Configuración IP dinámica | 🔴 Alto | Servidor DHCP falso (Rogue), agotamiento de IPs | Habilitar **DHCP Snooping** en todos los conmutadores |
| **69** | TFTP | UDP | Transferencia trivial | 🔴 Crítico | Sin autenticación, transferencia de backups planos | Confinar exclusivamente a VLAN aislada de gestión |
| **80** | HTTP | TCP | Tráfico Web plano | 🔴 Alto | Man-in-the-Middle, intercepción de cookies | Redirección obligatoria 301 a HTTPS y HSTS Preload |
| **88** | Kerberos | TCP / UDP | Autenticación Active Directory | 🟡 Medio | Ataques Kerberoasting, Golden Ticket | Cifrado AES obligatorio (deshabilitar RC4), cuentas seguras |
| **123** | NTP | UDP | Sincronización horaria | 🟡 Medio | Ataques DDoS de amplificación, desincronización | Filtrar `monlist`, autenticación criptográfica NTP |
| **161 / 162** | SNMP | UDP | Monitoreo y Traps | 🔴 Alto (v1/v2c) | Robo de credenciales comunitarias (`public`), DoS | Migrar obligatoriamente a **SNMPv3 con authPriv (SHA/AES)** |
| **179** | BGP | TCP | Enrutamiento Internet | 🔴 Alto | Inyección de rutas no autorizadas, DoS al peering | Autenticación MD5/TCP-AO, RPKI y filtrado GTSM (TTL=255) |
| **389 / 636** | LDAP / LDAPS | TCP | Consultas de directorio | 🟡 Medio | Exfiltración de atributos de usuario | Exigir LDAPS (puerto 636 cifrado con TLS) |
| **443** | HTTPS | TCP (y UDP/QUIC) | Web cifrada | 🟢 Bajo | Tráfico malicioso oculto en el túnel TLS | Inspección profunda SSL (SSL Deep Inspection en NGFW) |
| **445** | SMB | TCP | Compartición de archivos Windows | 🔴 Crítico | Propagación de Ransomware (EternalBlue / WannaCry)| **Bloquear estrictamente en el perímetro WAN** |
| **500 / 4500**| IKE / NAT-T | UDP | Negociación VPN IPsec | 🟢 Bajo | Ataques de fuerza bruta en claves PSK débiles | Usar grupos Diffie-Hellman >= 19 (ECDH) o certificados X.509 |
| **5060 / 5061**| SIP / SIPS | UDP / TCP | Señalización telefonía VoIP | 🔴 Alto | Fraude telefónico (Toll Fraud), secuestro de llamadas| Exigir SIPS (puerto 5061 con TLS) y SBC perimetral |
| **1812 / 1813**| RADIUS | UDP | Autenticación y Accounting | 🟢 Bajo | Vulnerabilidad si la clave secreta es débil | Claves compartidas complejas o túnel RadSec (TLS) |
| **3389** | RDP | TCP | Escritorio Remoto Windows | 🔴 Crítico | Fuerza bruta, BlueKeep, acceso administrativo | **Nunca exponer a Internet**: Exigir VPN previa o MFA |
| **4789** | VXLAN | UDP | Overlay de Datacenter | 🟡 Medio | Inyección de tramas virtuales en la fábrica | Aislar estrictamente la red Underlay de las cargas de trabajo |

---

## 4. Matriz Técnica de Medios Físicos: Cobre, Fibra Óptica y Transceptores

### A. Categorías de Cable de Par Trenzado de Cobre (ANSI/TIA-568-D)

| Categoría | Frecuencia Máx. | Velocidad Máxima | Distancia Máx. | Blindaje Estándar | Aplicación Típica Recomendada |
| :--- | :-: | :-: | :-: | :--- | :--- |
| **Cat 5e** | 100 MHz | 1 Gbps | 100 metros | UTP (Sin blindaje) | Redes de oficina básicas heredadas |
| **Cat 6** | 250 MHz | 1 Gbps (10G hasta 55m)| 100 m / 55 m | UTP o F/UTP | Estándar empresarial común |
| **Cat 6A** | 500 MHz | 10 Gbps | 100 metros | F/UTP o U/FTP | Datacenters, enlaces AP Wi-Fi 6/7, PoE++ 90W |
| **Cat 7** | 600 MHz | 10 Gbps | 100 metros | S/FTP (Malla + Papel) | Entornos industriales de alto ruido electromagnético |
| **Cat 8** | 2000 MHz | 25 Gbps / 40 Gbps | 30 metros | S/FTP blindado | Conexiones Top-of-Rack (ToR) en Centros de Datos |

### B. Fibras Ópticas Monomodo y Multimodo (ISO/IEC 11801)

| Tipo de Fibra | Clasificación | Diámetro Núcleo/Revestimiento | Longitud de Onda | Atenuación Típica | Distancia Máx. (10 Gbps) | Distancia Máx. (100 Gbps) |
| :--- | :--- | :-: | :-: | :-: | :-: | :-: |
| **Multimodo** | **OM1** | 62.5 / 125 µm | 850 nm | 3.5 dB/km | 33 metros | No soportado |
| **Multimodo** | **OM2** | 50 / 125 µm | 850 nm | 3.0 dB/km | 82 metros | No soportado |
| **Multimodo** | **OM3** | 50 / 125 µm (Láser Aqua)| 850 nm | 3.0 dB/km | 300 metros | 70 metros (100GBASE-SR4) |
| **Multimodo** | **OM4** | 50 / 125 µm (Láser Violeta)| 850 nm | 2.8 dB/km | 400 metros | 100 metros (100GBASE-SR4) |
| **Multimodo** | **OM5** | 50 / 125 µm (SWDM Verde)| 850 - 953 nm | 2.5 dB/km | 400 metros | 150 metros (SWDM4) |
| **Monomodo** | **OS1** | 9 / 125 µm (Interior) | 1310 / 1550 nm | 1.0 dB/km | 10 km (10GBASE-LR) | 10 km (100GBASE-LR4) |
| **Monomodo** | **OS2** | 9 / 125 µm (Exterior) | 1310 / 1550 nm | 0.4 dB/km | 40 km (10GBASE-ER) | 40 km (100GBASE-ER4) |

### C. Formatos de Módulos Transceptores Ópticos

| Formato | Canales Eléctricos | Tasa por Canal | Velocidad Agregada | Conector Óptico Típico | Consumo Térmico Máx. |
| :--- | :-: | :-: | :-: | :--- | :-: |
| **SFP** | 1 | 1.25 Gbps | **1 Gbps** | LC Duplex | ~1.0 W |
| **SFP+** | 1 | 10.3 Gbps | **10 Gbps** | LC Duplex | ~1.5 W |
| **SFP28** | 1 | 25.78 Gbps | **25 Gbps** | LC Duplex | ~1.8 W |
| **QSFP+** | 4 | 10.3 Gbps | **40 Gbps** | MPO-12 o LC Duplex (BiDi) | ~3.5 W |
| **QSFP28**| 4 | 25.78 Gbps | **100 Gbps** | MPO-12 o LC Duplex (CWDM4) | ~4.5 W |
| **QSFP-DD**| 8 | 50 Gbps (PAM4)| **400 Gbps** | MPO-16 o CS Connector | ~12.0 W |

---

## 5. Fórmulas Matemáticas y Reglas de Ingeniería (Cheat Sheet Numérico)

### A. Cálculo del Presupuesto de Enlace Óptico (Optical Power Budget)

Para garantizar que un enlace de fibra funcione sin degradación ni saturación, se debe calcular la potencia recibida estimada ($P_{rx}$) frente a la sensibilidad del receptor:

$$\text{Margen de Seguridad (dB)} = P_{tx\_min} - \text{Sensibilidad}_{rx\_min} - \text{Pérdida Total del Canal}$$

Donde la Pérdida Total del Canal se calcula como:

$$\text{Pérdida Total (dB)} = (\alpha \cdot L) + (N_{\text{conectores}} \cdot A_{\text{conector}}) + (N_{\text{empalmes}} \cdot A_{\text{empalme}}) + M_{\text{diseño}}$$

- $\alpha$: Coeficiente de atenuación de la fibra (dB/km). (Típico: $0.35\text{ dB/km}$ a 1310 nm en OS2; $3.0\text{ dB/km}$ a 850 nm en OM3).
- $L$: Longitud total del enlace en kilómetros.
- $A_{\text{conector}}$: Atenuación por conector óptico (Norma TIA: máx $0.75\text{ dB}$, típico $0.3\text{ dB}$).
- $A_{\text{empalme}}$: Atenuación por empalme de fusión (Típico $0.05\text{ dB}$ a $0.1\text{ dB}$).
- $M_{\text{diseño}}$: Margen de degradación por envejecimiento (Recomendado: $3.0\text{ dB}$).

---

### B. Sobrecarga de Encapsulamiento y MSS Clamping en Túneles

Cuando los paquetes atraviesan túneles (IPsec, GRE, VXLAN), las cabeceras adicionales reducen el tamaño de carga útil utilizable. Si la MTU física es de 1500 bytes:

$$\text{MSS (Maximum Segment Size)} = \text{MTU} - \text{Cabecera IP} - \text{Cabecera TCP} - \text{Sobrecarga del Túnel}$$

| Tipo de Túnel | Cabeceras Adicionales | Sobrecarga Típica (Bytes) | MTU Máxima sin Fragmentación | MSS Recomendado para Evitar Blackholes |
| :--- | :--- | :-: | :-: | :-: |
| **Ethernet Estándar** | Ninguna (IP + TCP) | 0 bytes | 1500 bytes | `1460 bytes` |
| **VLAN 802.1Q** | Etiqueta 802.1Q | 4 bytes | 1500 bytes (con switch 1504) | `1460 bytes` |
| **PPPoE** | Cabecera PPPoE + PPP | 8 bytes | 1492 bytes | `1452 bytes` |
| **GRE Puro** | Cabecera GRE + IP externa | 24 bytes | 1476 bytes | `1436 bytes` |
| **VXLAN (Data Center)** | IP ext (20) + UDP (8) + VXLAN (8) + Eth (14) | 50 a 54 bytes | Requiere **Jumbo Frame** (9000 bytes) | `1450 bytes` (si underlay es 1500) |
| **IPsec ESP Túnel** | IP ext (20) + SPI/Seq (8) + IV (8) + Pad (0-15) + ICV (16)| 56 a 72 bytes | 1428 a 1444 bytes | **`1360 a 1400 bytes`** (Seguro) |

Comando universal de ajuste en routers Cisco para interfaces de túnel:
```cisco
interface Tunnel1
 ip tcp adjust-mss 1360
```

---

### C. Dimensionamiento de Ancho de Banda para Telefonía VoIP

El consumo de ancho de banda real de una llamada sobre Ethernet es sustancialmente mayor que la tasa nominal del códec debido a la sobrecarga de capas L2/L3/L4:

$$\text{Ancho de Banda por Llamada (kbps)} = \frac{\text{Tamaño Total del Paquete (bits)}}{\text{Intervalo de Muestreo (ms)}} = \text{Tamaño Total (Bytes)} \times 8 \times \text{Paquetes por Segundo (pps)}$$

*Para códec G.711 (muestreo estándar de 20 ms = 50 pps):*
- Carga útil de voz: $64\text{ kbps} \times 0.02\text{ s} = 160\text{ Bytes}$.
- Cabecera RTP: 12 Bytes.
- Cabecera UDP: 8 Bytes.
- Cabecera IP: 20 Bytes.
- Cabecera Ethernet + FCS: 18 Bytes (sin preámbulo).
- **Tamaño total de la trama Ethernet:** $160 + 12 + 8 + 20 + 18 = 218\text{ Bytes}$.
- **Consumo real de red:** $218\text{ Bytes} \times 8 \times 50\text{ pps} = \mathbf{87.2\text{ kbps}}$ por llamada (unidireccional).

---

### D. Reglas Nemotécnicas de Decibeles (dB) en Potencia de RF y Óptica

El decibelio es una unidad logarítmica que relaciona dos valores de potencia ($P_1$ y $P_2$):

$$\text{Ganancia / Pérdida (dB)} = 10 \cdot \log_{10}\left(\frac{P_2}{P_1}\right)$$

*Reglas prácticas indispensables para cálculo mental:*
- **$+3\text{ dB}$:** Duplica exactamente la potencia ($P \times 2$).
- **$-3\text{ dB}$:** Reduce la potencia exactamente a la mitad ($P / 2$).
- **$+10\text{ dB}$:** Multiplica la potencia por 10 ($P \times 10$).
- **$-10\text{ dB}$:** Reduce la potencia a la décima parte ($P / 10$).
- **$0\text{ dBm}$:** Equivale exactamente a $1\text{ milivatio (mW)}$.
- **$20\text{ dBm}$:** Equivale a $100\text{ mW}$ (Potencia máxima permitida típica en Wi-Fi 2.4 GHz).
