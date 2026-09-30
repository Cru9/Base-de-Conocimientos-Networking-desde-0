# 🪟 Tools_BC_Windows: Suite Nativa de Redes y Ciberseguridad para Windows

<p align="center">
  <img src="https://img.shields.io/badge/Entorno-Windows%2010%20%7C%2011%20%7C%20Server-0078d4?style=for-the-badge&logo=windows&logoColor=white" />
  <img src="https://img.shields.io/badge/Scripts-CMD%20%2B%20PowerShell-002456?style=for-the-badge&logo=powershell&logoColor=white" />
  <img src="https://img.shields.io/badge/Privilegios-Auto--Elevacion%20UAC-darkgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Cobertura-Capas%20OSI%20L1--L7%20%2B%20OT-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Licencia-MIT-green?style=for-the-badge" />
</p>

---

## 📌 Visión General

**`Tools_BC_Windows`** es una suite de herramientas 100% nativas desarrolladas en **Batch (.cmd)** y **PowerShell (.ps1)** para estaciones de trabajo y servidores Windows (Windows 10, Windows 11, Windows Server 2016/2019/2022). 

No requiere instalar entornos adicionales (como Python o Node.js), aprovechando las capacidades nativas de la consola del sistema, WMI/CIM, la pila de sockets de .NET y las utilidades `netsh`, `route`, `w32tm` e `ipconfig`.

---

## 🛠️ Herramienta Destacada: `Configurador_IP_Avanzado.cmd`

Diseñada especialmente para ingenieros de campo, técnicos de soporte y **usuarios avanzados** (incluyendo miembros del grupo local de Windows *Operadores de configuración de red* / *Network Configuration Operators*):

### ✨ Capacidades Principales
1. **Auto-Elevación Inteligente:** Detecta si se ejecuta con permisos estándar o avanzados; si requiere elevación, invoca automáticamente la ventana de confirmación UAC (`RunAs`) sin cerrar la sesión de trabajo.
2. **Soporte Flexible de Máscaras:** Permite ingresar máscaras en notación decimal clásica (`255.255.255.0`, `255.255.255.252`, etc.) o en prefijo CIDR compacto (`/24`, `/16`, `/28`, `/30`), convirtiéndolas automáticamente.
3. **Conmutación Inmediata a DHCP:** Restablece la IP y los servidores DNS a modo automático con un solo clic y renueva la concesión al instante.
4. **Perfiles Rápidos de DNS:** Permite aplicar con un solo número perfiles de DNS públicos líderes:
   - **Cloudflare:** `1.1.1.1` / `1.0.0.1` (Velocidad y privacidad).
   - **Google Public DNS:** `8.8.8.8` / `8.8.4.4`.
   - **Quad9:** `9.9.9.9` (Filtrado de dominios maliciosos y C2).
   - DNS Personalizado / Manual.
5. **Multihoming L3:** Permite añadir direcciones IP secundarias adicionales en la misma interfaz de red (ideal para laboratorios o gestión de dispositivos en rangos disjuntos).
6. **Respaldar y Restaurar Configuración:** Exporta un volcado completo de la configuración actual (`netsh interface ipv4 dump`) a un archivo de texto con timestamp para restaurarlo ante cualquier contingencia.
7. **Modificación de MTU:** Cambia el tamaño de MTU de forma persistente (ej. 1500 estándar, 1400/1420 para túneles VPN/PPPoE, 9000 para Jumbo Frames).
8. **Ciclo de Interfaz (Restart):** Deshabilita y re-habilita el adaptador automáticamente para renegociar estados de enlace.

---

## 🏛️ Estructura del Directorio

```text
Tools_BC_Windows/
│
├── Menu_Maestro_Windows.cmd           -> Lanzador Maestro interactivo (Acceso a todas las herramientas)
├── Configurador_IP_Avanzado.cmd       -> Configurador dedicado de IP, Máscara, Gateway y DNS
├── README.md                          -> Guía técnica y manual de referencia
│
├── cmd/                               -> Scripts por Lotes (.cmd)
│   ├── 01_Configurador_IP_Avanzado.cmd-> Enlace directo al configurador de red
│   ├── 02_Hardening_Red_Insegura.cmd  -> Deshabilita SMBv1, LLMNR, NetBIOS sobre TCP y WPAD
│   ├── 03_Diagnostico_L1_L4_Completo.cmd -> Chequeo estructurado por capas OSI (L1 a L4)
│   ├── 04_Control_Servicios_Red.cmd   -> Reinicio de servicios (DHCP, DNS Cache, W32Time, Firewall)
│   └── 05_Optimizador_TCP_Pila.cmd    -> Optimización TCP Window Auto-Tuning, RSS, ECN y CUBIC
│
└── powershell/                        -> Scripts de Ingeniería y Diagnóstico (.ps1)
    ├── 01_Diagnostico_L1_Fisico.ps1   -> Velocidad Link, Duplex, errores de transmisión CRC y descartes
    ├── 02_Auditoria_L2_ARP_MAC.ps1    -> Tabla ARP, identificación de Gateway y resolución de OUI
    ├── 03_Inspector_Rutas_Traceroute.ps1 -> Traza WAN hop-by-hop con RTT en ms y resolución PTR
    ├── 04_Auditor_TCP_Sockets_Salud.ps1  -> Estados TCP, puertos Listen y detección de fugas CloseWait
    ├── 05_Auditor_DNS_DHCP_NTP.ps1    -> Servidores DNS, concesiones DHCP y sincronización W32Time
    ├── 06_Auditor_WiFi_Enterprise.ps1 -> RSSI en dBm, estándar 802.11, canal, banda 2.4/5/6GHz y WPA3
    ├── 07_Gestor_Firewall_Perfiles.ps1-> Auditoría de perfiles Domain, Private y Public de Windows Firewall
    ├── 08_Verificador_QoS_DSCP.ps1    -> Verificación de directivas QoS y marcado de paquetes RFC 4594
    └── 09_Tester_Conectividad_OT.ps1  -> Sondeo de puertos industriales Modbus, S7, EtherNet/IP, DNP3
```

---

## 🚀 Cómo Ejecutar

### Método 1: Menú Maestro Unificado
Haz doble clic en:
> [`Tools_BC_Windows\Menu_Maestro_Windows.cmd`](file:///c:/Users/z_eke/OneDrive/Escritorio/BC/Tools_BC_Windows/Menu_Maestro_Windows.cmd)

Permite navegar entre las 14 herramientas mediante un menú numérico intuitivo.

### Método 2: Acceso Directo al Configurador de IP
Haz doble clic en:
> [`Tools_BC_Windows\Configurador_IP_Avanzado.cmd`](file:///c:/Users/z_eke/OneDrive/Escritorio/BC/Tools_BC_Windows/Configurador_IP_Avanzado.cmd)

---

## 📚 Matriz de Correspondencia con el Compendio Técnico

| Capa / Dominio | Herramienta | Módulo del Compendio | Funcionalidad Clave |
| :---: | :--- | :--- | :--- |
| **Config Host** | [`Configurador_IP_Avanzado.cmd`](./Configurador_IP_Avanzado.cmd) | [OSI](../OSI/README.md) / [Routing_y_WAN](../Routing_y_WAN/README.md) | Cambia IP, máscara, gateway, DNS y DHCP con auto-elevación de privilegios. |
| **Capa 1** | [`01_Diagnostico_L1_Fisico.ps1`](./powershell/01_Diagnostico_L1_Fisico.ps1) | [Cableado_y_Fibra_Optica](../Cableado_y_Fibra_Optica/README.md) | Velocidad de enlace, dúplex, paquetes descartados y diagnóstico de cable defectuoso. |
| **Capa 2** | [`02_Auditoria_L2_ARP_MAC.ps1`](./powershell/02_Auditoria_L2_ARP_MAC.ps1) | [SW](../SW/README.md) / [Ciberseguridad_OSI](../Ciberseguridad_OSI/README.md) | Mapeo de tabla ARP, detección de Gateway, búsqueda de OUI y colisiones de MAC. |
| **Capa 3** | [`03_Inspector_Rutas_Traceroute.ps1`](./powershell/03_Inspector_Rutas_Traceroute.ps1) | [Routing_y_WAN](../Routing_y_WAN/README.md) | Traza TTL salto a salto con medición de RTT x 3 y resolución inversa PTR. |
| **Capa 4** | [`04_Auditor_TCP_Sockets_Salud.ps1`](./powershell/04_Auditor_TCP_Sockets_Salud.ps1) | [Troubleshooting](../Troubleshooting/README.md) | Estados de conexión TCP, servicios en escucha y detección de fugas (CloseWait). |
| **DDI / NTP** | [`05_Auditor_DNS_DHCP_NTP.ps1`](./powershell/05_Auditor_DNS_DHCP_NTP.ps1) | [Servicios_DDI_y_Gestion](../Servicios_DDI_y_Gestion/README.md) | Tiempo de resolución DNS, concesión DHCP (WMI) y estrato de reloj NTP. |
| **Wireless** | [`06_Auditor_WiFi_Enterprise.ps1`](./powershell/06_Auditor_WiFi_Enterprise.ps1) | [Wireless_Enterprise](../Wireless_Enterprise/README.md) | RSSI en dBm, estándar 802.11ax/ac, banda (2.4/5/6 GHz), canal y seguridad WPA3. |
| **Firewall** | [`07_Gestor_Firewall_Perfiles.ps1`](./powershell/07_Gestor_Firewall_Perfiles.ps1) | [Firewalls_y_VPN](../Firewalls_y_VPN/README.md) | Auditoría de reglas y comportamiento predeterminado en los 3 perfiles de Windows. |
| **Hardening** | [`02_Hardening_Red_Insegura.cmd`](./cmd/02_Hardening_Red_Insegura.cmd) | [Ciberseguridad_OSI](../Ciberseguridad_OSI/README.md) | Cierra vectores de ataque mitigando SMBv1, LLMNR, NetBIOS y WPAD. |
| **QoS** | [`08_Verificador_QoS_DSCP.ps1`](./powershell/08_Verificador_QoS_DSCP.ps1) | [QoS_Traffic_Shaping](../QoS_Traffic_Shaping/README.md) | Revisa políticas DSCP (RFC 4594) y habilitación de marcado TOS en registro. |
| **OT / SCADA** | [`09_Tester_Conectividad_OT.ps1`](./powershell/09_Tester_Conectividad_OT.ps1) | [Redes_Industriales_OT](../Redes_Industriales_OT/README.md) | Sondeo de disponibilidad en sockets Modbus (502), S7 (102), CIP (44818), DNP3 (20000). |
| **Pila TCP** | [`05_Optimizador_TCP_Pila.cmd`](./cmd/05_Optimizador_TCP_Pila.cmd) | [Troubleshooting](../Troubleshooting/README.md) | Configura Auto-Tuning, RSS, ECN y algoritmo de congestión CUBIC. |

---

**Autor:** Ezequiel ([@Cru9](https://github.com/Cru9))  
**Licencia:** [MIT License](../LICENSE)
