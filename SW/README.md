# 🖧 Conmutación Multi-Vendor (Switching Multi-Fabricante)

<p align="center">
  <img src="https://img.shields.io/badge/Cisco-Catalyst%20IOS%2FIOS--XE-005073?style=for-the-badge&logo=cisco&logoColor=white" />
  <img src="https://img.shields.io/badge/Huawei-CloudEngine%20VRP-c7000b?style=for-the-badge&logo=huawei&logoColor=white" />
  <img src="https://img.shields.io/badge/Aruba-ArubaOS--CX-ff8300?style=for-the-badge&logo=aruba&logoColor=white" />
  <img src="https://img.shields.io/badge/HP-ProCurve%20Provision-0096d6?style=for-the-badge&logo=hp&logoColor=white" />
  <img src="https://img.shields.io/badge/3Com-Comware%20OS-002f6c?style=for-the-badge" />
  <img src="https://img.shields.io/badge/TP--Link-JetStream%20L2%2FL3-4acbd6?style=for-the-badge" />
</p>

---

## 📌 Visión General del Módulo de Switching

En la ingeniería de redes corporativas, es fundamental dominar múltiples dialectos de CLI. Este módulo reúne **72 guías técnicas y 6 plantillas maestras de configuración** organizadas por fabricante, permitiendo trasladar conceptos arquitectónicos (VLANs, agregación de enlaces, Spanning Tree, enrutamiento inter-VLAN, seguridad L2 y alta disponibilidad) a la sintaxis exacta de cada conmutador.

---

## 🏢 Fabricantes Incluidos

| Fabricante | Sistema Operativo | Guía de Inicio | Plantilla de Producción |
| :--- | :--- | :--- | :--- |
| **Cisco** | IOS / IOS-XE | [Manual Cisco](./Cisco/README.md) | [Plantilla Hardened](./Cisco/PLANTILLA_CONFIGURACION_SWITCH.md) |
| **Huawei** | VRP (Versatile Routing Platform) | [Manual Huawei](./Huawei/README.md) | [Plantilla Hardened](./Huawei/PLANTILLA_CONFIGURACION_SWITCH.md) |
| **Aruba** | ArubaOS-CX / Provision | [Manual Aruba](./Aruba/README.md) | [Plantilla Hardened](./Aruba/PLANTILLA_CONFIGURACION_SWITCH.md) |
| **HP** | ProCurve / Provision (AOS-S) | [Manual HP](./HP/README.md) | [Plantilla Hardened](./HP/PLANTILLA_CONFIGURACION_SWITCH.md) |
| **3Com** | Comware OS | [Manual 3Com](./3Com/README.md) | [Plantilla Hardened](./3Com/PLANTILLA_CONFIGURACION_SWITCH.md) |
| **TP-Link** | JetStream L2/L3 CLI | [Manual TP-Link](./TP-Link/README.md) | [Plantilla Hardened](./TP-Link/PLANTILLA_CONFIGURACION_SWITCH.md) |

---

## 🔄 Tabla Maestra de Equivalencia de Modos y Comandos

| Acción Técnica | Cisco IOS / IOS-XE | Huawei VRP | Aruba ArubaOS-CX | HP ProCurve | 3Com Comware |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Modo Configuración** | `configure terminal` | `system-view` | `configure terminal` | `configure` | `system-view` |
| **Salir / Retroceder** | `exit` / `end` | `quit` / `return` | `exit` / `end` | `exit` | `quit` / `return` |
| **Guardar Config** | `write memory` / `copy run start` | `save` | `write memory` | `write memory` | `save` |
| **Ver Configuración** | `show running-config` | `display current-configuration` | `show running-config` | `show run` | `display current-configuration` |
| **Estado Interfaces** | `show ip int brief` | `display ip interface brief` | `show interface brief` | `show ip` | `display ip interface brief` |
| **Tabla MAC** | `show mac address-table` | `display mac-address` | `show mac-address` | `show mac-address` | `display mac-address` |
| **VLANs Activas** | `show vlan brief` | `display vlan` | `show vlan` | `show vlans` | `display vlan` |

---

**Volver al índice maestro:** [README Principal](../README.md)