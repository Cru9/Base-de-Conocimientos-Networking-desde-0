# 🛠️ Tools_BC: Suite Avanzada de Redes y Ciberseguridad

<p align="center">
  <img src="https://img.shields.io/badge/Lenguajes-CMD%20%7C%20PowerShell%20%7C%20Python%203-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Entorno-Windows%2010%20%2F%2011%20%2F%20Server-0078d4?style=for-the-badge&logo=windows&logoColor=white" />
  <img src="https://img.shields.io/badge/Librerías-Scapy%20%7C%20Netmiko%20%7C%20Rich-darkgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Cobertura-OSI%20L2--L7%20%7C%20OT%20%7C%20DDI%20%7C%20SOC-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Licencia-MIT-green?style=for-the-badge" />
</p>

---

## 📌 Visión General

**`Tools_BC`** es la suite de herramientas ejecutables desarrollada para acompañar y poner en práctica los conocimientos técnicos del **Network Engineering & Cybersecurity Master Compendium**. 

A diferencia de scripts básicos, esta suite integra herramientas funcionales en tres tecnologías (**CMD**, **PowerShell** y **Python**) preparadas para escenarios de producción, soporte en sitio, laboratorios de certificación (**Cisco CCNA/CCNP, Huawei HCIA/HCIP, CompTIA**) y auditorías defensivas de seguridad.

---

## 🏛️ Estructura del Directorio

```text
Tools_BC/
│
├── Menu_Principal.cmd              -> Lanzador Maestro interactivo (CMD, PowerShell y Python con 1 clic)
├── requirements.txt                -> Dependencias Python (Rich, Netmiko, Scapy, Paramiko, etc.)
├── README.md                       -> Guía técnica de uso y catálogo de herramientas
│
├── cmd/                            -> Utilidades por Lotes nativas de Windows (Zero Dependencies)
│   ├── 01_Reset_Pila_Red.cmd       -> Restablecimiento de DNS, ARP, Winsock, TCP/IP y DHCP
│   ├── 02_Rutas_Estaticas_Mgr.cmd  -> Gestor interactivo de rutas estáticas y persistentes
│   └── 03_Diagnostico_Rapido.cmd   -> Chequeo veloz de IP, Gateway, resolución DNS e IP Pública
│
├── powershell/                     -> Scripts de Administración y Auditoría de Seguridad
│   ├── Detect_Rogue_DHCP.ps1       -> Detector defensivo de servidores DHCP no autorizados (L2)
│   ├── Monitor_Conexiones_SOC.ps1  -> Monitor continuo de sockets TCP, procesos y puertos C2
│   ├── Auditor_Firewall_Reglas.ps1 -> Auditor de reglas de entrada abiertas hacia Any en Windows Firewall
│   └── Test_DNS_Benchmark.ps1      -> Comparador de latencias DNS (Cloudflare, Google, Quad9, Local)
│
└── python/                         -> Módulos Avanzados de Automatización, Forense y Ciberseguridad
    ├── menu_tools.py               -> Tablero interactivo estilizado con Rich en consola
    ├── vlsm_calculator.py          -> Calculadora VLSM con generación de comandos Cisco y Huawei
    ├── multivendor_backup.py       -> Respaldo SSH y motor Diff con Netmiko (Cisco, Huawei, Aruba, MikroTik)
    ├── pcap_analyzer.py            -> Analizador forense PCAP con Scapy (Retransmisiones TCP, Resets, DNS)
    ├── arp_spoof_detector.py       -> Detector pasivo en tiempo real de ataques ARP Poisoning (MITM)
    ├── tls_cert_inspector.py       -> Auditor de certificados SSL/TLS, días de caducidad y Cipher Suites
    ├── syslog_collector.py         -> Servidor Syslog UDP (RFC 5424) con severidad en colores y log a archivo
    ├── ot_industrial_scanner.py    -> Escáner de redes industriales OT/SCADA (Modbus, S7, DNP3, Purdue)
    └── port_banner_grabber.py      -> Escáner multihilo TCP con captura de banners de infraestructura
```

---

## 🚀 Cómo Ejecutar las Herramientas

### Método 1: El Lanzador Maestro (Recomendado)
Haz doble clic en el archivo:
```bat
Tools_BC\Menu_Principal.cmd
```
* **Ventajas:** Abre un menú interactivo con numeración directa (1 al 16), elude de manera segura las restricciones de ejecución de PowerShell (`-ExecutionPolicy Bypass`), valida la presencia de Python y permite lanzar cualquier script sin lidiar con rutas manuales.

---

### Método 2: Menú Gráfico en Consola de Python (Rich Dashboard)
Para una experiencia visual moderna con tablas de alta definición en la terminal:
```bash
python Tools_BC/python/menu_tools.py
```

---

### Método 3: Ejecución Individual

#### 1. Scripts CMD:
```cmd
cd Tools_BC\cmd
01_Reset_Pila_Red.cmd
```

#### 2. Scripts PowerShell:
Si los ejecutas individualmente desde tu terminal de PowerShell, utiliza el parámetro `-ExecutionPolicy Bypass`:
```powershell
powershell -ExecutionPolicy Bypass -File .\Tools_BC\powershell\Detect_Rogue_DHCP.ps1
powershell -ExecutionPolicy Bypass -File .\Tools_BC\powershell\Monitor_Conexiones_SOC.ps1
powershell -ExecutionPolicy Bypass -File .\Tools_BC\powershell\Auditor_Firewall_Reglas.ps1
powershell -ExecutionPolicy Bypass -File .\Tools_BC\powershell\Test_DNS_Benchmark.ps1
```

#### 3. Scripts Python:
```bash
python Tools_BC/python/vlsm_calculator.py
python Tools_BC/python/multivendor_backup.py
python Tools_BC/python/pcap_analyzer.py
python Tools_BC/python/arp_spoof_detector.py
python Tools_BC/python/tls_cert_inspector.py
python Tools_BC/python/syslog_collector.py
python Tools_BC/python/ot_industrial_scanner.py
python Tools_BC/python/port_banner_grabber.py
```

---

## 📚 Catálogo Detallado de Herramientas y Correspondencia con el Compendio

### 1. Herramientas CMD

| Script | Dominio Técnico | Relación con el Compendio | Utilidad Práctica |
| :--- | :--- | :--- | :--- |
| **`01_Reset_Pila_Red.cmd`** | Troubleshooting de Host | [Troubleshooting](../Troubleshooting/README.md) | Vía rápida para resolver conflictos IP, loops de Winsock o registros DNS obsoletos en Windows en 6 pasos automáticos. |
| **`02_Rutas_Estaticas_Mgr.cmd`** | Enrutamiento IPv4 | [Routing_y_WAN](../Routing_y_WAN/README.md) | Permite dar de alta y probar saltos hacia redes de gestión, túneles VPN o laboratorios de forma temporal o persistente (`-p`). |
| **`03_Diagnostico_Rapido.cmd`** | Conectividad Básica | [OSI](../OSI/README.md) | Pantallazo de 3 segundos que valida tarjeta de red, salto al Default Gateway, tiempo de respuesta DNS e IP pública de salida. |

---

### 2. Herramientas PowerShell

| Script | Dominio Técnico | Relación con el Compendio | Utilidad Práctica |
| :--- | :--- | :--- | :--- |
| **`Detect_Rogue_DHCP.ps1`** | Seguridad L2 / DDI | [Ciberseguridad_OSI](../Ciberseguridad_OSI/README.md) | Envía un paquete `DHCP Discover` broadcast real y escucha las ofertas. Alerta si detecta más de un servidor DHCP en la LAN (justifica el uso de **DHCP Snooping**). |
| **`Monitor_Conexiones_SOC.ps1`** | Monitoreo SOC / Malware | [Ciberseguridad_OSI](../Ciberseguridad_OSI/README.md) | Muestra sockets activos en vivo, los procesos propietarios y alerta si detecta conexiones hacia puertos comunes de balizas C2 (4444, 1337, etc.). |
| **`Auditor_Firewall_Reglas.ps1`** | Seguridad en Endpoints | [Firewalls_y_VPN](../Firewalls_y_VPN/README.md) | Audita reglas de entrada en Windows Defender Firewall que expongan puertos críticos (SMB 445, RDP 3389, RPC 135) hacia orígenes abiertos (`Any / 0.0.0.0/0`). Exporta a CSV. |
| **`Test_DNS_Benchmark.ps1`** | Rendimiento DDI | [Servicios_DDI_y_Gestion](../Servicios_DDI_y_Gestion/README.md) | Compara en paralelo la velocidad de resolución contra Cloudflare (1.1.1.1), Google (8.8.8.8), Quad9 (9.9.9.9), OpenDNS y el DNS local, calculando promedios y mínimos. |

---

### 3. Herramientas Python

| Script | Dominio Técnico | Relación con el Compendio | Utilidad Práctica |
| :--- | :--- | :--- | :--- |
| **`vlsm_calculator.py`** | Direccionamiento L3 | [OSI](../OSI/README.md) / [Routing_y_WAN](../Routing_y_WAN/README.md) | Toma una red base y una lista de subredes con hosts requeridos. Asigna prefijos de forma óptima calculando el desperdicio y genera comandos listos para copiar en Cisco IOS (`ip address...`) y Huawei VRP. |
| **`multivendor_backup.py`** | Automatización Multi-Vendor | [SW](../SW/README.md) / [Troubleshooting](../Troubleshooting/README.md) | Conexión SSH mediante `Netmiko` hacia switches Cisco, Huawei, Aruba y MikroTik. Guarda la configuración con timestamp y cuenta con un **motor Diff visual** para auditar qué cambió entre versiones. Incluye modo demo. |
| **`pcap_analyzer.py`** | Análisis Forense de Paquetes | [Wireshark_Analysis](../Wireshark_Analysis/README.md) | Procesa capturas `.pcap/.pcapng` con `Scapy`. Detecta retransmisiones TCP, conexiones reseteadas (RST), consultas DNS más frecuentes y porcentaje de protocolos L3/L4. Incluye generador de capturas sintéticas de prueba. |
| **`arp_spoof_detector.py`** | Ciberseguridad Defensiva L2 | [Ciberseguridad_OSI](../Ciberseguridad_OSI/README.md) | Aprende la IP y MAC del Default Gateway y monitorea el tráfico ARP de la red. Si un atacante intenta envenenar la tabla ARP (MITM), lanza una alerta crítica en pantalla. Incluye modo de prueba. |
| **`tls_cert_inspector.py`** | Seguridad L6/L7 | [Ciberseguridad_OSI](../Ciberseguridad_OSI/README.md) | Inspecciona certificados X.509 de servidores web y firewalls. Detecta versiones TLS inseguras (1.0/1.1), calcula los días exactos para su vencimiento y audita la suite criptográfica negociada. |
| **`syslog_collector.py`** | Gestión y Telemetría | [Servicios_DDI_y_Gestion](../Servicios_DDI_y_Gestion/README.md) | Servidor Syslog UDP RFC 5424. Recibe eventos en tiempo real de routers, switches y firewalls, coloreando la salida según la severidad (Emergency a Debug) y persistiendo en archivo `.log`. |
| **`ot_industrial_scanner.py`** | Ciberseguridad OT/SCADA | [Redes_Industriales_OT](../Redes_Industriales_OT/README.md) | Audita la exposición de protocolos industriales críticos (Modbus TCP 502, Siemens S7 102, EtherNet/IP 44818, DNP3 20000, BACnet) y evalúa el cumplimiento de la segmentación del Modelo Purdue (ISA/IEC 62443). |
| **`port_banner_grabber.py`** | Reconocimiento y Auditoría | [Firewalls_NGFW_Lideres](../Firewalls_NGFW_Lideres/README.md) | Escáner multihilo TCP de alta velocidad que realiza Banner Grabbing sobre servicios de infraestructura (SSH, Telnet, HTTP, BGP, SIP, etc.) para identificar versiones de firmware. |

---

## ⚙️ Requisitos de Instalación

Los scripts de CMD y PowerShell son 100% nativos de Windows y no requieren software externo.

Para los módulos de Python:
- **Python:** 3.10 o superior (Verificado en Python 3.14).
- **Instalación rápida de dependencias:**
  ```bash
  python -m pip install -r Tools_BC/requirements.txt
  ```
  *(O directamente desde la opción `[P]` en el menú `Menu_Principal.cmd`)*.

---

## 🛡️ Consideraciones de Permisos

- **Herramientas que requieren ejecutar como Administrador:**
  - `01_Reset_Pila_Red.cmd` (Reinicio de TCP/IP y Winsock).
  - `02_Rutas_Estaticas_Mgr.cmd` (Modificación de tablas de rutas de Windows).
  - `arp_spoof_detector.py` (Captura raw con Scapy para monitoreo en vivo de la tarjeta de red).
  - `syslog_collector.py` (Si se utiliza el puerto estándar privilegiado UDP 514).
- **Herramientas que funcionan sin privilegios elevados:**
  - `03_Diagnostico_Rapido.cmd`.
  - `vlsm_calculator.py`.
  - `multivendor_backup.py`.
  - `pcap_analyzer.py`.
  - `tls_cert_inspector.py`.
  - `ot_industrial_scanner.py`.
  - `port_banner_grabber.py`.
  - `Test_DNS_Benchmark.ps1`.
  - `Auditor_Firewall_Reglas.ps1` (Modo lectura).

---

**Desarrollado para:** Network Engineering & Cybersecurity Master Compendium  
**Autor:** Ezequiel ([@Cru9](https://github.com/Cru9))  
**Licencia:** [MIT License](../LICENSE)
